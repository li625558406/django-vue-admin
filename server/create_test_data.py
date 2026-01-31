"""
创建 GitHub Trending 测试数据
用于前端展示效果演示
"""
import os
import sys
import django
from datetime import date

# 设置 Django 环境
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from apps.system.models import GithubTrending

# 测试数据
test_projects = [
    {
        "author": "huggingface",
        "name": "transformers",
        "full_name": "huggingface/transformers",
        "url": "https://github.com/huggingface/transformers",
        "description": "Transformers: State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX. Provides thousands of pre-trained models to perform tasks on different modalities.",
        "language": "Python",
        "stars": 125000,
        "forks": 25000,
        "current_period_stars": 150,
        "avatar": "https://github.com/huggingface.png",
        "ai_analysis": {
            "core_features": "最先进的机器学习库，提供数千个预训练模型，支持文本、视觉、音频等多模态任务",
            "tech_stack": ["Python", "PyTorch", "TensorFlow", "JAX"],
            "use_cases": "自然语言处理、计算机视觉、语音识别、文本生成、问答系统等",
            "highlights": [
                "提供 100,000+ 预训练模型",
                "支持多种深度学习框架",
                "活跃的社区和完善的文档",
                "企业级生产就绪"
            ],
            "recommendation_score": 98,
            "tags": ["python", "machine-learning", "nlp", "deep-learning", "pytorch"]
        }
    },
    {
        "author": "vercel",
        "name": "next.js",
        "full_name": "vercel/next.js",
        "url": "https://github.com/vercel/next.js",
        "description": "The React Framework for the Web. Used by some of the world's largest companies. Enables you to build full-stack Web applications.",
        "language": "JavaScript",
        "stars": 115000,
        "forks": 24000,
        "current_period_stars": 120,
        "avatar": "https://github.com/vercel.png",
        "ai_analysis": {
            "core_features": "React 全栈框架，支持 SSR、SSG、API Routes，提供优秀的开发体验和性能",
            "tech_stack": ["JavaScript", "React", "TypeScript", "Node.js"],
            "use_cases": "企业官网、电商网站、博客平台、SaaS 应用、全栈 Web 应用",
            "highlights": [
                "零配置部署到 Vercel",
                "内置图片优化和字体优化",
                "支持多种渲染模式",
                "优秀的性能和 SEO"
            ],
            "recommendation_score": 96,
            "tags": ["javascript", "react", "web", "framework", "ssr"]
        }
    },
    {
        "author": "golang",
        "name": "go",
        "full_name": "golang/go",
        "url": "https://github.com/golang/go",
        "description": "The Go programming language. Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.",
        "language": "Go",
        "stars": 115000,
        "forks": 17000,
        "current_period_stars": 85,
        "avatar": "https://github.com/golang.png",
        "ai_analysis": {
            "core_features": "Google 开发的静态类型编程语言，专注于简洁、高效和并发",
            "tech_stack": ["Go", "C", "Assembly"],
            "use_cases": "云原生应用、微服务、网络服务、DevOps 工具、分布式系统",
            "highlights": [
                "内置并发支持（goroutines 和 channels）",
                "快速的编译速度",
                "简洁的语法和强大的标准库",
                "优秀的性能和内存占用"
            ],
            "recommendation_score": 94,
            "tags": ["go", "programming-language", "concurrent", "cloud-native"]
        }
    },
    {
        "author": "rust-lang",
        "name": "rust",
        "full_name": "rust-lang/rust",
        "url": "https://github.com/rust-lang/rust",
        "description": "Empowering everyone to build reliable and efficient software. Rust is a systems programming language that runs blazingly fast, prevents segfaults, and guarantees thread safety.",
        "language": "Rust",
        "stars": 88000,
        "forks": 11000,
        "current_period_stars": 95,
        "avatar": "https://github.com/rust-lang.png",
        "ai_analysis": {
            "core_features": "现代系统编程语言，专注于安全、并发和性能，无 GC 且内存安全",
            "tech_stack": ["Rust", "C++", "LLVM"],
            "use_cases": "系统编程、WebAssembly、嵌入式开发、区块链、CLI 工具",
            "highlights": [
                "编译时内存安全保证",
                "零成本抽象",
                "优秀的并发支持",
                "现代化的包管理器 Cargo"
            ],
            "recommendation_score": 95,
            "tags": ["rust", "systems-programming", "memory-safe", "webassembly"]
        }
    },
    {
        "author": "microsoft",
        "name": "TypeScript",
        "full_name": "microsoft/TypeScript",
        "url": "https://github.com/microsoft/TypeScript",
        "description": "TypeScript is a superset of JavaScript that compiles to clean JavaScript output. It adds static typing, classes, and interfaces to JavaScript.",
        "language": "TypeScript",
        "stars": 97000,
        "forks": 12000,
        "current_period_stars": 75,
        "avatar": "https://github.com/microsoft.png",
        "ai_analysis": {
            "core_features": "JavaScript 的超集，添加静态类型系统、类和接口，编译为纯 JavaScript",
            "tech_stack": ["TypeScript", "JavaScript", "Node.js"],
            "use_cases": "大型 Web 应用、企业级项目、全栈开发、库和框架开发",
            "highlights": [
                "优秀的 IDE 支持（VS Code、IntelliJ）",
                "静态类型检查减少 bug",
                "渐进式采用",
                "活跃的社区和生态系统"
            ],
            "recommendation_score": 93,
            "tags": ["typescript", "javascript", "web", "static-typing"]
        }
    },
    {
        "author": "openai",
        "name": "tiktoken",
        "full_name": "openai/tiktoken",
        "url": "https://github.com/openai/tiktoken",
        "description": "tiktoken is a fast BPE tokeniser for use with OpenAI's models. Supports GPT-4, GPT-3.5, and GPT-2.",
        "language": "Python",
        "stars": 18000,
        "forks": 1200,
        "current_period_stars": 220,
        "avatar": "https://github.com/openai.png",
        "ai_analysis": {
            "core_features": "OpenAI 官方的 BPE 分词器，用于 GPT 模型的 token 计算，高性能且易用",
            "tech_stack": ["Python", "C++", "Rust"],
            "use_cases": "LLM 应用开发、Token 计数优化、成本控制、文本处理",
            "highlights": [
                "官方支持，准确可靠",
                "超快的分词速度",
                "支持所有 GPT 模型",
                "简单的 API 设计"
            ],
            "recommendation_score": 91,
            "tags": ["python", "openai", "gpt", "llm", "tokenizer"]
        }
    },
    {
        "author": "langchain-ai",
        "name": "langchain",
        "full_name": "langchain-ai/langchain",
        "url": "https://github.com/langchain-ai/langchain",
        "description": "Building applications with LLMs through composability. The most popular framework for building LLM applications.",
        "language": "Python",
        "stars": 82000,
        "forks": 12000,
        "current_period_stars": 280,
        "avatar": "https://github.com/langchain-ai.png",
        "ai_analysis": {
            "core_features": "最流行的 LLM 应用开发框架，提供链式调用、代理、记忆管理等组件",
            "tech_stack": ["Python", "TypeScript", "LangChain"],
            "use_cases": "AI 应用开发、RAG 系统、智能代理、问答系统、文档分析",
            "highlights": [
                "丰富的集成（100+ 模型和工具）",
                "灵活的链式和代理机制",
                "活跃的社区和文档",
                "支持多种 LLM 提供商"
            ],
            "recommendation_score": 92,
            "tags": ["python", "llm", "ai", "langchain", "rag"]
        }
    },
    {
        "author": "facebook",
        "name": "react",
        "full_name": "facebook/react",
        "url": "https://github.com/facebook/react",
        "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
        "language": "JavaScript",
        "stars": 220000,
        "forks": 45000,
        "current_period_stars": 180,
        "avatar": "https://github.com/facebook.png",
        "ai_analysis": {
            "core_features": "Meta 开发的声明式 JavaScript 库，用于构建用户界面，组件化和虚拟 DOM",
            "tech_stack": ["JavaScript", "React", "TypeScript"],
            "use_cases": "单页应用、移动应用、桌面应用、组件库开发",
            "highlights": [
                "庞大的生态系统",
                "组件化开发模式",
                "虚拟 DOM 提升性能",
                "Hooks 和并发模式"
            ],
            "recommendation_score": 97,
            "tags": ["javascript", "react", "frontend", "ui", "library"]
        }
    }
]

