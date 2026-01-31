"""
更新现有 GitHub Trending 数据的 AI 分析字段
为已有的记录添加中文标题和简介
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

def update_ai_analysis_fields():
    """更新 AI 分析字段，添加 title 和 summary"""
    print("开始更新 AI 分析字段...")

    # 获取所有记录
    records = GithubTrending.objects.filter(is_deleted=False)
    total = records.count()

    print(f"找到 {total} 条记录")

    updated_count = 0
    for record in records:
        if record.ai_analysis and isinstance(record.ai_analysis, dict):
            # 如果还没有 title 和 summary，添加默认值
            updated = False

            if 'title' not in record.ai_analysis:
                language = record.language or '未知'
                record.ai_analysis['title'] = f"{language}开源项目" if language != '未知' else "热门开源项目"
                updated = True

            if 'summary' not in record.ai_analysis:
                description = record.description or '暂无描述'
                full_name = record.full_name or '未知项目'
                short_desc = description[:100] if len(description) > 100 else description
                record.ai_analysis['summary'] = f"{full_name} 是一个优秀的开源项目。{short_desc}"
                updated = True

            if updated:
                record.save(update_fields=['ai_analysis'])
                updated_count += 1
                print(f"已更新: {record.full_name}")

    print(f"\n完成！更新了 {updated_count} 条记录")

if __name__ == '__main__':
    update_ai_analysis_fields()
