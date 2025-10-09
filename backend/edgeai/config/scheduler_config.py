"""
任务调度器配置管理
提供可配置的参数和环境变量支持
"""

import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SchedulerConfig:
    """任务调度器配置类"""

    # 并发控制
    MAX_CONCURRENT_TASKS: int = 1

    # 时间间隔配置 (秒)
    QUEUE_CHECK_INTERVAL: int = 10
    TASK_TIMEOUT: int = 3600  # 1小时
    CLEANUP_INTERVAL: int = 300  # 5分钟
    HEARTBEAT_INTERVAL: int = 30  # 心跳间隔

    # 重试配置
    MAX_RETRY_COUNT: int = 3
    RETRY_DELAY_BASE: int = 60  # 基础重试延迟 (秒)
    RETRY_DELAY_MULTIPLIER: float = 2.0  # 延迟倍数

    # 队列配置
    QUEUE_SIZE_LIMIT: int = 100  # 队列最大长度
    PRIORITY_LEVELS: int = 10  # 优先级级别数
    DEFAULT_PRIORITY: int = 5  # 默认优先级

    # 数据库配置
    DB_CONNECTION_TIMEOUT: int = 30
    DB_QUERY_TIMEOUT: int = 60

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: Optional[str] = None
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 5

    # 监控配置
    ENABLE_METRICS: bool = True
    METRICS_EXPORT_INTERVAL: int = 60  # 指标导出间隔
    HEALTH_CHECK_INTERVAL: int = 30  # 健康检查间隔

    # 通知配置
    ENABLE_NOTIFICATIONS: bool = False
    NOTIFICATION_WEBHOOK_URL: Optional[str] = None
    NOTIFICATION_ON_FAILURE: bool = True
    NOTIFICATION_ON_SUCCESS: bool = False

    @classmethod
    def from_env(cls) -> 'SchedulerConfig':
        """从环境变量创建配置"""
        return cls(
            # 并发控制
            MAX_CONCURRENT_TASKS=int(os.getenv('SCHEDULER_MAX_CONCURRENT_TASKS', 1)),

            # 时间间隔配置
            QUEUE_CHECK_INTERVAL=int(os.getenv('SCHEDULER_QUEUE_CHECK_INTERVAL', 10)),
            TASK_TIMEOUT=int(os.getenv('SCHEDULER_TASK_TIMEOUT', 3600)),
            CLEANUP_INTERVAL=int(os.getenv('SCHEDULER_CLEANUP_INTERVAL', 300)),
            HEARTBEAT_INTERVAL=int(os.getenv('SCHEDULER_HEARTBEAT_INTERVAL', 30)),

            # 重试配置
            MAX_RETRY_COUNT=int(os.getenv('SCHEDULER_MAX_RETRY_COUNT', 3)),
            RETRY_DELAY_BASE=int(os.getenv('SCHEDULER_RETRY_DELAY_BASE', 60)),
            RETRY_DELAY_MULTIPLIER=float(os.getenv('SCHEDULER_RETRY_DELAY_MULTIPLIER', 2.0)),

            # 队列配置
            QUEUE_SIZE_LIMIT=int(os.getenv('SCHEDULER_QUEUE_SIZE_LIMIT', 100)),
            PRIORITY_LEVELS=int(os.getenv('SCHEDULER_PRIORITY_LEVELS', 10)),
            DEFAULT_PRIORITY=int(os.getenv('SCHEDULER_DEFAULT_PRIORITY', 5)),

            # 数据库配置
            DB_CONNECTION_TIMEOUT=int(os.getenv('SCHEDULER_DB_CONNECTION_TIMEOUT', 30)),
            DB_QUERY_TIMEOUT=int(os.getenv('SCHEDULER_DB_QUERY_TIMEOUT', 60)),

            # 日志配置
            LOG_LEVEL=os.getenv('SCHEDULER_LOG_LEVEL', 'INFO'),
            LOG_FILE_PATH=os.getenv('SCHEDULER_LOG_FILE_PATH'),
            LOG_MAX_BYTES=int(os.getenv('SCHEDULER_LOG_MAX_BYTES', 10 * 1024 * 1024)),
            LOG_BACKUP_COUNT=int(os.getenv('SCHEDULER_LOG_BACKUP_COUNT', 5)),

            # 监控配置
            ENABLE_METRICS=os.getenv('SCHEDULER_ENABLE_METRICS', 'true').lower() == 'true',
            METRICS_EXPORT_INTERVAL=int(os.getenv('SCHEDULER_METRICS_EXPORT_INTERVAL', 60)),
            HEALTH_CHECK_INTERVAL=int(os.getenv('SCHEDULER_HEALTH_CHECK_INTERVAL', 30)),

            # 通知配置
            ENABLE_NOTIFICATIONS=os.getenv('SCHEDULER_ENABLE_NOTIFICATIONS', 'false').lower() == 'true',
            NOTIFICATION_WEBHOOK_URL=os.getenv('SCHEDULER_NOTIFICATION_WEBHOOK_URL'),
            NOTIFICATION_ON_FAILURE=os.getenv('SCHEDULER_NOTIFICATION_ON_FAILURE', 'true').lower() == 'true',
            NOTIFICATION_ON_SUCCESS=os.getenv('SCHEDULER_NOTIFICATION_ON_SUCCESS', 'false').lower() == 'true',
        )

    def validate(self) -> bool:
        """验证配置的有效性"""
        errors = []

        # 验证数值范围
        if self.MAX_CONCURRENT_TASKS < 1:
            errors.append("MAX_CONCURRENT_TASKS must be >= 1")

        if self.QUEUE_CHECK_INTERVAL < 1:
            errors.append("QUEUE_CHECK_INTERVAL must be >= 1")

        if self.TASK_TIMEOUT < 60:
            errors.append("TASK_TIMEOUT must be >= 60 seconds")

        if self.MAX_RETRY_COUNT < 0:
            errors.append("MAX_RETRY_COUNT must be >= 0")

        if not (1 <= self.DEFAULT_PRIORITY <= self.PRIORITY_LEVELS):
            errors.append(f"DEFAULT_PRIORITY must be between 1 and {self.PRIORITY_LEVELS}")

        # 验证日志级别
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.LOG_LEVEL.upper() not in valid_log_levels:
            errors.append(f"LOG_LEVEL must be one of: {valid_log_levels}")

        # 验证日志文件路径
        if self.LOG_FILE_PATH:
            log_dir = Path(self.LOG_FILE_PATH).parent
            if not log_dir.exists():
                try:
                    log_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    errors.append(f"Cannot create log directory {log_dir}: {e}")

        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")

        return True

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            field.name: getattr(self, field.name)
            for field in self.__dataclass_fields__.values()
        }

    def update_from_dict(self, config_dict: dict) -> None:
        """从字典更新配置"""
        for key, value in config_dict.items():
            if hasattr(self, key):
                # 类型转换
                field_type = self.__dataclass_fields__[key].type
                if field_type == int:
                    value = int(value)
                elif field_type == float:
                    value = float(value)
                elif field_type == bool:
                    value = str(value).lower() in ('true', '1', 'yes', 'on')

                setattr(self, key, value)


