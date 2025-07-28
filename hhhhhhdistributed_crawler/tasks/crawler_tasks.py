import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from celery import current_task
from fake_useragent import UserAgent
import logging
import time
import json
from typing import Dict, List, Any
from urllib.parse import urljoin, urlparse
import redis
from config import Config

# 配置日志
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# 创建Redis连接
redis_client = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=Config.REDIS_DB,
    password=Config.REDIS_PASSWORD,
    decode_responses=True
)

# 创建用户代理生成器
ua = UserAgent()

class CrawlerTask:
    """爬虫任务基类"""
    
    def __init__(self):
        self.session = None
        self.proxy_pool = Config.PROXY_LIST if Config.USE_PROXY else []
        self.current_proxy_index = 0
    
    def get_user_agent(self):
        """获取随机用户代理"""
        if Config.USER_AGENT_ROTATION:
            return ua.random
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    
    def get_proxy(self):
        """获取代理"""
        if not self.proxy_pool:
            return None
        proxy = self.proxy_pool[self.current_proxy_index % len(self.proxy_pool)]
        self.current_proxy_index += 1
        return {'http': proxy, 'https': proxy}
    
    def update_progress(self, progress: int, message: str = ""):
        """更新任务进度"""
        if current_task:
            current_task.update_state(
                state='PROGRESS',
                meta={'progress': progress, 'message': message}
            )

def crawl_url_task(url: str, parser_type: str = 'html', extract_rules: Dict = None) -> Dict[str, Any]:
    """
    单个URL爬取任务
    
    Args:
        url: 要爬取的URL
        parser_type: 解析类型 ('html', 'json', 'xml')
        extract_rules: 提取规则
    
    Returns:
        爬取结果字典
    """
    crawler = CrawlerTask()
    result = {
        'url': url,
        'status': 'failed',
        'data': None,
        'error': None,
        'timestamp': time.time()
    }
    
    try:
        # 更新进度
        crawler.update_progress(10, f"开始爬取: {url}")
        
        # 发送请求
        headers = {
            'User-Agent': crawler.get_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        proxies = crawler.get_proxy()
        
        crawler.update_progress(30, "发送HTTP请求...")
        
        response = requests.get(
            url,
            headers=headers,
            proxies=proxies,
            timeout=Config.CRAWLER_TIMEOUT,
            verify=False
        )
        
        crawler.update_progress(60, "解析响应内容...")
        
        # 检查响应状态
        if response.status_code != 200:
            result['error'] = f"HTTP错误: {response.status_code}"
            return result
        
        # 根据解析类型处理内容
        if parser_type == 'html':
            soup = BeautifulSoup(response.content, 'html.parser')
            if extract_rules:
                data = extract_data_from_html(soup, extract_rules)
            else:
                data = {
                    'title': soup.title.string if soup.title else '',
                    'text': soup.get_text()[:1000],  # 限制文本长度
                    'links': [a.get('href') for a in soup.find_all('a', href=True)]
                }
        elif parser_type == 'json':
            data = response.json()
        else:
            data = response.text
        
        crawler.update_progress(90, "保存结果...")
        
        # 保存到Redis
        result_key = f"crawl_result:{hash(url)}"
        redis_client.setex(
            result_key,
            3600,  # 1小时过期
            json.dumps({
                'url': url,
                'data': data,
                'timestamp': time.time()
            })
        )
        
        result['status'] = 'success'
        result['data'] = data
        
        crawler.update_progress(100, "爬取完成")
        
    except Exception as e:
        logger.error(f"爬取失败 {url}: {str(e)}")
        result['error'] = str(e)
    
    return result

def crawl_batch_task(urls: List[str], parser_type: str = 'html', extract_rules: Dict = None) -> List[Dict[str, Any]]:
    """
    批量URL爬取任务
    
    Args:
        urls: URL列表
        parser_type: 解析类型
        extract_rules: 提取规则
    
    Returns:
        爬取结果列表
    """
    results = []
    total_urls = len(urls)
    
    for i, url in enumerate(urls):
        try:
            # 更新进度
            progress = int((i / total_urls) * 100)
            current_task.update_state(
                state='PROGRESS',
                meta={'progress': progress, 'message': f"处理第 {i+1}/{total_urls} 个URL"}
            )
            
            # 爬取单个URL
            result = crawl_url_task(url, parser_type, extract_rules)
            results.append(result)
            
            # 添加延迟避免请求过快
            time.sleep(Config.CRAWLER_DELAY)
            
        except Exception as e:
            logger.error(f"批量爬取失败 {url}: {str(e)}")
            results.append({
                'url': url,
                'status': 'failed',
                'error': str(e),
                'timestamp': time.time()
            })
    
    return results

async def async_crawl_url(url: str, session: aiohttp.ClientSession, parser_type: str = 'html') -> Dict[str, Any]:
    """
    异步爬取单个URL
    
    Args:
        url: 要爬取的URL
        session: aiohttp会话
        parser_type: 解析类型
    
    Returns:
        爬取结果
    """
    result = {
        'url': url,
        'status': 'failed',
        'data': None,
        'error': None,
        'timestamp': time.time()
    }
    
    try:
        headers = {
            'User-Agent': ua.random if Config.USER_AGENT_ROTATION else 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=Config.CRAWLER_TIMEOUT)) as response:
            if response.status == 200:
                if parser_type == 'html':
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    data = {
                        'title': soup.title.string if soup.title else '',
                        'text': soup.get_text()[:1000],
                        'links': [a.get('href') for a in soup.find_all('a', href=True)]
                    }
                else:
                    data = await response.text()
                
                result['status'] = 'success'
                result['data'] = data
            else:
                result['error'] = f"HTTP错误: {response.status}"
                
    except Exception as e:
        result['error'] = str(e)
    
    return result

def extract_data_from_html(soup: BeautifulSoup, rules: Dict) -> Dict[str, Any]:
    """
    根据规则从HTML中提取数据
    
    Args:
        soup: BeautifulSoup对象
        rules: 提取规则
    
    Returns:
        提取的数据
    """
    data = {}
    
    for field, rule in rules.items():
        try:
            if rule.get('type') == 'text':
                element = soup.select_one(rule['selector'])
                data[field] = element.get_text().strip() if element else ''
            elif rule.get('type') == 'attr':
                element = soup.select_one(rule['selector'])
                data[field] = element.get(rule['attr']) if element else ''
            elif rule.get('type') == 'list':
                elements = soup.select(rule['selector'])
                data[field] = [elem.get_text().strip() for elem in elements]
        except Exception as e:
            logger.error(f"提取字段 {field} 失败: {str(e)}")
            data[field] = ''
    
    return data

# Celery任务装饰器
from celery_app import celery_app

@celery_app.task(bind=True)
def crawl_url(self, url: str, parser_type: str = 'html', extract_rules: Dict = None):
    """Celery任务：爬取单个URL"""
    return crawl_url_task(url, parser_type, extract_rules)

@celery_app.task(bind=True)
def crawl_batch(self, urls: List[str], parser_type: str = 'html', extract_rules: Dict = None):
    """Celery任务：批量爬取URL"""
    return crawl_batch_task(urls, parser_type, extract_rules)

@celery_app.task(bind=True)
def async_crawl_batch(self, urls: List[str], parser_type: str = 'html'):
    """Celery任务：异步批量爬取"""
    async def run_async_crawl():
        async with aiohttp.ClientSession() as session:
            tasks = [async_crawl_url(url, session, parser_type) for url in urls]
            return await asyncio.gather(*tasks)
    
    return asyncio.run(run_async_crawl()) 