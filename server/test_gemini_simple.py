"""
简单的 Gemini API 测试脚本（不依赖 Django）
"""
import os

# 手动设置环境变量
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCzashUYoV3LNyK5gLDM4HDSZbk2fFo3Gs'

# 导入 Gemini 客户端
from utils.gemini_client import ask_gemini

def test_basic():
    """测试基本调用"""
    print("=" * 50)
    print("测试 1: 基本调用")
    print("=" * 50)

    response = ask_gemini("你好，请用一句话介绍一下你自己")
    print(f"AI 回复: {response}")
    print()


def test_with_search():
    """测试联网搜索"""
    print("=" * 50)
    print("测试 2: 联网搜索")
    print("=" * 50)

    response = ask_gemini(
        "今天北京天气怎么样？",
        enable_search=True
    )
    print(f"AI 回复: {response}")
    print()


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("Gemini API 简单测试")
    print("=" * 50 + "\n")

    print(f"API Key: {os.environ.get('GOOGLE_API_KEY', 'Not set')[:20]}...")
    print()

    test_basic()
    test_with_search()

    print("=" * 50)
    print("测试完成！")
    print("=" * 50)
