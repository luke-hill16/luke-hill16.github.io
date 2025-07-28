# 分布式爬虫系统

一个基于Python的分布式爬虫系统，支持多节点并行爬取、任务调度、结果存储等功能。

## 功能特性

- 🚀 **hhhhhh分布式架构**: 基于Celery和Redis的分布式任务处理
- 🔄 **多种爬取模式**: 支持单个、批量、并行、异步爬取
- 🎯 **灵活配置**: 支持代理、用户代理轮换、请求延迟等配置
- 📊 **任务监控**: 实时监控任务执行状态和统计信息
- 🌐 **Web API**: 提供RESTful API接口管理爬虫任务
- 💾 **数据存储**: 支持Redis缓存和多种数据库存储
- 🔧 **易于扩展**: 模块化设计，易于添加新的爬虫功能

## 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   主节点        │    │   工作节点1     │    │   工作节点2     │
│  (调度器)       │    │  (爬虫进程)     │    │  (爬虫进程)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Redis队列     │
                    │  (任务分发)     │
                    └─────────────────┘
```

## 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Redis (Ubuntu/Debian)
sudo apt-get install redis-server

# 安装Redis (macOS)
brew install redis

# 启动Redis服务
redis-server
```

## 快速开始

### 1. 配置环境

复制并修改配置文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置Redis连接等信息：

```env
# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# 爬虫配置
CRAWLER_DELAY=1.0
CRAWLER_TIMEOUT=30
MAX_RETRIES=3
MAX_WORKERS=4
```

### 2. 启动工作节点

```bash
# 启动工作节点
python worker.py --mode worker

# 启动定时任务调度器
python worker.py --mode beat

# 启动任务监控
python worker.py --mode monitor
```

### 3. 启动Web API

```bash
# 启动API服务
python api/app.py
```

### 4. 使用示例

```python
from scheduler import CrawlerScheduler

# 创建调度器
scheduler = CrawlerScheduler()

# 单个URL爬取
task_id = scheduler.add_url_task("https://example.com", parser_type='html')

# 批量URL爬取
urls = ["https://example1.com", "https://example2.com"]
task_id = scheduler.add_batch_task(urls, parser_type='html')

# 并行爬取
result = scheduler.execute_parallel_tasks(urls, parser_type='html')
```

## API接口

### 创建任务

```bash
# 单个任务
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "type": "single",
    "url": "https://example.com",
    "parser_type": "html"
  }'

# 批量任务
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "type": "batch",
    "urls": ["https://example1.com", "https://example2.com"],
    "parser_type": "html"
  }'
```

### 查询任务状态

```bash
curl http://localhost:5000/api/tasks/{task_id}
```

### 获取任务结果

```bash
curl http://localhost:5000/api/tasks/{task_id}/result
```

### 获取统计信息

```bash
curl http://localhost:5000/api/tasks
```

## 配置说明

### 爬虫配置

- `CRAWLER_DELAY`: 请求间隔时间（秒）
- `CRAWLER_TIMEOUT`: 请求超时时间（秒）
- `MAX_RETRIES`: 最大重试次数
- `MAX_WORKERS`: 最大工作进程数
- `MAX_CONCURRENT_REQUESTS`: 最大并发请求数

### 代理配置

```env
USE_PROXY=true
PROXY_LIST=http://proxy1:8080,http://proxy2:8080
```

### 用户代理配置

```env
USER_AGENT_ROTATION=true
```

## 自定义数据提取

支持通过CSS选择器自定义数据提取规则：

```python
extract_rules = {
    'title': {
        'type': 'text',
        'selector': 'h1.title'
    },
    'content': {
        'type': 'text',
        'selector': 'div.content'
    },
    'links': {
        'type': 'list',
        'selector': 'a.link'
    },
    'image': {
        'type': 'attr',
        'selector': 'img.cover',
        'attr': 'src'
    }
}
```

## 部署说明

### Docker部署

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "api/app.py"]
```

### 生产环境配置

1. 使用生产级Redis集群
2. 配置负载均衡器
3. 设置日志轮转
4. 配置监控告警
5. 使用HTTPS

## 监控和日志

### 日志配置

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)
```

### 性能监控

- 任务执行时间
- 成功率统计
- 队列长度监控
- 资源使用情况

## 故障排除

### 常见问题

1. **Redis连接失败**
   - 检查Redis服务是否启动
   - 验证连接配置

2. **任务执行失败**
   - 检查网络连接
   - 验证目标网站可访问性
   - 查看错误日志

3. **性能问题**
   - 调整并发数配置
   - 优化请求间隔
   - 使用代理池

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue 或联系开发者。 