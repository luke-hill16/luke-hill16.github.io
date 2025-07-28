import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Redis配置
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    
    # Celery配置
    CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    # 数据库配置
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB = os.getenv('MONGODB_DB', 'crawler_db')
    
    # MySQL配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'crawler_db')
    
    # 爬虫配置
    CRAWLER_DELAY = float(os.getenv('CRAWLER_DELAY', 1.0))  # 请求间隔
    CRAWLER_TIMEOUT = int(os.getenv('CRAWLER_TIMEOUT', 30))  # 请求超时
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))  # 最大重试次数
    
    # 并发配置
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', 4))  # 最大工作进程数
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', 16))  # 最大并发请求数
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'crawler.log')
    
    # 代理配置
    USE_PROXY = os.getenv('USE_PROXY', 'false').lower() == 'true'
    PROXY_LIST = os.getenv('PROXY_LIST', '').split(',') if os.getenv('PROXY_LIST') else []
    
    # 用户代理配置
    USER_AGENT_ROTATION = os.getenv('USER_AGENT_ROTATION', 'true').lower() == 'true'
    
    # 任务队列配置
    TASK_QUEUE_NAME = 'crawler_tasks'
    RESULT_QUEUE_NAME = 'crawler_results'
    ERROR_QUEUE_NAME = 'crawler_errors' 