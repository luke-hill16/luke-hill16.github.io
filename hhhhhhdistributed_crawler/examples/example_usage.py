#!/usr/bin/env python3
"""
分布式爬虫使用示例
展示如何使用分布式爬虫系统
"""

import time
import json
import requests
from scheduler import CrawlerScheduler

def example_single_crawl():
    """示例：单个URL爬取"""
    print("=== 单个URL爬取示例 ===")
    
    scheduler = CrawlerScheduler()
    
    # 创建单个爬取任务
    url = "https://httpbin.org/html"
    task_id = scheduler.add_url_task(url, parser_type='html')
    
    print(f"创建任务: {task_id}")
    
    # 等待任务完成
    while True:
        status = scheduler.get_task_status(task_id)
        print(f"任务状态: {status['status']}")
        
        if status['status'] in ['success', 'failed']:
            break
        
        time.sleep(2)
    
    # 获取结果
    result = scheduler.get_task_result(task_id)
    if result:
        print(f"爬取结果: {json.dumps(result, indent=2, ensure_ascii=False)}")

def example_batch_crawl():
    """示例：批量URL爬取"""
    print("\n=== 批量URL爬取示例 ===")
    
    scheduler = CrawlerScheduler()
    
    # 准备URL列表
    urls = [
        "https://httpbin.org/html",
        "https://httpbin.org/json",
        "https://httpbin.org/xml"
    ]
    
    # 创建批量爬取任务
    task_id = scheduler.add_batch_task(urls, parser_type='html')
    
    print(f"创建批量任务: {task_id}")
    
    # 等待任务完成
    while True:
        status = scheduler.get_task_status(task_id)
        print(f"任务状态: {status['status']}")
        
        if status['status'] in ['success', 'failed']:
            break
        
        time.sleep(3)
    
    # 获取结果
    result = scheduler.get_task_result(task_id)
    if result:
        print(f"批量爬取结果: {json.dumps(result, indent=2, ensure_ascii=False)}")

def example_parallel_crawl():
    """示例：并行爬取"""
    print("\n=== 并行爬取示例 ===")
    
    scheduler = CrawlerScheduler()
    
    # 准备URL列表
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/3",
        "https://httpbin.org/delay/1"
    ]
    
    # 执行并行爬取
    result = scheduler.execute_parallel_tasks(urls, parser_type='html')
    
    print(f"并行任务ID: {result.id}")
    
    # 等待任务完成
    while not result.ready():
        print("任务执行中...")
        time.sleep(2)
    
    # 获取结果
    results = result.get()
    print(f"并行爬取结果: {json.dumps(results, indent=2, ensure_ascii=False)}")

def example_custom_extract():
    """示例：自定义数据提取"""
    print("\n=== 自定义数据提取示例 ===")
    
    scheduler = CrawlerScheduler()
    
    # 定义提取规则
    extract_rules = {
        'title': {
            'type': 'text',
            'selector': 'h1'
        },
        'links': {
            'type': 'list',
            'selector': 'a'
        },
        'description': {
            'type': 'text',
            'selector': 'p'
        }
    }
    
    # 执行带提取规则的爬取
    url = "https://httpbin.org/html"
    result = scheduler.execute_single_task(url, parser_type='html', extract_rules=extract_rules)
    
    print(f"自定义提取任务ID: {result.id}")
    
    # 等待任务完成
    while not result.ready():
        print("任务执行中...")
        time.sleep(2)
    
    # 获取结果
    data = result.get()
    print(f"自定义提取结果: {json.dumps(data, indent=2, ensure_ascii=False)}")

def example_api_usage():
    """示例：通过API使用"""
    print("\n=== API使用示例 ===")
    
    api_base = "http://localhost:5000/api"
    
    # 创建单个任务
    task_data = {
        'type': 'single',
        'url': 'https://httpbin.org/html',
        'parser_type': 'html'
    }
    
    response = requests.post(f"{api_base}/tasks", json=task_data)
    if response.status_code == 200:
        task_info = response.json()
        task_id = task_info['task_id']
        print(f"通过API创建任务: {task_id}")
        
        # 查询任务状态
        while True:
            status_response = requests.get(f"{api_base}/tasks/{task_id}")
            if status_response.status_code == 200:
                status = status_response.json()
                print(f"任务状态: {status['status']}")
                
                if status['status'] in ['success', 'failed']:
                    break
            
            time.sleep(2)
        
        # 获取任务结果
        result_response = requests.get(f"{api_base}/tasks/{task_id}/result")
        if result_response.status_code == 200:
            result = result_response.json()
            print(f"API获取结果: {json.dumps(result, indent=2, ensure_ascii=False)}")

def example_statistics():
    """示例：获取统计信息"""
    print("\n=== 统计信息示例 ===")
    
    scheduler = CrawlerScheduler()
    
    # 获取任务统计
    stats = scheduler.get_task_statistics()
    print(f"任务统计: {json.dumps(stats, indent=2, ensure_ascii=False)}")

def main():
    """主函数"""
    print("分布式爬虫使用示例")
    print("=" * 50)
    
    try:
        # 运行各种示例
        example_single_crawl()
        example_batch_crawl()
        example_parallel_crawl()
        example_custom_extract()
        example_api_usage()
        example_statistics()
        
        print("\n所有示例执行完成！")
        
    except Exception as e:
        print(f"示例执行失败: {str(e)}")
        print("请确保Redis服务已启动，并且工作节点正在运行")

if __name__ == '__main__':
    main() 