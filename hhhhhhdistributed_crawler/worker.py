#!/usr/bin/env python3
"""
Celery工作节点启动脚本
用于启动分布式爬虫的工作进程
"""

import os
import sys
import logging
from celery_app import celery_app
from config import Config

# 配置日志
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def start_worker():
    """启动Celery工作节点"""
    try:
        logger.info("启动分布式爬虫工作节点...")
        logger.info(f"Redis连接: {Config.REDIS_HOST}:{Config.REDIS_PORT}")
        logger.info(f"最大工作进程数: {Config.MAX_WORKERS}")
        logger.info(f"最大并发请求数: {Config.MAX_CONCURRENT_REQUESTS}")
        
        # 启动Celery工作节点
        celery_app.worker_main([
            'worker',
            '--loglevel=INFO',
            '--concurrency=' + str(Config.MAX_WORKERS),
            '--queues=crawler_queue',
            '--hostname=worker@%h',
            '--without-gossip',
            '--without-mingle',
            '--without-heartbeat'
        ])
        
    except KeyboardInterrupt:
        logger.info("工作节点停止")
    except Exception as e:
        logger.error(f"启动工作节点失败: {str(e)}")
        sys.exit(1)

def start_beat():
    """启动Celery定时任务调度器"""
    try:
        logger.info("启动定时任务调度器...")
        
        celery_app.worker_main([
            'beat',
            '--loglevel=INFO',
            '--scheduler=celery.beat.PersistentScheduler'
        ])
        
    except KeyboardInterrupt:
        logger.info("定时任务调度器停止")
    except Exception as e:
        logger.error(f"启动定时任务调度器失败: {str(e)}")
        sys.exit(1)

def start_monitor():
    """启动任务监控"""
    try:
        logger.info("启动任务监控...")
        
        from scheduler import CrawlerScheduler
        scheduler = CrawlerScheduler()
        scheduler.monitor_tasks(interval=30)
        
    except KeyboardInterrupt:
        logger.info("任务监控停止")
    except Exception as e:
        logger.error(f"启动任务监控失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='分布式爬虫工作节点')
    parser.add_argument(
        '--mode',
        choices=['worker', 'beat', 'monitor'],
        default='worker',
        help='运行模式: worker(工作节点), beat(定时任务), monitor(监控)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'worker':
        start_worker()
    elif args.mode == 'beat':
        start_beat()
    elif args.mode == 'monitor':
        start_monitor() 