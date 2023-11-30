import os

# 日志
LOG_NAME = os.path.basename(os.getcwd())
LOG_PATH = "log/%s.log" % LOG_NAME  # log存储路径
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")  # 日志级别
LOG_COLOR = True  # 是否带有颜色
LOG_IS_WRITE_TO_CONSOLE = True  # 是否打印到控制台
LOG_IS_WRITE_TO_FILE = False  # 是否写文件
LOG_MODE = "w"  # 写文件的模式
LOG_MAX_BYTES = 10 * 1024 * 1024  # 每个日志文件的最大字节数
LOG_BACKUP_COUNT = 20  # 日志文件保留数量
LOG_ENCODING = "utf8"  # 日志文件编码
# 是否详细的打印异常
PRINT_EXCEPTION_DETAILS = True
# 设置不带颜色的日志格式
LOG_FORMAT = "%(threadName)s|%(asctime)s|%(filename)s|%(funcName)s|line:%(lineno)d|%(levelname)s| %(message)s"
# 设置带有颜色的日志格式
os.environ["LOGURU_FORMAT"] = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>line:{line}</cyan> | <level>{message}</level>"
)
OTHERS_LOG_LEVAL = "ERROR"  # 第三方库的log等级