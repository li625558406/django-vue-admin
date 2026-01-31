# Google Gemini AI 集成文档

## 📋 概述

本项目已经集成了 Google Gemini AI 公共调用模块，提供统一的 AI 接口调用方法，支持 **Google Search 联网搜索** 功能。

---

## 🌟 特色功能

### Google Search 联网搜索

Gemini AI 的核心优势之一是支持实时联网搜索，可以获取最新的信息：

- **实时信息查询**：天气、新闻、股票等动态信息
- **准确的数据支撑**：基于真实搜索结果的回答
- **引用来源**：返回搜索结果链接，便于验证
- **智能触发**：根据问题复杂度自动决定是否搜索

---

## 🚀 快速开始

### 步骤 1: 获取 API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登录 Google 账号
3. 点击 "Create API Key" 创建新的 API Key
4. 复制 API Key

### 步骤 2: 配置 API Key

在 `server/.env` 文件中添加你的 Google API Key：

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 步骤 3: 安装依赖

```bash
cd server
pip install google-generativeai
```

或将 `google-generativeai` 添加到 `requirements.txt`（已完成）：

```
google-generativeai>=0.3.0
```

然后运行：
```bash
pip install -r requirements.txt
```

### 步骤 4: 验证配置

运行示例脚本测试：

```bash
cd server
python utils/gemini_client_example.py
```

---

## 📖 使用方法

### 方式 1: 最简单的调用（推荐用于简单场景）

```python
from utils.gemini_client import ask_gemini

# 直接获取 AI 回复
response = ask_gemini("什么是人工智能？")
print(response)
```

### 方式 2: 启用 Google Search 联网搜索

```python
from utils.gemini_client import ask_gemini

# 查询需要实时信息的问题
response = ask_gemini(
    prompt="今天北京天气怎么样？",
    enable_search=True  # 启用联网搜索
)
print(response)
```

### 方式 3: 自定义系统提示

```python
from utils.gemini_client import ask_gemini

response = ask_gemini(
    prompt="解释什么是Python",
    system_prompt="你是一个编程老师，擅长用简单的语言解释复杂的概念"
)
print(response)
```

### 方式 4: 完整控制（推荐用于复杂场景）

```python
from utils.gemini_client import chat_gemini

messages = [
    {"role": "system", "content": "你是一个Python专家"},
    {"role": "user", "content": "Django是什么？"}
]

result = chat_gemini(messages, temperature=1.0)

if result['success']:
    print(f"AI 回复: {result['content']}")
    print(f"Token 使用: {result['usage']}")
    if result.get('search_results'):
        print(f"搜索结果: {result['search_results']}")
else:
    print(f"调用失败: {result['message']}")
```

### 方式 5: 流式输出

```python
from utils.gemini_client import stream_gemini

messages = [{"role": "user", "content": "讲一个故事"}]

print("AI: ", end="", flush=True)
for chunk in stream_gemini(messages):
    print(chunk, end="", flush=True)
print()
```

### 方式 6: 联网搜索专用接口

```python
from utils.gemini_client import chat_gemini

# 询问需要最新信息的问题
result = chat_gemini(
    messages=[{"role": "user", "content": "2024年最流行的Python框架有哪些？"}],
    enable_search=True  # 启用联网搜索
)

if result['success']:
    print(f"AI 回复: {result['content']}")
    print(f"搜索结果: {result.get('search_results')}")
```

---

## 🎯 在 Django 视图中使用

### 示例 1: 简单聊天接口

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.gemini_client import ask_gemini

