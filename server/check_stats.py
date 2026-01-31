"""
查看 GitHub Trending 数据统计
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

from apps.system.models import GithubTrending
from django.db.models import Count

qs = GithubTrending.objects.filter(is_deleted=False)

print(f'Total records: {qs.count()}')
print()
print('Statistics by language:')
for lang, count in qs.values('language').annotate(count=Count('id')).order_by('-count'):
    lang_name = lang or 'Unknown'
    print(f'  {lang_name}: {count}')

print()
print('Latest 5 records:')
for item in qs.order_by('-create_time')[:5]:
    print(f'  - {item.full_name} ({item.language}) - Stars: {item.stars} - Today: +{item.current_period_stars}')
