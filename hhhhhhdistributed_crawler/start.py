#!/usr/bin/env python3
"""
分布式爬虫系统启动脚本
用于快速启动整个系统
"""

import os
import sys
import time
import subprocess
import threading
import signal
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DistributedCrawler:
    """分布式爬虫系统管理器"""
    
    def __init__(self):
        self.processes = []
        self.running = False
        
    def start_redis(self):
        """启动Redis服务"""
        try:
            logger.info("检查Redis服务...")
            import redis
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.ping()
            logger.info("Redis服务已运行")
            return True
        except Exception as e:
            logger.warning(f"Redis服务未运行: {str(e)}")
            logger.info("请手动启动Redis服务: redis-server")
            return False
    
    def start_worker(self, worker_id=1):
        """启动工作节点"""
        try:
            logger.info(f"启动工作节点 {worker_id}...")
            cmd = [sys.executable, "worker.py", "--mode", "worker"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(process)
            logger.info(f"工作节点 {worker_id} 已启动 (PID: {process.pid})")
            return process
        except Exception as e:
            logger.error(f"启动工作节点失败: {str(e)}")
            return None
    
    def start_api(self):
        """启动Web API服务"""
        try:
            logger.info("启动Web API服务...")
            cmd = [sys.executable, "api/app.py"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(process)
            logger.info(f"Web API服务已启动 (PID: {process.pid})")
            return process
        except Exception as e:
            logger.error(f"启动Web API服务失败: {str(e)}")
            return None
    
    def start_monitor(self):
        """启动任务监控"""
        try:
            logger.info("启动任务监控...")
            cmd = [sys.executable, "worker.py", "--mode", "monitor"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(process)
            logger.info(f"任务监控已启动 (PID: {process.pid})")
            return process
        except Exception as e:
            logger.error(f"启动任务监控失败: {str(e)}")
            return None
    
    def start_beat(self):
        """启动定时任务调度器"""
        try:
            logger.info("启动定时任务调度器...")
            cmd = [sys.executable, "worker.py", "--mode", "beat"]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.processes.append(process)
            logger.info(f"定时任务调度器已启动 (PID: {process.pid})")
            return process
        except Exception as e:
            logger.error(f"启动定时任务调度器失败: {str(e)}")
            return None
    
    def start_all(self, num_workers=2):
        """启动所有服务"""
        logger.info("启动分布式爬虫系统...")
        
        # 检查Redis
        if not self.start_redis():
            logger.error("Redis服务未运行，请先启动Redis")
            return False
        
        # 启动工作节点
        for i in range(num_workers):
            self.start_worker(i + 1)
            time.sleep(1)
        
        # 启动API服务
        self.start_api()
        time.sleep(2)
        
        # 启动监控
        self.start_monitor()
        time.sleep(1)
        
        # 启动定时任务调度器
        self.start_beat()
        
        self.running = True
        logger.info("分布式爬虫系统启动完成！")
        logger.info("Web API地址: http://localhost:5000")
        logger.info("按 Ctrl+C 停止所有服务")
        
        return True
    
    def stop_all(self):
        """停止所有服务"""
        logger.info("停止分布式爬虫系统...")
        
        self.running = False
        
        for process in self.processes:
            try:
                if process.poll() is None:  # 进程仍在运行
                    logger.info(f"停止进程 (PID: {process.pid})")
                    process.terminate()
                    process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(f"强制停止进程 (PID: {process.pid})")
                process.kill()
            except Exception as e:
                logger.error(f"停止进程失败: {str(e)}")
        
        self.processes.clear()
        logger.info("所有服务已停止")
    
    def monitor_processes(self):
        """监控进程状态"""
        while self.running:
            for i, process in enumerate(self.processes):
                if process.poll() is not None:  # 进程已结束
                    logger.warning(f"进程 {i+1} 已停止 (PID: {process.pid})")
                    # 可以在这里重启进程
            time.sleep(10)
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        logger.info("收到停止信号")
        self.stop_all()
        sys.exit(0)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='分布式爬虫系统启动器')
    parser.add_argument(
        '--workers',
        type=int,
        default=2,
        help='工作节点数量 (默认: 2)'
    )
    parser.add_argument(
        '--api-only',
        action='store_true',
        help='仅启动API服务'
    )
    parser.add_argument(
        '--worker-only',
        action='store_true',
        help='仅启动工作节点'
    )
    
    args = parser.parse_args()
    
    # 创建系统管理器
    crawler = DistributedCrawler()
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, crawler.signal_handler)
    signal.signal(signal.SIGTERM, crawler.signal_handler)
    
    try:
        if args.api_only:
            # 仅启动API服务
            crawler.start_redis()
            crawler.start_api()
        elif args.worker_only:
            # 仅启动工作节点
            crawler.start_redis()
            for i in range(args.workers):
                crawler.start_worker(i + 1)
        else:
            # 启动所有服务
            crawler.start_all(args.workers)
        
        # 启动进程监控
        monitor_thread = threading.Thread(target=crawler.monitor_processes)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # 保持主线程运行
        while crawler.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("收到中断信号")
    except Exception as e:
        logger.error(f"启动失败: {str(e)}")
    finally:
        crawler.stop_all()

if __name__ == '__main__':
    main() 