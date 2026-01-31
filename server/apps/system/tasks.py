# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from datetime import date
import logging

from apps.system.models import GithubTrending
from utils.github_trending import get_github_trending, format_trending_data
from utils.github_analyzer import analyze_github_project

logger = logging.getLogger('log')


@shared_task
def show():
    print('ok')


@shared_task(name='fetch_github_trending')
def fetch_github_trending():
    """
    定时任务：获取 GitHub Trending 数据并使用 AI 分析
    每天早上 9 点执行
    分别获取日榜和周榜，每个榜单20条数据
    """
    try:
        logger.info("=" * 50)
        logger.info("开始执行 GitHub Trending 数据获取任务")
        logger.info("=" * 50)

        collection_date = date.today()
        total_count = 0
        success_count = 0

        # 分别获取日榜和周榜
        for since in ['daily', 'weekly']:
            logger.info(f"正在获取 {since} 热门项目...")

            # 获取 Trending 数据（不限语言，获取前20条）
            trending_data = get_github_trending(language='', since=since)

            if not trending_data:
                logger.warning(f"{since} 未获取到数据")
                continue

            # 只取前20条
            trending_data = trending_data[:20]

            logger.info(f"{since} 获取到 {len(trending_data)} 个项目")

            # 格式化数据
            formatted_data = format_trending_data(trending_data, collection_date)

            # 保存并分析每个项目
            for item in formatted_data:
                try:
                    total_count += 1

                    # 检查是否已存在
                    exists = GithubTrending.objects.filter(
                        collection_date=collection_date,
                        full_name=item['full_name'],
                        since=since
                    ).exists()

                    if exists:
                        logger.info(f"项目 {item['full_name']} 已存在，跳过")
                        continue

                    # AI 分析
                    logger.info(f"正在分析项目: {item['full_name']}")
                    ai_analysis = analyze_github_project(item)

                    # 创建数据库记录
                    GithubTrending.objects.create(
                        author=item['author'],
                        name=item['name'],
                        full_name=item['full_name'],
                        url=item['url'],
                        description=item['description'],
                        language=item['language'],
                        stars=item['stars'],
                        forks=item['forks'],
                        current_period_stars=item['current_period_stars'],
                        avatar=item['avatar'],
                        collection_date=item['collection_date'],
                        since=item['since'],
                        ai_analysis=ai_analysis,
                        extra_data=item['extra_data']
                    )

                    success_count += 1
                    logger.info(f"成功保存项目: {item['full_name']}")

                except Exception as e:
                    logger.error(f"处理项目失败 {item.get('full_name', '')}: {str(e)}")
                    continue

        logger.info("=" * 50)
        logger.info(f"任务完成！总数: {total_count}, 成功: {success_count}")
        logger.info("=" * 50)

        return {
            'status': 'success',
            'total': total_count,
            'success': success_count,
            'date': str(collection_date)
        }

    except Exception as e:
        logger.error(f"GitHub Trending 任务执行失败: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }
