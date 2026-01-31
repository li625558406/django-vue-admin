"""
GitHub Trending 爬虫服务
直接从 GitHub Trending 页面爬取数据（不依赖第三方 API）
"""
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
import re
from datetime import date

logger = logging.getLogger('log')


class GithubTrendingCrawler:
    """GitHub Trending 爬虫类"""

    def __init__(self):
        """初始化爬虫"""
        self.base_url = "https://github.com/trending"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.timeout = 30

    def fetch_trending(
        self,
        language: str = '',
        since: str = 'daily'
    ) -> List[Dict]:
        """
        爬取 GitHub Trending 数据

        Args:
            language: 编程语言 (如 python, javascript，空字符串代表所有)
            since: 时间范围 (daily, weekly, monthly)

        Returns:
            List[Dict]: 热门项目列表
        """
        # 构建 URL
        url = f"{self.base_url}/{language}" if language else self.base_url
        params = {'since': since} if since != 'daily' else {}

        try:
            logger.info(f"正在爬取 GitHub Trending: language={language or 'all'}, since={since}")

            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()

            # 解析 HTML
            soup = BeautifulSoup(response.text, 'lxml')
            repos = []

            # 找到所有的项目文章 (GitHub 使用 article.Box-row)
            articles = soup.find_all('article', class_='Box-row')
            logger.info(f"找到 {len(articles)} 个项目")

            for article in articles:
                repo = self._parse_article(article, language, since)
                if repo:
                    repos.append(repo)

            logger.info(f"成功解析 {len(repos)} 个项目")
            return repos

        except requests.exceptions.Timeout:
            logger.error(f'请求超时: {url}')
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f'请求发生错误: {str(e)}')
            return []
        except Exception as e:
            logger.error(f'未知错误: {str(e)}')
            return []

    def _parse_article(self, article, language: str = '', since: str = 'daily') -> Dict:
        """
        解析单个项目的 HTML

        Args:
            article: BeautifulSoup Article 对象
            language: 默认编程语言
            since: 时间范围

        Returns:
            Dict: 项目信息
        """
        try:
            repo = {}

            # 1. 提取项目名称和地址
            h1 = article.find('h2', class_='h3 lh-condensed')
            if h1 and h1.a:
                full_name = h1.a.get_text(strip=True)
                repo['full_name'] = full_name
                repo['url'] = "https://github.com" + h1.a['href']

                # 分割作者和项目名
                if '/' in full_name:
                    parts = full_name.split('/')
                    repo['author'] = parts[0]
                    repo['name'] = parts[1]
                else:
                    repo['author'] = full_name
                    repo['name'] = full_name
            else:
                # 备用方案
                link = article.find('a', href=True)
                if link:
                    href = link['href']
                    if href.startswith('/'):
                        repo['url'] = "https://github.com" + href
                        parts = href.strip('/').split('/')
                        if len(parts) >= 2:
                            repo['author'] = parts[0]
                            repo['name'] = parts[1]
                            repo['full_name'] = f"{parts[0]}/{parts[1]}"

            # 2. 提取描述
            p = article.find('p', class_='col-9')
            if not p:
                p = article.find('p')
            repo['description'] = p.get_text(strip=True) if p else ""

            # 3. 提取编程语言
            lang_span = article.find('span', itemprop='programmingLanguage')
            repo['language'] = lang_span.get_text(strip=True) if lang_span else (language.capitalize() if language else '')

            # 4. 提取编程语言颜色
            color_span = article.find('span', class_='d-inline-block ml-0 mr-3')
            if color_span and color_span.get('class'):
                # 尝试获取语言颜色
                repo['languageColor'] = ''
            else:
                repo['languageColor'] = ''

            # 5. 提取 Star 总数
            star_link = article.find('a', href=lambda x: x and x.endswith('/stargazers'))
            if star_link:
                stars_text = star_link.get_text(strip=True)
                repo['stars'] = self._parse_number(stars_text)
            else:
                # 尝试从其他位置获取
                stars_spans = article.find_all('a', href=lambda x: x and 'stargazers' in x)
                if stars_spans:
                    repo['stars'] = self._parse_number(stars_spans[0].get_text(strip=True))
                else:
                    repo['stars'] = 0

            # 6. 提取 Fork 数
            fork_link = article.find('a', href=lambda x: x and x.endswith('/forks'))
            if fork_link:
                forks_text = fork_link.get_text(strip=True)
                repo['forks'] = self._parse_number(forks_text)
            else:
                repo['forks'] = 0

            # 7. 提取今日/本周新增 Star 数
            # GitHub 使用 "d-inline-block float-sm-right" 类
            today_stars_elem = article.find('span', class_='d-inline-block float-sm-right')
            if today_stars_elem:
                today_text = today_stars_elem.get_text(strip=True)
                # 提取数字，例如 "100 stars today" 或 "1,200 stars this week"
                numbers = re.findall(r'[\d,]+', today_text)
                if numbers:
                    repo['currentPeriodStars'] = int(numbers[0].replace(',', ''))
                else:
                    repo['currentPeriodStars'] = 0
            else:
                # 备用：查找包含 "stars" 的文本
                all_spans = article.find_all('span')
                for span in all_spans:
                    text = span.get_text(strip=True)
                    if 'stars' in text.lower() and ('today' in text.lower() or 'week' in text.lower() or 'month' in text.lower()):
                        numbers = re.findall(r'[\d,]+', text)
                        if numbers:
                            repo['currentPeriodStars'] = int(numbers[0].replace(',', ''))
                            break
                else:
                    repo['currentPeriodStars'] = 0

            # 8. 提取作者头像
            avatar_img = article.find('img', class_='avatar')
            if avatar_img and avatar_img.get('src'):
                repo['avatar'] = avatar_img['src']
            else:
                # 尝试找到其他头像
                avatar_link = article.find('a', class_='d-inline-block')
                if avatar_link:
                    img = avatar_link.find('img')
                    if img and img.get('src'):
                        repo['avatar'] = img['src']
                    else:
                        repo['avatar'] = ''
                else:
                    repo['avatar'] = ''

            # 9. 添加时间范围标识
            repo['since'] = since

            # 验证必要字段
            if 'full_name' in repo and 'url' in repo:
                return repo
            else:
                return None

        except Exception as e:
            logger.error(f'解析项目失败: {str(e)}')
            return None

    def _parse_number(self, text: str) -> int:
        """
        解析数字字符串（如 "1.2k", "100"）

        Args:
            text: 数字字符串

        Returns:
            int: 解析后的整数
        """
        if not text:
            return 0

        text = text.strip().replace(',', '')

        # 处理 k 后缀（如 1.2k = 1200）
        if 'k' in text.lower():
            try:
                num = float(text.lower().replace('k', ''))
                return int(num * 1000)
            except ValueError:
                return 0

        # 处理普通数字
        try:
            return int(text)
        except ValueError:
            return 0

    def get_multi_language_trending(
        self,
        language_list: List[str] = ['python', 'javascript', 'go', 'rust', 'java', 'typescript'],
        since: str = 'daily'
    ) -> Dict[str, List[Dict]]:
        """
        获取多种编程语言的热门项目

        Args:
            language_list: 编程语言列表
            since: 时间范围

        Returns:
            Dict[str, List[Dict]]: 各语言的热门项目
        """
        result = {}

        for language in language_list:
            logger.info(f"正在爬取 {language} 的热门项目...")
            trending_data = self.fetch_trending(language=language, since=since)
            result[language] = trending_data

        return result


