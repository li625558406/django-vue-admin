"""
DeepSeek AI 视图示例
演示如何在 Django REST Framework 中使用 AI 客户端
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from http import StreamingHttpResponse
import json

from utils.ai_client import ask_ai, chat_ai, stream_ai
import logging

logger = logging.getLogger('log')


@method_decorator(csrf_exempt, name='dispatch')
class SimpleAIChatView(APIView):
    """
    简单的 AI 聊天接口

    POST /api/ai/simple-chat/
    {
        "prompt": "你好",
        "system_prompt": "你是一个友好的助手"  // 可选
    }
    """
    authentication_classes = []  # 允许匿名访问，根据需要调整
    permission_classes = []

    def post(self, request):
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '').strip()
            system_prompt = data.get('system_prompt', 'You are a helpful assistant')

            if not prompt:
                return Response({
                    'success': False,
                    'message': 'prompt 参数不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 调用 AI
            response = ask_ai(prompt, system_prompt)

            return Response({
                'success': True,
                'response': response
            })

        except Exception as e:
            logger.error(f'AI 聊天失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class AIConversationView(APIView):
    """
    AI 多轮对话接口

    POST /api/ai/conversation/
    {
        "messages": [
            {"role": "system", "content": "你是一个Python专家"},
            {"role": "user", "content": "Django是什么？"}
        ],
        "temperature": 1.0  // 可选，默认 1.0
    }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            data = json.loads(request.body)
            messages = data.get('messages', [])
            temperature = data.get('temperature', 1.0)

            if not messages:
                return Response({
                    'success': False,
                    'message': 'messages 参数不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 调用 AI
            result = chat_ai(messages, temperature=temperature)

            if result['success']:
                return Response({
                    'success': True,
                    'content': result['content'],
                    'usage': result['usage']
                })
            else:
                return Response({
                    'success': False,
                    'message': result['message']
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f'AI 对话失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class AIStreamView(APIView):
    """
    AI 流式响应接口 (SSE)

    POST /api/ai/stream/
    {
        "prompt": "讲一个故事"
    }
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '').strip()

            if not prompt:
                return Response({
                    'success': False,
                    'message': 'prompt 参数不能为空'
                }, status=status.HTTP_400_BAD_REQUEST)

            messages = [{"role": "user", "content": prompt}]

            def generate():
                """生成流式响应"""
                try:
                    for chunk in stream_ai(messages):
                        # SSE 格式
                        yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
                except Exception as e:
                    logger.error(f'流式生成失败: {str(e)}')
                    yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingHttpResponse(
                generate(),
                content_type="text/event-stream"
            )

        except Exception as e:
            logger.error(f'AI 流式聊天失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProtectedAIChatView(APIView):
    """
    需要登录的 AI 聊天接口示例

    POST /api/ai/chat/
    {
        "prompt": "帮我分析一下用户行为"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '').strip()

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

            response = ask_ai(prompt, system_prompt)

            # 记录 AI 使用情况（可选）
            logger.info(f'用户 {request.user.username} 使用了 AI 聊天')

            return Response({
                'success': True,
                'response': response,
                'user': request.user.username
            })

        except Exception as e:
            logger.error(f'AI 聊天失败: {str(e)}')
            return Response({
                'success': False,
                'message': f'服务器错误: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# URL 配置示例
"""
# urls.py
from django.urls import path
from .ai_views import (
    SimpleAIChatView,
    AIConversationView,
    AIStreamView,
    ProtectedAIChatView
)

urlpatterns = [
    path('api/ai/simple-chat/', SimpleAIChatView.as_view(), name='ai-simple-chat'),
    path('api/ai/conversation/', AIConversationView.as_view(), name='ai-conversation'),
    path('api/ai/stream/', AIStreamView.as_view(), name='ai-stream'),
    path('api/ai/chat/', ProtectedAIChatView.as_view(), name='ai-chat'),
]
"""
