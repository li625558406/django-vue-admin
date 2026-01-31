"""
GitHub Trending API 接口
提供 GitHub 热门项目的查询接口
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from datetime import date, timedelta
import logging

from apps.system.models import GithubTrending
from apps.system.tasks import fetch_github_trending

logger = logging.getLogger('log')


@method_decorator(csrf_exempt, name='dispatch')
class GithubTrendingListView(APIView):
    """
    GitHub Trending 列表接口

    GET /api/github/trending/
    参数:
        - date: 日期 (YYYY-MM-DD 格式，默认今天)
        - language: 编程语言筛选
        - limit: 返回数量限制 (默认 50)
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        try:
            # 获取查询参数
            date_str = request.GET.get('date')
            language = request.GET.get('language', '')
            limit = int(request.GET.get('limit', 50))

            # 确定查询日期
            if date_str:
                try:
                    query_date = date.fromisoformat(date_str)
                except ValueError:
                    return Response({
                        'success': False,
                        'message': '日期格式错误，请使用 YYYY-MM-DD 格式'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                query_date = date.today()

            # 构建查询
            queryset = GithubTrending.objects.filter(
                collection_date=query_date,
                is_deleted=False
            )

            # 语言筛选
            if language:
                queryset = queryset.filter(language__icontains=language)

            # 排序
            queryset = queryset.order_by('-current_period_stars')

            # 限制数量
            queryset = queryset[:limit]

            # 序列化数据
            data_list = []
            for item in queryset:
                data_list.append({
                    'id': item.id,
                    'author': item.author,
                    'name': item.name,
                    'full_name': item.full_name,
                    'url': item.url,
                    'description': item.description,
                    'language': item.language,
                    'stars': item.stars,
                    'forks': item.forks,
                    'current_period_stars': item.current_period_stars,
                    'avatar': item.avatar,
                    'collection_date': item.collection_date.isoformat(),
                    'ai_analysis': item.ai_analysis or {},
                })

            return Response({
                'success': True,
                'data': data_list,
                'total': len(data_list),
                'date': query_date.isoformat()
            })

        except Exception as e:
            logger.error(f'获取 GitHub Trending 失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class GithubTrendingDetailView(APIView):
    """
    GitHub Trending 详情接口

    GET /api/github/trending/<id>/
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        try:
            item = GithubTrending.objects.get(id=id, is_deleted=False)

            return Response({
                'success': True,
                'data': {
                    'id': item.id,
                    'author': item.author,
                    'name': item.name,
                    'full_name': item.full_name,
                    'url': item.url,
                    'description': item.description,
                    'language': item.language,
                    'stars': item.stars,
                    'forks': item.forks,
                    'current_period_stars': item.current_period_stars,
                    'avatar': item.avatar,
                    'collection_date': item.collection_date.isoformat(),
                    'since': item.since,
                    'ai_analysis': item.ai_analysis or {},
                    'extra_data': item.extra_data or {},
                    'created_at': item.create_datetime.isoformat() if item.create_datetime else None,
                }
            })

        except GithubTrending.DoesNotExist:
            return Response({
                'success': False,
                'message': '项目不存在'
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f'获取 GitHub Trending 详情失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class GithubTrendingStatsView(APIView):
    """
    GitHub Trending 统计接口

    GET /api/github/trending/stats/
    参数:
        - days: 统计最近几天 (默认 7 天)
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        try:
            days = int(request.GET.get('days', 7))
            end_date = date.today()
            start_date = end_date - timedelta(days=days)

            # 统计数据
            queryset = GithubTrending.objects.filter(
                collection_date__gte=start_date,
                collection_date__lte=end_date,
                is_deleted=False
            )

            # 按语言统计
            language_stats = {}
            for item in queryset:
                lang = item.language or 'Unknown'
                if lang not in language_stats:
                    language_stats[lang] = {
                        'count': 0,
                        'total_stars': 0,
                        'total_current_stars': 0
                    }
                language_stats[lang]['count'] += 1
                language_stats[lang]['total_stars'] += item.stars
                language_stats[lang]['total_current_stars'] += item.current_period_stars

            # 按日期统计
            date_stats = {}
            for item in queryset:
                date_str = item.collection_date.isoformat()
                if date_str not in date_stats:
                    date_stats[date_str] = 0
                date_stats[date_str] += 1

            return Response({
                'success': True,
                'data': {
                    'period': {
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat(),
                        'days': days
                    },
                    'total_projects': queryset.count(),
                    'language_stats': language_stats,
                    'date_stats': date_stats
                }
            })

        except Exception as e:
            logger.error(f'获取 GitHub Trending 统计失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class TriggerFetchTrendingView(APIView):
    """
    手动触发获取 GitHub Trending 任务

    POST /api/github/trending/trigger/
    需要登录认证
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # 异步执行任务
            task = fetch_github_trending.delay()

            return Response({
                'success': True,
                'message': '任务已触发',
                'task_id': task.id
            })

        except Exception as e:
            logger.error(f'触发 GitHub Trending 任务失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# URL 配置示例
"""
# urls.py
from django.urls import path
from .github_trending_views import (
    GithubTrendingListView,
    GithubTrendingDetailView,
    GithubTrendingStatsView,
    TriggerFetchTrendingView
)

urlpatterns = [
    path('api/github/trending/', GithubTrendingListView.as_view(), name='github-trending-list'),
    path('api/github/trending/<int:id>/', GithubTrendingDetailView.as_view(), name='github-trending-detail'),
    path('api/github/trending/stats/', GithubTrendingStatsView.as_view(), name='github-trending-stats'),
    path('api/github/trending/trigger/', TriggerFetchTrendingView.as_view(), name='github-trending-trigger'),
]
"""
