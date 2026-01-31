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

分析要求：
1. 项目核心功能：用1-2句话概括项目的主要功能
2. 技术栈：列出项目使用的主要技术和框架
3. 应用场景：说明项目的适用场景和目标用户
4. 亮点特色：总结项目的创新点和优势（2-3条）
5. 推荐指数：根据项目质量、活跃度、star数等给出0-100的评分

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
返回 JSON 格式，包含以下字段：
{{
    "core_features": "项目核心功能（1-2句话）",
    "tech_stack": ["技术1", "技术2", "技术3"],
    "use_cases": "应用场景和目标用户",
    "highlights": ["亮点1", "亮点2", "亮点3"],
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
        return {
            "core_features": project_data.get('description', '暂无描述')[:100] + '...',
            "tech_stack": [project_data.get('language', '未知')] if project_data.get('language') else ["其他"],
            "use_cases": "适用于相关技术栈的开发者和企业",
            "highlights": [
                f"Star 数: {project_data.get('stars', 0)}",
                f"今日新增: {project_data.get('current_period_stars', 0)}",
                f"编程语言: {project_data.get('language', '未知')}"
            ],
            "recommendation_score": min(100, 50 + project_data.get('current_period_stars', 0)),
            "tags": [project_data.get('language', 'unknown'), "github", "trending"],
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