class ConfigManager:
    """配置管理器"""

    def __init__(self, config: SchedulerConfig = None):
        self.config = config or SchedulerConfig.from_env()
        self.config.validate()

    def reload_config(self) -> None:
        """重新加载配置"""
        self.config = SchedulerConfig.from_env()
        self.config.validate()

    def update_config(self, **kwargs) -> None:
        """更新配置参数"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)

        self.config.validate()

    def get_config(self) -> SchedulerConfig:
        """获取当前配置"""
        return self.config

    def export_config(self, file_path: str) -> None:
        """导出配置到文件"""
        import json

        config_dict = self.config.to_dict()

        # 转换不可序列化的值
        for key, value in config_dict.items():
            if value is None:
                config_dict[key] = None
            elif isinstance(value, (int, float, str, bool)):
                config_dict[key] = value
            else:
                config_dict[key] = str(value)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)

    def import_config(self, file_path: str) -> None:
        """从文件导入配置"""
        import json

        with open(file_path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)

        self.config.update_from_dict(config_dict)
        self.config.validate()


# 全局配置管理器实例
config_manager = ConfigManager()


def get_config() -> SchedulerConfig:
    """获取全局配置"""
    return config_manager.get_config()


def update_config(**kwargs) -> None:
    """更新全局配置"""
    config_manager.update_config(**kwargs)


def reload_config() -> None:
    """重新加载全局配置"""
    config_manager.reload_config()