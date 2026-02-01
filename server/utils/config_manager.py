"""
系统配置管理工具
从数据字典读取系统配置，支持缓存和环境变量 fallback
"""
import os
import logging
from typing import Optional
from django.core.cache import cache
from apps.system.models import Dict, DictType

logger = logging.getLogger('log')


class ConfigManager:
    """配置管理器，从数据字典读取配置"""

    # 缓存时间（秒），默认 1 小时
    CACHE_TIMEOUT = 3600

    # 系统配置的字典类型代码
    SYSTEM_CONFIG_TYPE_CODE = 'system_config'

    @classmethod
    def get(cls, key: str, default: Optional[str] = None, use_env_fallback: bool = True) -> Optional[str]:
        """
        获取配置值

        Args:
            key: 配置键（字典的 code 字段）
            default: 默认值
            use_env_fallback: 如果数据字典中没有找到，是否从环境变量读取

        Returns:
            str: 配置值，如果找不到则返回默认值
        """
        # 1. 先尝试从缓存读取
        cache_key = f'system_config:{key}'
        cached_value = cache.get(cache_key)
        if cached_value is not None:
            return cached_value

        # 2. 从数据字典读取
        try:
            # 获取系统配置字典类型
            dict_type = DictType.objects.filter(code=cls.SYSTEM_CONFIG_TYPE_CODE).first()

            if dict_type:
                # 查找对应的配置项（使用 code 字段匹配）
                config_dict = Dict.objects.filter(
                    type=dict_type,
                    code=key,
                    is_used=True
                ).first()

                if config_dict:
                    # 使用 description 字段存储配置值（因为 description 是 TextField，适合存储较长的值）
                    value = config_dict.description

                    # 缓存配置值
                    cache.set(cache_key, value, cls.CACHE_TIMEOUT)

                    logger.info(f'从数据字典读取配置: {key}')
                    return value

        except Exception as e:
            logger.warning(f'从数据字典读取配置失败: {key}, 错误: {str(e)}')

        # 3. 如果数据字典中没有，尝试从环境变量读取
        if use_env_fallback:
            env_value = os.environ.get(key)
            if env_value is not None:
                logger.info(f'从环境变量读取配置: {key}')
                # 也缓存环境变量的值，避免重复读取
                cache.set(cache_key, env_value, cls.CACHE_TIMEOUT)
                return env_value

        # 4. 返回默认值
        return default

    @classmethod
    def get_deepseek_api_key(cls) -> Optional[str]:
        """
        获取 DeepSeek API Key

        Returns:
            str: DeepSeek API Key
        """
        return cls.get('DEEPSEEK_API_KEY', use_env_fallback=True)

    @classmethod
    def get_google_api_key(cls) -> Optional[str]:
        """
        获取 Google API Key

        Returns:
            str: Google API Key
        """
        return cls.get('GOOGLE_API_KEY', use_env_fallback=True)

    @classmethod
    def clear_cache(cls, key: Optional[str] = None):
        """
        清除配置缓存

        Args:
            key: 配置键，如果为 None 则清除所有配置缓存
        """
        if key:
            cache_key = f'system_config:{key}'
            cache.delete(cache_key)
            logger.info(f'已清除配置缓存: {key}')
        else:
            # 清除所有 system_config 相关的缓存
            # 注意：Django 的 cache 不支持模式匹配删除，这里只能通过其他方式实现
            # 简单做法：清除所有缓存
            cache.clear()
            logger.info('已清除所有配置缓存')

    @classmethod
    def refresh_config(cls, key: str) -> Optional[str]:
        """
        刷新配置（清除缓存后重新读取）

        Args:
            key: 配置键

        Returns:
            str: 配置值
        """
        cls.clear_cache(key)
        return cls.get(key, use_env_fallback=True)


# 创建便捷函数
def get_config(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    获取配置值的便捷函数

    Args:
        key: 配置键
        default: 默认值

    Returns:
        str: 配置值

    Example:
        >>> from utils.config_manager import get_config
        >>> api_key = get_config('DEEPSEEK_API_KEY')
        >>> print(api_key)
    """
    return ConfigManager.get(key, default=default)


def get_deepseek_api_key() -> Optional[str]:
    """获取 DeepSeek API Key"""
    return ConfigManager.get_deepseek_api_key()


def get_google_api_key() -> Optional[str]:
    """获取 Google API Key"""
    return ConfigManager.get_google_api_key()
