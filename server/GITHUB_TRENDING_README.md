# GitHub Trending 热榜功能完整实现文档

## 📋 功能概述

本项目实现了完整的 GitHub Trending 热榜功能，包括：
1. **自动数据获取**：每天早上 9 点自动获取 GitHub 热门项目
2. **AI 智能分析**：使用 Google Gemini AI 联网分析每个项目
3. **数据持久化**：将分析结果存储到 PostgreSQL 数据库
4. **Web 展示**：提供美观的前端展示页面

---

## 🗂️ 文件结构

### 后端文件

```
server/
├── apps/system/
│   ├── models.py                              # 数据模型（新增 GithubTrending 表）
│   ├── tasks.py                               # Celery 定时任务（新增 fetch_github_trending）
│   ├── github_trending_views.py               # API 视图（新增）
│   └── urls.py                                # URL 路由（更新）
├── utils/
│   ├── github_trending.py                     # GitHub Trending API 客户端（新增）
│   └── github_analyzer.py                     # AI 分析服务（新增）
└── server/
    └── settings.py                            # Celery Beat 定时配置（更新）
```

### 前端文件

```
client/
├── src/views/github-trending/
│   └── index.vue                               # GitHub Trending 展示页（新增）
└── src/router/index.js                         # 路由配置（更新）
```

---

## 🚀 部署步骤

### 步骤 1: 应用数据库迁移

```bash
cd server
python manage.py migrate
```

### 步骤 2: 启动 Celery Worker 和 Beat

**Windows:**
```bash
# 终端 1: 启动 Celery Worker
celery -A server worker -l info -P solo

# 终端 2: 启动 Celery Beat（定时任务调度器）
celery -A server beat -l info -P solo
```

**Linux/Mac:**
```bash
# 终端 1: 启动 Celery Worker
celery -A server worker -l info

# 终端 2: 启动 Celery Beat
celery -A server beat -l info
```

### 步骤 3: 启动 Django 服务器

```bash
cd server
python manage.py runserver
```

### 步骤 4: 启动前端开发服务器

```bash
cd client
npm run serve
```

---

## 📡 API 接口

### 1. 获取 GitHub Trending 列表

**接口:** `GET /api/github/trending/`

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 否 | 日期 (YYYY-MM-DD 格式，默认今天) |
| language | string | 否 | 编程语言筛选 (python, javascript 等) |
| limit | int | 否 | 返回数量限制 (默认 50) |

**示例:**
```bash
# 获取今天的数据
GET /api/github/trending/

# 获取指定日期的 Python 项目
GET /api/github/trending/?date=2026-01-31&language=python&limit=20
```

**响应:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "author": "huggingface",
      "name": "transformers",
      "full_name": "huggingface/transformers",
      "url": "https://github.com/huggingface/transformers",
      "description": "Transformers: State-of-the-art Machine Learning...",
      "language": "Python",
      "stars": 110543,
      "forks": 23400,
      "current_period_stars": 150,
      "avatar": "https://github.com/huggingface.png",
      "collection_date": "2026-01-31",
      "ai_analysis": {
        "core_features": "最先进的机器学习库...",
        "tech_stack": ["Python", "PyTorch", "TensorFlow"],
        "use_cases": "自然语言处理、计算机视觉...",
        "highlights": [
          "支持多种深度学习框架",
          "预训练模型丰富",
          "社区活跃度高"
        ],
        "recommendation_score": 95,
        "tags": ["python", "machine-learning", "nlp"]
      }
    }
  ],
  "total": 50,
  "date": "2026-01-31"
}
```

### 2. 获取项目详情

**接口:** `GET /api/github/trending/<id>/`

**示例:**
```bash
GET /api/github/trending/1/
```

### 3. 获取统计数据

**接口:** `GET /api/github/trending/stats/`

**参数:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| days | int | 否 | 统计最近几天 (默认 7) |

**示例:**
```bash
GET /api/github/trending/stats/?days=7
```

**响应:**
```json
{
  "success": true,
  "data": {
    "period": {
      "start_date": "2026-01-24",
      "end_date": "2026-01-31",
      "days": 7
    },
    "total_projects": 350,
    "language_stats": {
      "Python": {
        "count": 100,
        "total_stars": 500000,
        "total_current_stars": 5000
      },
      "JavaScript": {
        "count": 120,
        "total_stars": 600000,
        "total_current_stars": 6000
      }
    },
    "date_stats": {
      "2026-01-31": 50,
      "2026-01-30": 45
    }
  }
}
```

### 4. 手动触发任务（需要登录）

**接口:** `POST /api/github/trending/trigger/`

**示例:**
```bash
POST /api/github/trending/trigger/
```

**响应:**
```json
{
  "success": true,
  "message": "任务已触发",
  "task_id": "xxx-xxx-xxx"
}
```

---

## 🎯 前端页面

### 访问地址

- **公开访问**: `http://localhost:8080/github-trending`
- **用户中心**: `http://localhost:8080/user/github-trending` (需要登录)

