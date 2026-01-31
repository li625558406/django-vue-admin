"""
Google Gemini AI 视图示例
演示如何在 Django REST Framework 中使用 Gemini AI 客户端，包括 Google Search 联网搜索
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from http import StreamingHttpResponse
import json

from utils.gemini_client import ask_gemini, chat_gemini, stream_gemini
import logging

logger = logging.getLogger('log')


@method_decorator(csrf_exempt, name='dispatch')
class SimpleGeminiChatView(APIView):
    """
    简单的 Gemini AI 聊天接口

    POST /api/gemini/simple-chat/
    {
        "prompt": "你好",
        "system_prompt": "你是一个友好的助手",  // 可选
        "enable_search": false  // 可选，是否启用联网搜索
    }
    """
    authentication_classes = []  # 允许匿名访问，根据需要调整
    permission_classes = []

    def post(self, request):
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '').strip()
            system_prompt = data.get('system_prompt', 'You are a helpful assistant')
            enable_search = data.get('enable_search', False)

            if not prompt:
                return Response({
                    'success': False,
                    'message': 'prompt 参数不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 调用 Gemini AI
            response = ask_gemini(prompt, system_prompt, enable_search=enable_search)

            return Response({
                'success': True,
                'response': response,
                'search_enabled': enable_search
            })

        except Exception as e:
            logger.error(f'Gemini AI 聊天失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class GeminiConversationView(APIView):
    """
    Gemini AI 多轮对话接口

    POST /api/gemini/conversation/
    {
        "messages": [
            {"role": "system", "content": "你是一个Python专家"},
            {"role": "user", "content": "Django是什么？"}
        ],
        "temperature": 1.0,  // 可选，默认 1.0
        "enable_search": false  // 可选，是否启用联网搜索
    }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            data = json.loads(request.body)
            messages = data.get('messages', [])
            temperature = data.get('temperature', 1.0)
            enable_search = data.get('enable_search', False)

            if not messages:
                return Response({
                    'success': False,
                    'message': 'messages 参数不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 调用 Gemini AI
            result = chat_gemini(messages, temperature=temperature, enable_search=enable_search)

            if result['success']:
                return Response({
                    'success': True,
                    'content': result['content'],
                    'usage': result['usage'],
                    'search_results': result.get('search_results'),
                    'search_enabled': enable_search
                })
            else:
                return Response({
                    'success': False,
                    'message': result['message']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f'Gemini AI 对话失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class GeminiStreamView(APIView):
    """
    Gemini AI 流式响应接口 (SSE)

    POST /api/gemini/stream/
    {
        "prompt": "讲一个故事",
        "enable_search": false  // 可选
    }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '').strip()
            enable_search = data.get('enable_search', False)

            if not prompt:
                return Response({
                    'success': False,
                    'message': 'prompt 参数不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)

            messages = [{"role": "user", "content": prompt}]

            def generate():
                """生成流式响应"""
                try:
                    for chunk in stream_gemini(messages, enable_search=enable_search):
                        # SSE 格式
                        yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\\n\\n"
                except Exception as e:
                    logger.error(f'流式生成失败: {str(e)}')
                    yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\\n\\n"
                yield "data: [DONE]\\n\\n"

            return StreamingHttpResponse(
                generate(),
                content_type="text/event-stream"
            )

        except Exception as e:
            logger.error(f'Gemini AI 流式聊天失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProtectedGeminiChatView(APIView):
    """
    需要登录的 Gemini AI 聊天接口示例

    POST /api/gemini/chat/
    {
        "prompt": "帮我分析一下用户行为",
        "enable_search": true
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '').strip()
            enable_search = data.get('enable_search', False)

            if not prompt:
                return Response({
                    'success': False,
                    'message': 'prompt 参数不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 使用用户信息定制系统提示
            system_prompt = f"""
            你是一个智能助手，正在为用户 {request.user.username} 提供帮助。
            请根据用户的请求提供专业、友好的回复。
            """

            response = ask_gemini(prompt, system_prompt, enable_search=enable_search)

            # 记录 AI 使用情况（可选）
            logger.info(f'用户 {request.user.username} 使用了 Gemini AI 聊天，搜索={enable_search}')

            return Response({
                'success': True,
                'response': response,
                'user': request.user.username,
                'search_enabled': enable_search
            })

        except Exception as e:
            logger.error(f'Gemini AI 聊天失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class GeminiSearchView(APIView):
    """
    Gemini AI 联网搜索专用接口

    POST /api/gemini/search/
    {
        "query": "今天北京天气怎么样？",
        "system_prompt": "你是一个专业的信息查询助手"  // 可选
    }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            data = json.loads(request.body)
            query = data.get('query', '').strip()
            system_prompt = data.get('system_prompt', '你是一个专业的信息查询助手，请根据搜索结果提供准确的回答。')

            if not query:
                return Response({
                    'success': False,
                    'message': 'query 参数不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 调用 Gemini AI，强制启用联网搜索
            result = chat_gemini(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                enable_search=True  # 强制启用联网搜索
            )

            if result['success']:
                return Response({
                    'success': True,
                    'content': result['content'],
                    'usage': result['usage'],
                    'search_results': result.get('search_results'),
                    'search_enabled': True
                })
            else:
                return Response({
                    'success': False,
                    'message': result['message']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f'Gemini AI 搜索失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# URL 配置示例
"""
# urls.py
from django.urls import path
from .gemini_views import (
    SimpleGeminiChatView,
    GeminiConversationView,
    GeminiStreamView,
    ProtectedGeminiChatView,
    GeminiSearchView
)

urlpatterns = [
    path('api/gemini/simple-chat/', SimpleGeminiChatView.as_view(), name='gemini-simple-chat'),
    path('api/gemini/conversation/', GeminiConversationView.as_view(), name='gemini-conversation'),
    path('api/gemini/stream/', GeminiStreamView.as_view(), name='gemini-stream'),
    path('api/gemini/chat/', ProtectedGeminiChatView.as_view(), name='gemini-chat'),
    path('api/gemini/search/', GeminiSearchView.as_view(), name='gemini-search'),
]
"""