if __name__ == '__main__':
    print("=" * 50)
    print("开始创建 GitHub Trending 测试数据")
    print("=" * 50)
    print()

    collection_date = date.today()
    created_count = 0

    for project in test_projects:
        # 检查是否已存在
        exists = GithubTrending.objects.filter(
            collection_date=collection_date,
            full_name=project['full_name']
        ).exists()

        if exists:
            print(f"[SKIP] Already exists: {project['full_name']}")
            continue

        # 创建记录
        GithubTrending.objects.create(
            author=project['author'],
            name=project['name'],
            full_name=project['full_name'],
            url=project['url'],
            description=project['description'],
            language=project['language'],
            stars=project['stars'],
            forks=project['forks'],
            current_period_stars=project['current_period_stars'],
            avatar=project['avatar'],
            collection_date=collection_date,
            since='daily',
            ai_analysis=project['ai_analysis'],
            extra_data={}
        )
        created_count += 1
        print(f"[OK] Created: {project['full_name']} ({project['language']})")

    print()
    print("=" * 50)
    print(f"Done! Created {created_count} records")
    print(f"Total records in DB: {GithubTrending.objects.filter(is_deleted=False).count()}")
    print("=" * 50)
    print()
    print("Now you can visit:")
    print("   http://localhost:8080/github-trending")
    print("=" * 50)
