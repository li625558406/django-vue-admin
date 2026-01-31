"""
手动触发 GitHub Trending 定时任务
用于测试和初始化数据
"""
import os
import sys
import django

# 设置 Django 环境
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from apps.system.tasks import fetch_github_trending
from apps.system.models import GithubTrending

if __name__ == '__main__':
    print("=" * 50)
    print("开始手动触发 GitHub Trending 任务")
    print("=" * 50)
    print()

    # 执行任务（同步调用，不使用 Celery）
    result = fetch_github_trending()

    print()
    print("=" * 50)
    print("任务执行结果:")
    print(f"  状态: {result.get('status')}")
    print(f"  总数: {result.get('total', 0)}")
    print(f"  成功: {result.get('success', 0)}")
    print(f"  日期: {result.get('date', 'N/A')}")
    print("=" * 50)
    print()

    # 查询数据库验证数据
    print("验证数据库中的数据:")
    count = GithubTrending.objects.filter(is_deleted=False).count()
    print(f"  总记录数: {count}")

    if count > 0:
        latest = GithubTrending.objects.filter(is_deleted=False).order_by('-create_time')[:5]
        print()
        print("最新的 5 条记录:")
        for item in latest:
            print(f"  - {item.full_name} ({item.language}) - Stars: {item.stars}")
    print()
    print("=" * 50)
    print("任务完成！现在可以访问前端页面查看效果:")
    print("  http://localhost:8080/github-trending")
    print("=" * 50)