### 功能特性

1. **日期筛选**: 查看任意日期的热门项目
2. **语言筛选**: 按 Python、JavaScript、Go 等语言筛选
3. **数量限制**: 可选择显示 20/50/100 个项目
4. **AI 分析展示**:
   - 核心功能
   - 技术栈标签
   - 应用场景
   - 亮点特色
   - 推荐指数（0-100分）

### 页面截图说明

每个项目卡片包含：
- 项目基本信息（名称、描述、头像）
- 统计数据（Stars、新增 Stars、Forks）
- AI 智能分析（功能、技术栈、场景、亮点、评分）
- 编程语言标识
- 项目链接

---

## ⚙️ 定时任务配置

### 任务名称
`fetch_github_trending`

### 执行时间
每天早上 9:00（Asia/Shanghai 时区）

### 配置位置
`server/server/settings.py`:
```python
CELERY_BEAT_SCHEDULE = {
    'fetch-github-trending-daily': {
        'task': 'fetch_github_trending',
        'schedule': crontab(hour=9, minute=0),
        'options': {
            'expires': 3600
        }
    },
}
```

### 任务流程

1. **获取数据**：从 GitHub Trending API 获取 6 种编程语言的热门项目
   - Python
   - JavaScript
   - Go
   - Rust
   - Java
   - TypeScript

2. **AI 分析**：使用 Google Gemini AI 联网分析每个项目
   - 访问项目 GitHub 页面
   - 提取关键信息
   - 生成结构化分析报告

3. **数据存储**：将结果保存到 PostgreSQL 数据库
   - 基础信息（作者、项目名、描述等）
   - 统计数据（Stars、Forks 等）
   - AI 分析结果（JSON 格式）

---

## 🗄️ 数据库表结构

### 表名：`system_githubtrending`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| author | varchar(100) | 作者 |
| name | varchar(200) | 项目名称 |
| full_name | varchar(300) | 完整名称 (author/name) |
| url | varchar(500) | 项目地址 |
| description | text | 项目描述 |
| language | varchar(50) | 编程语言 |
| stars | int | Star 数 |
| forks | int | Fork 数 |
| current_period_stars | int | 今日新增 Star |
| avatar | varchar(500) | 作者头像 |
| collection_date | date | 采集日期 |
| since | varchar(20) | 时间范围 (daily/weekly/monthly) |
| ai_analysis | json | AI 分析结果 |
| extra_data | json | 额外数据 |
| create_datetime | datetime | 创建时间 |
| update_datetime | datetime | 更新时间 |
| is_deleted | bool | 是否删除 |

---

## 🔧 手动测试

### 测试 API 接口

```bash
# 获取今天的 Python 热门项目
curl "http://localhost:8000/api/github/trending/?language=python&limit=10"

# 获取统计信息
curl "http://localhost:8000/api/github/trending/stats/?days=7"
```

### 测试定时任务

```python
# 在 Django shell 中测试
cd server
python manage.py shell

from apps.system.tasks import fetch_github_trending
result = fetch_github_trending()
print(result)
```

---

## 📊 监控和日志

### 日志位置
`server/log/` 目录

### 日志级别
- INFO: 正常执行信息
- WARNING: 警告信息（如 API 无数据）
- ERROR: 错误信息（如 API 调用失败）

### 查看日志

```bash
# 实时查看日志
tail -f server/log/celery.log

# 搜索 GitHub Trending 相关日志
grep "GitHub" server/log/celery.log
```

---

## ⚠️ 注意事项

1. **API Key 配置**
   - 确保在 `server/.env` 中配置了 `GOOGLE_API_KEY`
   - AI 分析需要联网功能

2. **Redis 依赖**
   - Celery 需要 Redis 运行
   - 确保 Redis 服务已启动

3. **数据库迁移**
   - 首次部署必须执行 `python manage.py migrate`
   - 迁移文件已生成：`0004_githubtrending_*.py`

4. **定时任务启动**
   - 必须同时启动 Worker 和 Beat
   - Beat 负责调度，Worker 负责执行

5. **API 限制**
   - GitHub Trending API 可能有限制
   - 建议不要频繁手动触发任务

---

## 🎉 功能亮点

✅ **自动化**: 无需人工干预，每天自动获取和分析
✅ **智能分析**: 使用 AI 提供深度的项目分析
✅ **美观界面**: 现代化的用户界面，支持多种筛选
✅ **数据持久**: 所有数据永久保存，支持历史查询
✅ **灵活扩展**: 轻松添加更多编程语言或分析维度

---

**部署完成后，访问**: `http://localhost:8080/github-trending`

**版本**: 1.0.0
**最后更新**: 2026-01-31
