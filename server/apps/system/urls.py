from django.urls import path, include
from .views import TaskList, UserViewSet, OrganizationViewSet, PermissionViewSet, RoleViewSet, PositionViewSet, TestView, DictTypeViewSet, DictViewSet, PTaskViewSet
from .github_trending_views import (
    GithubTrendingListView,
    GithubTrendingDetailView,
    GithubTrendingStatsView,
    TriggerFetchTrendingView
)
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user', UserViewSet, basename="user")
router.register('organization', OrganizationViewSet, basename="organization")
router.register('permission', PermissionViewSet, basename="permission")
router.register('role', RoleViewSet, basename="role")
router.register('position', PositionViewSet, basename="position")
router.register('dicttype', DictTypeViewSet, basename="dicttype")
router.register('dict', DictViewSet, basename="dict")
router.register('ptask', PTaskViewSet, basename="ptask")
urlpatterns = [
    path('', include(router.urls)),
    path('task/', TaskList.as_view()),
    path('test/', TestView.as_view()),
    # GitHub Trending 相关接口
    path('github/trending/', GithubTrendingListView.as_view(), name='github-trending-list'),
    path('github/trending/<int:id>/', GithubTrendingDetailView.as_view(), name='github-trending-detail'),
    path('github/trending/stats/', GithubTrendingStatsView.as_view(), name='github-trending-stats'),
    path('github/trending/trigger/', TriggerFetchTrendingView.as_view(), name='github-trending-trigger'),
]
