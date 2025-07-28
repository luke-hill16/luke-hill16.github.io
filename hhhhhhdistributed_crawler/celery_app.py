from celery import Celery
from config import Config

# 创建Celery应用
celery_app = Celery(
    'distributed_crawler',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=['tasks.crawler_tasks']
)

# Celery配置
celery_app.conf.update(
    # 任务序列化格式
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    
    # 任务路由
    task_routes={
        'tasks.crawler_tasks.crawl_url': {'queue': 'crawler_queue'},
        'tasks.crawler_tasks.crawl_batch': {'queue': 'crawler_queue'},
    },
    
    # 并发配置
    worker_concurrency=Config.MAX_WORKERS,
    worker_prefetch_multiplier=1,
    
    # 任务执行配置
    task_acks_late=True,
    worker_disable_rate_limits=False,
    
    # 结果配置
    result_expires=3600,  # 结果过期时间1小时
    
    # 重试配置
    task_annotations={
        'tasks.crawler_tasks.crawl_url': {
            'rate_limit': '10/m',  # 每分钟最多10个任务
            'retry_backoff': True,
            'max_retries': Config.MAX_RETRIES,
        }
    }
)

if __name__ == '__main__':
    celery_app.start() 