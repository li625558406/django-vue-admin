"""
GitHub Trending API 服务
用于获取 GitHub 热门项目数据
"""
import requests
import logging
from typing import List, Dict, Optional
from datetime import date

logger = logging.getLogger('log')


class GithubTrendingAPI:
    """GitHub Trending API 客户端"""

    def __init__(self, base_url: str = "https://gtrend.yapie.me/repositories"):
        """
        初始化 GitHub Trending API 客户端

        Args:
            base_url: API 基础地址
        """
        self.base_url = base_url
        self.timeout = 30  # 请求超时时间（秒）

    def get_trending(
        self,
        language: str = 'python',
        since: str = 'daily',
        spoken_language_code: Optional[str] = None
    ) -> List[Dict]:
        """
        获取 GitHub Trending 数据

        Args:
            language: 编程语言 (如 python, javascript, go, rust)
            since: 时间范围 (daily, weekly, monthly)
            spoken_language_code: 开发者主要语言 (如 zh, en)

        Returns:
            List[Dict]: 热门项目列表
        """
        params = {
            "language": language,
            "since": since,
        }

        if spoken_language_code:
            params["spoken_language_code"] = spoken_language_code

        try:
            logger.info(f"正在获取 GitHub Trending: language={language}, since={since}")
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(f"成功获取 {len(data)} 个热门项目")
                return data
            else:
                logger.error(f"请求失败，状态码: {response.status_code}")
                return []

        except requests.exceptions.Timeout:
            logger.error(f"请求超时: {self.base_url}")
            return []
        except requests.exceptions.RequestException as e:
            logger.error(f"请求发生错误: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            return []

    def get_multi_language_trending(
        self,
        languages: List[str] = ['python', 'javascript', 'go', 'rust', 'java'],
        since: str = 'daily'
    ) -> Dict[str, List[Dict]]:
        """
        获取多种编程语言的热门项目

        Args:
            languages: 编程语言列表
            since: 时间范围

        Returns:
            Dict[str, List[Dict]]: 各语言的热门项目
        """
        result = {}

        for language in languages:
            logger.info(f"正在获取 {language} 的热门项目...")
            trending_data = self.get_trending(language=language, since=since)
            result[language] = trending_data

        return result


# 全局实例
github_trending_api = GithubTrendingAPI()


def get_github_trending(
    language: str = 'python',
    since: str = 'daily',
    spoken_language_code: Optional[str] = None
) -> List[Dict]:
    """
    获取 GitHub Trending 数据（便捷函数）

    Args:
        language: 编程语言
        since: 时间范围
        spoken_language_code: 开发者主要语言

    Returns:
        List[Dict]: 热门项目列表
    """
    return github_trending_api.get_trending(language, since, spoken_language_code)


def format_trending_data(raw_data: List[Dict], collection_date: date) -> List[Dict]:
    """
    格式化 GitHub Trending 数据，用于存储到数据库

    Args:
        raw_data: API 返回的原始数据
        collection_date: 采集日期

    Returns:
        List[Dict]: 格式化后的数据
    """
    formatted_data = []

    for item in raw_data:
        formatted_item = {
            'author': item.get('author', ''),
            'name': item.get('name', ''),
            'full_name': f"{item.get('author', '')}/{item.get('name', '')}",
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
                'builtBy': item.get('builtBy', []),
            }
        }
        formatted_data.append(formatted_item)

    return formatted_data
