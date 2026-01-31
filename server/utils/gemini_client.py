"""
Google Gemini AI 公共调用模块（使用新版 google-genai SDK）
提供统一的 Gemini 接口调用方法，支持 Google Search 联网搜索

SDK 版本: google-genai (新版)
文档: https://github.com/googleapis/python-genai
"""
import os
import logging
from typing import List, Dict, Optional, Any, AsyncGenerator

# 尝试加载 .env 文件（如果 python-dotenv 可用）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Django 通常会在 settings.py 中加载环境变量

# 使用新版 google-genai SDK
from google import genai
from google.genai import types

logger = logging.getLogger('log')


class GeminiClient:
    """Google Gemini AI 客户端封装（新版 SDK），支持 Google Search 联网搜索"""

    def __init__(self):
        """初始化 Gemini 客户端"""
        self.api_key = os.environ.get('GOOGLE_API_KEY')
        if not self.api_key:
            logger.warning('GOOGLE_API_KEY 未在环境变量中配置')
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)

        # 默认模型（使用最新版本）
        self.model_name = "gemini-3-flash-preview"

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 1.0,
        top_p: float = 0.95,
        enable_search: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送聊天请求到 Gemini API（新版 SDK）

        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}, ...]
                     注意: Gemini 使用 "user" 和 "model" 角色
            model: 模型名称，默认为 "gemini-1.5-flash"
            temperature: 温度参数，控制随机性，范围 0-2，默认 1.0
            top_p: 核采样参数，默认 0.95
            enable_search: 是否启用 Google Search 联网搜索，默认 False
            **kwargs: 其他参数

        Returns:
            Dict[str, Any]: API 响应结果
            {
                "success": bool,  # 是否成功
                "content": str,   # 返回的内容
                "message": str,   # 消息
                "usage": dict,    # 使用量统计
                "search_results": list,  # Google Search 结果（如果启用）
                "raw_response": dict  # 原始响应
            }
        """
        if not self.client:
            logger.error('GOOGLE_API_KEY 未配置')
            return {
                "success": False,
                "content": "",
                "message": "GOOGLE_API_KEY 未配置",
                "usage": None,
                "search_results": None,
                "raw_response": None
            }

        try:
            logger.info(f'调用 Gemini API (新版): model={model or self.model_name}, search={enable_search}')

            # 转换消息格式（OpenAI 格式 -> Gemini Content 格式）
            contents = self._convert_messages_to_contents(messages)

            # 配置生成参数
            if enable_search:
                # 启用 Google Search
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=top_p,
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    **kwargs
                )
            else:
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=top_p,
                    **kwargs
                )

            # 调用 API
            response = self.client.models.generate_content(
                model=model or self.model_name,
                contents=contents,
                config=config
            )

            # 解析响应
            result = {
                "success": True,
                "content": response.text,
                "message": "调用成功",
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') and response.usage_metadata else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') and response.usage_metadata else 0,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') and response.usage_metadata else 0,
                },
                "search_results": None,
                "raw_response": str(response)
            }

            # 提取 Google Search 结果（如果有）
            if enable_search and hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                        result['search_results'] = {
                            "grounding_supported": True,
                            "search_entry_present": hasattr(candidate.grounding_metadata, 'search_entry_point')
                        }
                        if hasattr(candidate.grounding_metadata, 'search_entry_point'):
                            result['search_results']['entry_point'] = str(candidate.grounding_metadata.search_entry_point)

            logger.info(f'Gemini API 调用成功: tokens={result["usage"]["total_tokens"]}')
            return result

        except Exception as e:
            logger.error(f'Gemini API 调用失败: {str(e)}')
            return {
                "success": False,
                "content": "",
                "message": f"API 调用失败: {str(e)}",
                "usage": None,
                "search_results": None,
                "raw_response": None
            }

    def _convert_messages_to_contents(self, messages: List[Dict[str, str]]) -> List[types.Content]:
        """
        转换消息格式（OpenAI 格式 -> 新版 SDK Content 格式）

        Args:
            messages: OpenAI 格式的消息列表

        Returns:
            新版 SDK 的 Content 列表
        """
        contents = []

        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')

            # 转换角色名称
            if role == 'assistant':
                role = 'model'

            # 创建 Content 对象（新版 SDK 使用 from_text 创建 Part）
            part = types.Part.from_text(text=content)
            contents.append(
                types.Content(
                    role=role,
                    parts=[part]
                )
            )

        return contents

    def chat_simple(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful assistant",
        enable_search: bool = False,
        **kwargs
    ) -> str:
        """
        简化的聊天接口

        Args:
            prompt: 用户提示
            system_prompt: 系统提示
            enable_search: 是否启用 Google Search
            **kwargs: 其他传递给 chat 方法的参数

        Returns:
            str: AI 返回的内容，失败时返回空字符串
        """
        # 新版 SDK 将系统提示作为第一条消息
        messages = [
            {"role": "user", "content": f"{system_prompt}\n\n{prompt}"}
        ]

        result = self.chat(messages, enable_search=enable_search, **kwargs)

        if result["success"]:
            return result["content"]
        else:
            logger.error(f'Gemini 调用失败: {result["message"]}')
            return ""

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 1.0,
        top_p: float = 0.95,
        enable_search: bool = False,
        **kwargs
    ):
        """
        流式聊天接口

        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            top_p: 核采样参数
            enable_search: 是否启用 Google Search
            **kwargs: 其他参数

        Yields:
            str: 流式返回的文本片段
        """
        if not self.client:
            logger.error('GOOGLE_API_KEY 未配置')
            yield "[ERROR] GOOGLE_API_KEY 未配置"
            return

        try:
            logger.info(f'调用 Gemini API (流式): model={model or self.model_name}, search={enable_search}')

            # 转换消息格式
            contents = self._convert_messages_to_contents(messages)

            # 配置生成参数
            if enable_search:
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=top_p,
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    **kwargs
                )
            else:
                config = types.GenerateContentConfig(
                    temperature=temperature,
                    top_p=top_p,
                    **kwargs
                )

            # 流式生成
            stream = self.client.models.generate_content_stream(
                model=model or self.model_name,
                contents=contents,
                config=config
            )

            for chunk in stream:
                if hasattr(chunk, 'text') and chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f'Gemini API 流式调用失败: {str(e)}')
            yield f"[ERROR] {str(e)}"


# 创建全局单例实例
_gemini_client = None


def get_gemini_client() -> GeminiClient:
    """
    获取 Gemini 客户端单例

    Returns:
        GeminiClient: Gemini 客户端实例
    """
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client


# 便捷函数
def ask_gemini(prompt: str, system_prompt: str = "You are a helpful assistant", enable_search: bool = False) -> str:
    """
    便捷的 Gemini 调用函数

    Args:
        prompt: 用户提示
        system_prompt: 系统提示
        enable_search: 是否启用 Google Search 联网搜索

    Returns:
        str: AI 返回的内容

    Example:
        >>> from utils.gemini_client import ask_gemini
        >>> response = ask_gemini("什么是人工智能？")
        >>> print(response)
        >>>
        >>> # 启用联网搜索
        >>> response = ask_gemini("今天北京天气如何？", enable_search=True)
        >>> print(response)
    """
    client = get_gemini_client()
    return client.chat_simple(prompt, system_prompt, enable_search=enable_search)


def chat_gemini(
    messages: List[Dict[str, str]],
    temperature: float = 1.0,
    enable_search: bool = False,
    stream: bool = False
) -> Dict[str, Any]:
    """
    完整的 Gemini 聊天函数

    Args:
        messages: 消息列表
        temperature: 温度参数
        enable_search: 是否启用 Google Search
        stream: 是否流式输出

    Returns:
        Dict[str, Any]: 完整的响应结果

    Example:
        >>> from utils.gemini_client import chat_gemini
        >>> messages = [
        ...     {"role": "system", "content": "你是一个Python专家"},
        ...     {"role": "user", "content": "如何使用Django？"}
        ... ]
        >>> result = chat_gemini(messages)
        >>> if result['success']:
        ...     print(result['content'])
        >>>
        >>> # 启用联网搜索
        >>> result = chat_gemini(
        ...     messages=[{"role": "user", "content": "今天热门新闻有哪些？"}],
        ...     enable_search=True
        ... )
        >>> if result['success']:
        ...     print(result['content'])
        ...     print(result['search_results'])
    """
    client = get_gemini_client()
    return client.chat(messages, temperature=temperature, enable_search=enable_search)


def stream_gemini(
    messages: List[Dict[str, str]],
    temperature: float = 1.0,
    enable_search: bool = False
):
    """
    流式 Gemini 聊天函数

    Args:
        messages: 消息列表
        temperature: 温度参数
        enable_search: 是否启用 Google Search

    Yields:
        str: 流式返回的文本片段

    Example:
        >>> from utils.gemini_client import stream_gemini
        >>> messages = [{"role": "user", "content": "讲个故事"}]
        >>> for chunk in stream_gemini(messages):
        ...     print(chunk, end="", flush=True)
    """
    client = get_gemini_client()
    yield from client.stream_chat(messages, temperature=temperature, enable_search=enable_search)
