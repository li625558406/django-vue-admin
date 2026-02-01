"""
初始化系统配置数据字典的管理命令
用于在数据字典中创建系统配置类型和 API Key 配置项
"""
from django.core.management.base import BaseCommand
from apps.system.models import DictType, Dict
import os


class Command(BaseCommand):
    help = '初始化系统配置数据字典，创建 API Key 等配置项'

    def handle(self, *args, **options):
        """执行命令"""
        self.stdout.write(self.style.SUCCESS('开始初始化系统配置...'))

        # 1. 创建系统配置字典类型
        dict_type, created = DictType.objects.get_or_create(
            code='system_config',
            defaults={
                'name': '系统配置',
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ 创建字典类型: {dict_type.name} ({dict_type.code})'))
        else:
            self.stdout.write(self.style.WARNING(f'× 字典类型已存在: {dict_type.name} ({dict_type.code})'))

        # 2. 创建 DeepSeek API Key 配置项
        deepseek_dict, created = Dict.objects.get_or_create(
            type=dict_type,
            code='DEEPSEEK_API_KEY',
            defaults={
                'name': 'DeepSeek API Key',
                'description': os.environ.get('DEEPSEEK_API_KEY', ''),
                'sort': 1,
                'is_used': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ 创建配置项: {deepseek_dict.name}'))
            if deepseek_dict.description:
                self.stdout.write(self.style.SUCCESS(f'  值: {deepseek_dict.description[:20]}...'))
            else:
                self.stdout.write(self.style.WARNING(f'  警告: 环境变量中未找到 DEEPSEEK_API_KEY'))
        else:
            self.stdout.write(self.style.WARNING(f'× 配置项已存在: {deepseek_dict.name}'))
            # 如果环境变量中有值，询问是否更新
            env_value = os.environ.get('DEEPSEEK_API_KEY', '')
            if env_value and env_value != deepseek_dict.description:
                self.stdout.write(self.style.WARNING(f'  提示: 环境变量中的值与数据字典不同'))
                self.stdout.write(self.style.WARNING(f'  数据字典: {deepseek_dict.description[:20] if deepseek_dict.description else "空"}...'))
                self.stdout.write(self.style.WARNING(f'  环境变量: {env_value[:20]}...'))

        # 3. 创建 Google API Key 配置项
        google_dict, created = Dict.objects.get_or_create(
            type=dict_type,
            code='GOOGLE_API_KEY',
            defaults={
                'name': 'Google API Key',
                'description': os.environ.get('GOOGLE_API_KEY', ''),
                'sort': 2,
                'is_used': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ 创建配置项: {google_dict.name}'))
            if google_dict.description:
                self.stdout.write(self.style.SUCCESS(f'  值: {google_dict.description[:20]}...'))
            else:
                self.stdout.write(self.style.WARNING(f'  警告: 环境变量中未找到 GOOGLE_API_KEY'))
        else:
            self.stdout.write(self.style.WARNING(f'× 配置项已存在: {google_dict.name}'))
            # 如果环境变量中有值，询问是否更新
            env_value = os.environ.get('GOOGLE_API_KEY', '')
            if env_value and env_value != google_dict.description:
                self.stdout.write(self.style.WARNING(f'  提示: 环境变量中的值与数据字典不同'))
                self.stdout.write(self.style.WARNING(f'  数据字典: {google_dict.description[:20] if google_dict.description else "空"}...'))
                self.stdout.write(self.style.WARNING(f'  环境变量: {env_value[:20]}...'))

        self.stdout.write(self.style.SUCCESS('\n系统配置初始化完成！'))
        self.stdout.write(self.style.SUCCESS('您现在可以通过前端数据字典管理界面修改这些配置项'))
