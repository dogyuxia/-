# logger_utils.py
import logging
import os
import re
from datetime import datetime
from typing import Optional
from utils.path_tools import get_abs_path

# 日志保存根目录
LOG_ROOT = get_abs_path("logs")
# 确保日志目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

# 日志格式配置（包含时间、模块、行号，便于调试Agent）
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)



def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO,
        file_level: int = logging.DEBUG,
        log_file: Optional[str] = None
) -> logging.Logger:
    """
    获取配置好的日志器（开箱即用）
    :param name: 日志器名称（建议按模块命名，如agent.tools/agent.rag/agent.llm）
    :param console_level: 控制台日志级别（默认INFO，开发时可设为DEBUG）
    :param file_level: 文件日志级别（默认DEBUG，记录详细信息）
    :param log_file: 自定义日志文件名（默认按日期生成：agent_20240121.log）
    :return: 配置完成的Logger对象
    """
    # 1. 创建/获取日志器
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # 全局最低级别


    # 避免重复添加Handler（多次导入时只配置一次）
    if logger.handlers:
        return logger

    # 2. 配置控制台Handler（开发调试用）
    console_handler = logging.StreamHandler()# 控制台Handler
    console_handler.setLevel(console_level)# 日志级别
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)# 日志格式
    logger.addHandler(console_handler)# 添加Handler

    # 3. 配置文件Handler（生产环境留存日志）
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)

    return logger


# 快捷获取默认Agent日志器
logger = get_logger("agent")


if __name__ == '__main__':
    # 测试日志器
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")