class GeminiChatView(APIView):
    """Gemini AI 聊天接口"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt', '')
        system_prompt = request.data.get('system_prompt', 'You are a helpful assistant')
        enable_search = request.data.get('enable_search', False)

        response = ask_gemini(prompt, system_prompt, enable_search=enable_search)

        return Response({
            'success': True,
            'response': response,
            'search_enabled': enable_search
        })
```

### 示例 2: 联网搜索接口

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.gemini_client import chat_gemini

class GeminiSearchView(APIView):
    """Gemini AI 联网搜索接口"""

    def post(self, request):
        query = request.data.get('query', '')

        result = chat_gemini(
            messages=[{"role": "user", "content": query}],
            enable_search=True  # 强制启用联网搜索
        )

        return Response({
            'success': result['success'],
            'content': result.get('content', ''),
            'usage': result.get('usage', {}),
            'search_results': result.get('search_results')
        })
```

### 示例 3: 流式响应（SSE）

```python
# views.py
from django.http import StreamingHttpResponse
from utils.gemini_client import stream_gemini
import json

def gemini_stream_view(request):
    """Gemini AI 流式响应"""
    prompt = request.data.get('prompt', '')
    enable_search = request.data.get('enable_search', False)

    messages = [{"role": "user", "content": prompt}]

    def generate():
        for chunk in stream_gemini(messages, enable_search=enable_search):
            yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\\n\\n"
        yield "data: [DONE]\\n\\n"

    return StreamingHttpResponse(generate(), content_type="text/event-stream")
```

---

## 🔧 API 参考

### `ask_gemini(prompt, system_prompt, enable_search)`

**最简单的 Gemini AI 调用函数**

**参数:**
- `prompt` (str): 用户提示
- `system_prompt` (str): 系统提示，默认为 "You are a helpful assistant"
- `enable_search` (bool): 是否启用 Google Search 联网搜索，默认 False

**返回:**
- `str`: AI 返回的内容，失败时返回空字符串

**示例:**
```python
# 普通调用
response = ask_gemini("你好")

# 启用联网搜索
response = ask_gemini("今天天气怎么样？", enable_search=True)
```

---

### `chat_gemini(messages, temperature, enable_search, stream)`

**完整的 Gemini AI 聊天函数**

**参数:**
- `messages` (List[Dict]): 消息列表
  ```python
  [
      {"role": "system", "content": "系统提示"},
      {"role": "user", "content": "用户消息"},
      {"role": "assistant", "content": "AI 回复"}  # 注意: Gemini 使用 "model" 而非 "assistant"
  ]
  ```
- `temperature` (float): 温度参数，范围 0-2，默认 1.0
- `enable_search` (bool): 是否启用 Google Search，默认 False
- `stream` (bool): 是否流式输出，默认 False

**返回:**
```python
{
    "success": bool,      # 是否成功
    "content": str,       # 返回的内容
    "message": str,       # 消息
    "usage": dict,        # 使用量统计
    "search_results": list or str,  # Google Search 结果（如果启用）
    "raw_response": dict  # 原始响应
}
```

**示例:**
```python
result = chat_gemini(
    messages=[{"role": "user", "content": "你好"}],
    temperature=1.0,
    enable_search=False
)
if result['success']:
    print(result['content'])
```

---

### `stream_gemini(messages, temperature, enable_search)`

**流式 Gemini AI 聊天函数**

**参数:**
- `messages` (List[Dict]): 消息列表
- `temperature` (float): 温度参数，默认 1.0
- `enable_search` (bool): 是否启用 Google Search，默认 False

**返回:**
- 生成器，产生流式文本片段

**示例:**
```python
for chunk in stream_gemini([{"role": "user", "content": "你好"}]):
    print(chunk, end="", flush=True)
```

---

### GeminiClient 类

**底层的客户端类**

```python
from utils.gemini_client import get_gemini_client

client = get_gemini_client()
result = client.chat(messages, enable_search=True)
```

**方法:**
- `chat()`: 发送聊天请求
- `chat_simple()`: 简化的聊天接口
- `stream_chat()`: 流式聊天接口

---

## ⚙️ 参数说明

### Temperature (温度)

控制响应的随机性和多样性：

- `0.0-0.3`: 更确定，适合事实性回答
- `0.4-0.7`: 平衡，适合大多数场景
- `0.8-1.2`: 更有创意，适合创作
- `1.3-2.0`: 非常随机，适合头脑风暴

**示例:**
```python
# 事实性回答
result = chat_gemini(messages, temperature=0.3)

# 创意写作
result = chat_gemini(messages, temperature=1.2)
```

### Google Search 联网搜索

**启用方式:**
```python
# 方式 1: 使用 ask_gemini
response = ask_gemini("今天新闻", enable_search=True)

# 方式 2: 使用 chat_gemini
result = chat_gemini(messages, enable_search=True)
```

**适用场景:**
- 实时信息查询（天气、新闻、股票等）
- 需要最新数据的问题
- 需要引用来源的回答
- 事实性验证

**配置参数:**
```python
# 在 gemini_client.py 中配置
google_search_config = {
    "google_search_retrieval": {
        "dynamic_retrieval_config": {
            "mode": "MODE_DYNAMIC",
            "dynamic_threshold": 0.7  # 置信度阈值
        }
    }
}
```

### Messages 格式

```python
messages = [
    {
        "role": "system",      # 系统角色，设置 AI 的行为
        "content": "你是一个Python专家"
    },
    {
        "role": "user",        # 用户消息
        "content": "如何使用Django？"
    },
    {
        "role": "model",       # AI 的历史回复（用于多轮对话）
        "content": "Django是..."  # 注意: Gemini 使用 "model" 而非 "assistant"
    }
]
```

---

## 🛡️ 错误处理

所有函数都包含完善的错误处理：

```python
from utils.gemini_client import chat_gemini

result = chat_gemini([{"role": "user", "content": "你好"}])

if result['success']:
    print(f"✅ {result['content']}")
else:
    print(f"❌ {result['message']}")
```

**常见错误:**
1. `GOOGLE_API_KEY 未配置` - 检查 `.env` 文件
2. `API 调用失败` - 检查 API Key 是否有效
3. `网络错误` - 检查网络连接
4. `模型初始化失败` - 检查 API 配额和限制

---

## 📊 使用量统计

每次调用会返回 Token 使用量：

```python
result = chat_gemini(messages)
if result['success']:
    print(f"Prompt Tokens: {result['usage']['prompt_tokens']}")
    print(f"Completion Tokens: {result['usage']['completion_tokens']}")
    print(f"Total Tokens: {result['usage']['total_tokens']}")
```

---

## 🧪 测试

运行测试脚本：

```bash
cd server
python utils/gemini_client_example.py
```

或在 Python 交互式环境中测试：

```python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from utils.gemini_client import ask_gemini
print(ask_gemini("你好"))
```

---

## 📝 最佳实践

### 1. 设置合适的系统提示

```python
# ✅ 好的系统提示
system_prompt = "你是一个专业的Python程序员，擅长代码审查和优化"

# ❌ 不好的系统提示
system_prompt = "你好"
```

### 2. 使用多轮对话保持上下文

```python
conversation = [
    {"role": "system", "content": "你是一个Python老师"},
    {"role": "user", "content": "什么是装饰器？"},
    {"role": "model", "content": "装饰器是..."},
    {"role": "user", "content": "能给个例子吗？"}  # 基于前面的对话
]
result = chat_gemini(conversation)
```

### 3. 根据场景决定是否启用联网搜索

```python
# ✅ 适合启用联网搜索的场景
ask_gemini("今天北京天气怎么样？", enable_search=True)
ask_gemini("最新的科技新闻有哪些？", enable_search=True)

# ❌ 不需要联网搜索的场景
ask_gemini("如何用Python实现快速排序？", enable_search=False)
ask_gemini("解释什么是递归", enable_search=False)
```

### 4. 根据场景调整温度

```python
# 代码生成（低温度）
result = chat_gemini(messages, temperature=0.2)

# 创意写作（高温度）
result = chat_gemini(messages, temperature=1.3)
```

### 5. 处理长文本

```python
# 对于长文本，使用流式输出提升用户体验
for chunk in stream_gemini(messages):
    print(chunk, end="", flush=True)
```

---

## 🆚 DeepSeek vs Gemini

本项目同时集成了 DeepSeek 和 Gemini 两个 AI 提供商：

| 特性 | DeepSeek | Gemini |
|------|----------|--------|
| **主要优势** | 性价比高，中文能力强 | 支持联网搜索，多模态 |
| **适用场景** | 通用对话，代码生成 | 实时信息，事实查询 |
| **联网能力** | ❌ 不支持 | ✅ 支持 |
| **模块** | `utils.ai_client` | `utils.gemini_client` |
| **API Key** | `DEEPSEEK_API_KEY` | `GOOGLE_API_KEY` |

**建议:**
- 通用对话、代码生成 → 使用 DeepSeek
- 实时信息、新闻查询 → 使用 Gemini（启用搜索）
- 同时使用两个 AI，根据场景选择

---

## 🔗 相关链接

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API 文档](https://ai.google.dev/gemini-api/docs)
- [Python SDK GitHub](https://github.com/google/generative-ai-python)
- [API Key 获取](https://aistudio.google.com/app/apikey)

---

## 💡 常见问题

### Q: 如何检查 API Key 是否配置成功？

```python
import os
print(os.environ.get('GOOGLE_API_KEY'))
```

### Q: 如何查看日志？

```python
import logging
logger = logging.getLogger('log')
# Gemini AI 调用的日志会输出到 Django 日志中
```

### Q: 支持流式响应吗？

支持，使用 `stream_gemini()` 函数或在 `chat_gemini()` 中设置 `stream=True`。

### Q: 联网搜索会额外收费吗？

Google Search 功能是 Gemini API 的一部分，具体计费请参考 [Google AI 定价](https://ai.google.dev/pricing)。

### Q: 如何同时使用 DeepSeek 和 Gemini？

```python
from utils.ai_client import ask_ai
from utils.gemini_client import ask_gemini

# 根据场景选择
def get_ai_response(prompt, need_search=False):
    if need_search:
        return ask_gemini(prompt, enable_search=True)
    else:
        return ask_ai(prompt)
```

---

## 📂 文件结构

```
server/
├── .env                           # 环境变量配置（包含 API Keys）
├── requirements.txt                # Python 依赖（已添加 google-generativeai）
├── utils/
│   ├── gemini_client.py           # Gemini AI 客户端模块
│   └── gemini_client_example.py   # 使用示例
├── apps/
│   └── system/
│       ├── gemini_views.py        # Gemini Django 视图示例
│       └── ai_views.py            # DeepSeek Django 视图示例
├── AI_INTEGRATION.md              # DeepSeek 集成文档
└── GEMINI_INTEGRATION.md          # Gemini 集成文档（本文档）
```

---

## 🎯 完整示例

### 场景：智能问答助手

```python
from utils.ai_client import ask_ai
from utils.gemini_client import ask_gemini

class SmartAssistant:
    """智能问答助手，根据问题类型选择合适的 AI"""

    def answer(self, question: str) -> str:
        # 判断是否需要实时信息
        keywords = ['天气', '新闻', '最新', '今天', '股票', '汇率']
        need_search = any(kw in question for kw in keywords)

        if need_search:
            # 使用 Gemini + 联网搜索
            return ask_gemini(
                question,
                system_prompt="你是一个专业的实时信息查询助手",
                enable_search=True
            )
        else:
            # 使用 DeepSeek（性价比更高）
            return ask_ai(
                question,
                system_prompt="你是一个专业的知识问答助手"
            )

# 使用示例
assistant = SmartAssistant()
print(assistant.answer("今天北京天气怎么样？"))  # 使用 Gemini
print(assistant.answer("如何用Python实现快速排序？"))  # 使用 DeepSeek
```

---

**最后更新**: 2026-01-31
**版本**: 1.0.0
