"""
DeepSeek AI 公共调用模块
提供统一的 AI 接口调用方法
"""
import os
import logging
from typing import List, Dict, Optional, Any
from openai import OpenAI

logger = logging.getLogger('log')


class DeepSeekClient:
    """DeepSeek AI 客户端封装"""

    def __init__(self):
        """初始化 DeepSeek 客户端"""
        self.api_key = os.environ.get('DEEPSEEK_API_KEY')
        if not self.api_key:
            logger.warning('DEEPSEEK_API_KEY 未在环境变量中配置')

        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com/v1"
        )
        self.model = "deepseek-chat"

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        stream: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        发送聊天请求到 DeepSeek API

        Args:
            messages: 消息列表，格式为 [{"role": "system", "content": "..."}, ...]
            model: 模型名称，默认为 "deepseek-chat"
            temperature: 温度参数，控制随机性，范围 0-2，默认 1.0
            top_p: 核采样参数，默认 1.0
            stream: 是否使用流式输出，默认 False
            **kwargs: 其他参数

        Returns:
            Dict[str, Any]: API 响应结果
            {
                "success": bool,  # 是否成功
                "content": str,   # 返回的内容
                "message": str,   # 消息
                "usage": dict,    # 使用量统计
                "raw_response": dict  # 原始响应
            }

        Raises:
            ValueError: 当 API key 未配置时
            Exception: 当 API 调用失败时
        """
        if not self.api_key:
            logger.error('DEEPSEEK_API_KEY 未配置')
            return {
                "success": False,
                "content": "",
                "message": "DEEPSEEK_API_KEY 未配置",
                "usage": None,
                "raw_response": None
            }

        try:
            logger.info(f'调用 DeepSeek API: model={model or self.model}, messages={len(messages)}')

            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                stream=stream,
                **kwargs
            )

            # 解析响应
            result = {
                "success": True,
                "content": response.choices[0].message.content,
                "message": "调用成功",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0,
                },
                "raw_response": response.model_dump() if hasattr(response, 'model_dump') else str(response)
            }

            logger.info(f'DeepSeek API 调用成功: tokens={result["usage"]["total_tokens"]}')
            return result

        except Exception as e:
            logger.error(f'DeepSeek API 调用失败: {str(e)}')
            return {
                "success": False,
                "content": "",
                "message": f"API 调用失败: {str(e)}",
                "usage": None,
                "raw_response": None
            }

    def chat_simple(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful assistant",
        **kwargs
    ) -> str:
        """
        简化的聊天接口

        Args:
            prompt: 用户提示
            system_prompt: 系统提示，默认为 "You are a helpful assistant"
            **kwargs: 其他传递给 chat 方法的参数

        Returns:
            str: AI 返回的内容，失败时返回空字符串
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        result = self.chat(messages, **kwargs)

        if result["success"]:
            return result["content"]
        else:
            logger.error(f'AI 调用失败: {result["message"]}')
            return ""

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        **kwargs
    ):
        """
        流式聊天接口

        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            top_p: 核采样参数
            **kwargs: 其他参数

        Yields:
            str: 流式返回的文本片段
        """
        if not self.api_key:
            logger.error('DEEPSEEK_API_KEY 未配置')
            yield "[ERROR] DEEPSEEK_API_KEY 未配置"
            return

        try:
            logger.info(f'调用 DeepSeek API (流式): model={model or self.model}')

            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                stream=True,
                **kwargs
            )

            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f'DeepSeek API 流式调用失败: {str(e)}')
            yield f"[ERROR] {str(e)}"


# 创建全局单例实例
_deepseek_client = None


def get_deepseek_client() -> DeepSeekClient:
    """
    获取 DeepSeek 客户端单例

    Returns:
        DeepSeekClient: DeepSeek 客户端实例
    """
    global _deepseek_client
    if _deepseek_client is None:
        _deepseek_client = DeepSeekClient()
    return _deepseek_client


# 便捷函数
def ask_ai(prompt: str, system_prompt: str = "You are a helpful assistant") -> str:
    """
    便捷的 AI 调用函数

    Args:
        prompt: 用户提示
        system_prompt: 系统提示

    Returns:
        str: AI 返回的内容

    Example:
        >>> from utils.ai_client import ask_ai
        >>> response = ask_ai("什么是人工智能？")
        >>> print(response)
    """
    client = get_deepseek_client()
    return client.chat_simple(prompt, system_prompt)


def chat_ai(
    messages: List[Dict[str, str]],
    temperature: float = 1.0,
    stream: bool = False
) -> Dict[str, Any]:
    """
    完整的 AI 聊天函数

    Args:
        messages: 消息列表
        temperature: 温度参数
        stream: 是否流式输出

    Returns:
        Dict[str, Any]: 完整的响应结果

    Example:
        >>> from utils.ai_client import chat_ai
        >>> messages = [
        ...     {"role": "system", "content": "你是一个Python专家"},
        ...     {"role": "user", "content": "如何使用Django？"}
        ... ]
        >>> result = chat_ai(messages)
        >>> if result['success']:
        ...     print(result['content'])
    """
    client = get_deepseek_client()
    return client.chat(messages, temperature=temperature, stream=stream)


def stream_ai(
    messages: List[Dict[str, str]],
    temperature: float = 1.0
):
    """
    流式 AI 聊天函数

    Args:
        messages: 消息列表
        temperature: 温度参数

    Yields:
        str: 流式返回的文本片段

    Example:
        >>> from utils.ai_client import stream_ai
        >>> messages = [{"role": "user", "content": "讲个故事"}]
        >>> for chunk in stream_ai(messages):
        ...     print(chunk, end="", flush=True)
    """
    client = get_deepseek_client()
    yield from client.stream_chat(messages, temperature=temperature)
