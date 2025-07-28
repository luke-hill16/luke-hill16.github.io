import time
import json
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import redis
from celery import group
from config import Config
from tasks.crawler_tasks import crawl_url, crawl_batch, async_crawl_batch

# 配置日志
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class CrawlerScheduler:
    """分布式爬虫调度器"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            password=Config.REDIS_PASSWORD,
            decode_responses=True
        )
        self.task_queue = Config.TASK_QUEUE_NAME
        self.result_queue = Config.RESULT_QUEUE_NAME
        self.error_queue = Config.ERROR_QUEUE_NAME
    
    def add_url_task(self, url: str, parser_type: str = 'html', extract_rules: Dict = None) -> str:
        """
        添加单个URL爬取任务
        
        Args:
            url: 要爬取的URL
            parser_type: 解析类型
            extract_rules: 提取规则
        
        Returns:
            任务ID
        """
        task_data = {
            'url': url,
            'parser_type': parser_type,
            'extract_rules': extract_rules or {},
            'created_at': datetime.now().isoformat()
        }
        
        # 将任务添加到Redis队列
        task_id = f"task_{int(time.time() * 1000)}"
        self.redis_client.lpush(self.task_queue, json.dumps({
            'task_id': task_id,
            'data': task_data
        }))
        
        logger.info(f"添加任务: {task_id} - {url}")
        return task_id
    
    def add_batch_task(self, urls: List[str], parser_type: str = 'html', extract_rules: Dict = None) -> str:
        """
        添加批量URL爬取任务
        
        Args:
            urls: URL列表
            parser_type: 解析类型
            extract_rules: 提取规则
        
        Returns:
            任务ID
        """
        task_data = {
            'urls': urls,
            'parser_type': parser_type,
            'extract_rules': extract_rules or {},
            'created_at': datetime.now().isoformat()
        }
        
        task_id = f"batch_task_{int(time.time() * 1000)}"
        self.redis_client.lpush(self.task_queue, json.dumps({
            'task_id': task_id,
            'data': task_data,
            'type': 'batch'
        }))
        
        logger.info(f"添加批量任务: {task_id} - {len(urls)} 个URL")
        return task_id
    
    def execute_single_task(self, url: str, parser_type: str = 'html', extract_rules: Dict = None):
        """
        执行单个爬取任务
        
        Args:
            url: 要爬取的URL
            parser_type: 解析类型
            extract_rules: 提取规则
        
        Returns:
            Celery任务结果
        """
        return crawl_url.delay(url, parser_type, extract_rules)
    
    def execute_batch_task(self, urls: List[str], parser_type: str = 'html', extract_rules: Dict = None):
        """
        执行批量爬取任务
        
        Args:
            urls: URL列表
            parser_type: 解析类型
            extract_rules: 提取规则
        
        Returns:
            Celery任务结果
        """
        return crawl_batch.delay(urls, parser_type, extract_rules)
    
    def execute_async_batch_task(self, urls: List[str], parser_type: str = 'html'):
        """
        执行异步批量爬取任务
        
        Args:
            urls: URL列表
            parser_type: 解析类型
        
        Returns:
            Celery任务结果
        """
        return async_crawl_batch.delay(urls, parser_type)
    
    def execute_parallel_tasks(self, urls: List[str], parser_type: str = 'html', extract_rules: Dict = None):
        """
        并行执行多个爬取任务
        
        Args:
            urls: URL列表
            parser_type: 解析类型
            extract_rules: 提取规则
        
        Returns:
            Celery任务组结果
        """
        # 创建任务组
        job = group(crawl_url.s(url, parser_type, extract_rules) for url in urls)
        return job.apply_async()
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
        
        Returns:
            任务状态信息
        """
        try:
            # 从Redis获取任务结果
            result_key = f"task_result:{task_id}"
            result_data = self.redis_client.get(result_key)
            
            if result_data:
                return json.loads(result_data)
            else:
                return {
                    'task_id': task_id,
                    'status': 'pending',
                    'message': '任务正在执行中'
                }
        except Exception as e:
            logger.error(f"获取任务状态失败: {str(e)}")
            return {
                'task_id': task_id,
                'status': 'error',
                'error': str(e)
            }
    
    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """
        获取任务结果
        
        Args:
            task_id: 任务ID
        
        Returns:
            任务结果
        """
        result_key = f"task_result:{task_id}"
        result_data = self.redis_client.get(result_key)
        
        if result_data:
            return json.loads(result_data)
        return None
    
    def save_task_result(self, task_id: str, result: Dict[str, Any]):
        """
        保存任务结果到Redis
        
        Args:
            task_id: 任务ID
            result: 任务结果
        """
        result_key = f"task_result:{task_id}"
        result['task_id'] = task_id
        result['completed_at'] = datetime.now().isoformat()
        
        # 保存结果，设置过期时间
        self.redis_client.setex(
            result_key,
            3600,  # 1小时过期
            json.dumps(result)
        )
        
        logger.info(f"保存任务结果: {task_id}")
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """
        获取待处理任务列表
        
        Returns:
            待处理任务列表
        """
        tasks = []
        while True:
            task_data = self.redis_client.rpop(self.task_queue)
            if not task_data:
                break
            tasks.append(json.loads(task_data))
        return tasks
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """
        获取任务统计信息
        
        Returns:
            统计信息
        """
        stats = {
            'pending_tasks': self.redis_client.llen(self.task_queue),
            'completed_tasks': 0,
            'failed_tasks': 0,
            'total_results': 0
        }
        
        # 统计已完成任务
        for key in self.redis_client.keys("task_result:*"):
            result_data = self.redis_client.get(key)
            if result_data:
                result = json.loads(result_data)
                if result.get('status') == 'success':
                    stats['completed_tasks'] += 1
                else:
                    stats['failed_tasks'] += 1
        
        return stats
    
    def cleanup_expired_results(self, hours: int = 24):
        """
        清理过期的任务结果
        
        Args:
            hours: 过期时间（小时）
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        deleted_count = 0
        
        for key in self.redis_client.keys("task_result:*"):
            result_data = self.redis_client.get(key)
            if result_data:
                result = json.loads(result_data)
                completed_at = datetime.fromisoformat(result.get('completed_at', '1970-01-01T00:00:00'))
                
                if completed_at < cutoff_time:
                    self.redis_client.delete(key)
                    deleted_count += 1
        
        logger.info(f"清理了 {deleted_count} 个过期任务结果")
    
    def monitor_tasks(self, interval: int = 60):
        """
        监控任务执行状态
        
        Args:
            interval: 监控间隔（秒）
        """
        logger.info("开始监控任务执行状态...")
        
        while True:
            try:
                stats = self.get_task_statistics()
                logger.info(f"任务统计: {stats}")
                
                # 处理待处理任务
                pending_tasks = self.get_pending_tasks()
                for task in pending_tasks:
                    task_id = task['task_id']
                    task_data = task['data']
                    
                    if task.get('type') == 'batch':
                        # 批量任务
                        self.execute_batch_task(
                            task_data['urls'],
                            task_data['parser_type'],
                            task_data['extract_rules']
                        )
                    else:
                        # 单个任务
                        self.execute_single_task(
                            task_data['url'],
                            task_data['parser_type'],
                            task_data['extract_rules']
                        )
                
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("停止任务监控")
                break
            except Exception as e:
                logger.error(f"监控任务时出错: {str(e)}")
                time.sleep(interval) 