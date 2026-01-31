"""
检查 Django URL 配置
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

from django.urls import get_resolver

resolver = get_resolver()
patterns = []

def collect_urls(urlpatterns, prefix=''):
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            collect_urls(pattern.url_patterns, prefix + str(pattern.pattern))
        else:
            patterns.append(prefix + str(pattern.pattern))

collect_urls(resolver.url_patterns)

print('All URLs containing "github":')
for url in patterns:
    if 'github' in url.lower():
        print(f'  {url}')