# 全局实例
github_crawler = GithubTrendingCrawler()


def get_github_trending(
    language: str = '',
    since: str = 'daily'
) -> List[Dict]:
    """
    获取 GitHub Trending 数据（便捷函数）

    Args:
        language: 编程语言
        since: 时间范围

    Returns:
        List[Dict]: 热门项目列表
    """
    return github_crawler.fetch_trending(language, since)


def format_trending_data(raw_data: List[Dict], collection_date: date) -> List[Dict]:
    """
    格式化 GitHub Trending 数据，用于存储到数据库

    Args:
        raw_data: 爬虫返回的原始数据
        collection_date: 采集日期

    Returns:
        List[Dict]: 格式化后的数据
    """
    formatted_data = []

    for item in raw_data:
        formatted_item = {
            'author': item.get('author', ''),
            'name': item.get('name', ''),
            'full_name': item.get('full_name', ''),
            'url': item.get('url', ''),
            'description': item.get('description', ''),
            'language': item.get('language', ''),
            'stars': item.get('stars', 0),
            'forks': item.get('forks', 0),
            'current_period_stars': item.get('currentPeriodStars', 0),
            'avatar': item.get('avatar', ''),
            'collection_date': collection_date,
            'since': item.get('since', 'daily'),
            'extra_data': {
                'languageColor': item.get('languageColor', ''),
            }
        }
        formatted_data.append(formatted_item)

    return formatted_data
