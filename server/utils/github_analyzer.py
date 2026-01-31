"""
GitHub Trending AI 分析服务
使用 Google Gemini AI 分析 GitHub 热门项目
"""
import logging
from typing import Dict, List
from utils.gemini_client import ask_gemini, chat_gemini

logger = logging.getLogger('log')


class GithubTrendingAnalyzer:
    """GitHub Trending AI 分析器"""

    def __init__(self):
        """初始化分析器"""
        self.system_prompt = """
你是一个专业的技术分析师，擅长分析 GitHub 开源项目。
请对给定的 GitHub 项目进行深入分析，并返回特定格式的 JSON 数据。

重要要求：
- 所有分析内容必须使用中文
- 项目名称要有中文标题
- 核心功能要有详细的中文介绍
- 技术栈要使用中文描述
- 应用场景要用中文说明
- 亮点特色要用中文列举

分析要求：
1. 项目标题：为项目起一个简洁的中文标题（不超过10个字）
2. 项目简介：用2-3句话详细介绍项目的主要功能和价值
3. 核心功能：列出项目的主要功能点
4. 技术栈：列出项目使用的主要技术和框架（中文描述）
5. 应用场景：说明项目的适用场景和目标用户
6. 亮点特色：总结项目的创新点和优势（3-4条）
7. 推荐指数：根据项目质量、活跃度、star数等给出0-100的评分

返回格式要求：
必须返回有效的 JSON 格式，不要有任何额外的文字说明。
"""

    def analyze_project(self, project_data: Dict) -> Dict:
        """
        分析单个 GitHub 项目

        Args:
            project_data: 项目数据

        Returns:
            Dict: AI 分析结果
        """
        # 构建分析提示
        prompt = f"""
请分析以下 GitHub 项目：

项目名称：{project_data.get('full_name', '')}
项目描述：{project_data.get('description', '暂无描述')}
项目地址：{project_data.get('url', '')}
编程语言：{project_data.get('language', '未知')}
Star 数：{project_data.get('stars', 0)}
今日新增 Star：{project_data.get('current_period_stars', 0)}

请使用联网搜索功能，获取该项目的最新信息和详细情况。
**重要**：所有内容必须使用中文！

返回 JSON 格式，包含以下字段：
{{
    "title": "项目的中文标题（不超过10个字）",
    "summary": "项目的中文简介（2-3句话详细介绍）",
    "core_features": "项目核心功能（中文描述）",
    "tech_stack": ["技术1（中文）", "技术2（中文）", "技术3（中文）"],
    "use_cases": "应用场景和目标用户（中文）",
    "highlights": ["亮点1（中文）", "亮点2（中文）", "亮点3（中文）", "亮点4（中文）"],
    "recommendation_score": 85,
    "tags": ["标签1", "标签2", "标签3"]
}}
"""

        try:
            # 调用 Gemini AI，启用联网搜索
            response = ask_gemini(prompt, enable_search=True)

            # 尝试解析 JSON
            import json
            try:
                # 清理可能的 markdown 代码块标记
                cleaned_response = response.strip()
                if cleaned_response.startswith('```'):
                    cleaned_response = cleaned_response.split('```')[1]
                    if cleaned_response.startswith('json'):
                        cleaned_response = cleaned_response[4:]
                    cleaned_response = cleaned_response.strip()

                analysis = json.loads(cleaned_response)

                logger.info(f"成功分析项目: {project_data.get('full_name', '')}")
                return analysis

            except json.JSONDecodeError:
                # 如果 JSON 解析失败，返回结构化的默认数据
                logger.warning(f"JSON 解析失败: {project_data.get('full_name', '')}")
                return self._get_default_analysis(project_data, response)

        except Exception as e:
            logger.error(f"分析项目失败 {project_data.get('full_name', '')}: {str(e)}")
            return self._get_default_analysis(project_data, str(e))

    def _get_default_analysis(self, project_data: Dict, error_msg: str = None) -> Dict:
        """
        获取默认的分析结果（当 AI 分析失败时）

        Args:
            project_data: 项目数据
            error_msg: 错误信息

        Returns:
            Dict: 默认分析结果
        """
        full_name = project_data.get('full_name', '未知项目')
        description = project_data.get('description', '暂无描述')
        language = project_data.get('language', '未知')

        # 生成简单的中文标题
        title = f"{language}开源项目" if language and language != '未知' else "热门开源项目"

        return {
            "title": title,
            "summary": f"{full_name} 是一个优秀的开源项目。{description[:100] if description else '暂无详细描述'}",
            "core_features": description[:100] + '...' if len(description) > 100 else description,
            "tech_stack": [language] if language else ["其他"],
            "use_cases": "适用于相关技术栈的开发者和企业",
            "highlights": [
                f"Star 数: {project_data.get('stars', 0)}",
                f"今日新增: {project_data.get('current_period_stars', 0)}",
                f"编程语言: {language}",
                "GitHub 热门项目"
            ],
            "recommendation_score": min(100, 50 + project_data.get('current_period_stars', 0)),
            "tags": [language, "github", "trending"],
            "error": error_msg
        }

    def analyze_batch(self, projects: List[Dict]) -> List[Dict]:
        """
        批量分析项目

        Args:
            projects: 项目列表

        Returns:
            List[Dict]: 分析结果列表
        """
        results = []

        for i, project in enumerate(projects):
            logger.info(f"正在分析第 {i+1}/{len(projects)} 个项目...")

            analysis = self.analyze_project(project)
            results.append(analysis)

        return results


# 全局实例
github_analyzer = GithubTrendingAnalyzer()


def analyze_github_project(project_data: Dict) -> Dict:
    """
    分析 GitHub 项目（便捷函数）

    Args:
        project_data: 项目数据

    Returns:
        Dict: AI 分析结果
    """
    return github_analyzer.analyze_project(project_data)
