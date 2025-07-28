from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime
from scheduler import CrawlerScheduler
from config import Config

# 配置日志
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 创建调度器实例
scheduler = CrawlerScheduler()

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """创建爬虫任务"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        task_type = data.get('type', 'single')
        
        if task_type == 'single':
            url = data.get('url')
            if not url:
                return jsonify({'error': 'URL不能为空'}), 400
            
            parser_type = data.get('parser_type', 'html')
            extract_rules = data.get('extract_rules', {})
            
            task_id = scheduler.add_url_task(url, parser_type, extract_rules)
            
        elif task_type == 'batch':
            urls = data.get('urls', [])
            if not urls:
                return jsonify({'error': 'URL列表不能为空'}), 400
            
            parser_type = data.get('parser_type', 'html')
            extract_rules = data.get('extract_rules', {})
            
            task_id = scheduler.add_batch_task(urls, parser_type, extract_rules)
            
        else:
            return jsonify({'error': '不支持的任务类型'}), 400
        
        return jsonify({
            'task_id': task_id,
            'status': 'created',
            'message': '任务创建成功'
        })
        
    except Exception as e:
        logger.error(f"创建任务失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """获取任务状态"""
    try:
        status = scheduler.get_task_status(task_id)
        return jsonify(status)
    except Exception as e:
        logger.error(f"获取任务状态失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>/result', methods=['GET'])
def get_task_result(task_id):
    """获取任务结果"""
    try:
        result = scheduler.get_task_result(task_id)
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': '任务结果不存在'}), 404
    except Exception as e:
        logger.error(f"获取任务结果失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    """获取任务列表"""
    try:
        stats = scheduler.get_task_statistics()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"获取任务列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/execute', methods=['POST'])
def execute_task():
    """直接执行爬虫任务"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        execution_type = data.get('execution_type', 'single')
        
        if execution_type == 'single':
            url = data.get('url')
            if not url:
                return jsonify({'error': 'URL不能为空'}), 400
            
            parser_type = data.get('parser_type', 'html')
            extract_rules = data.get('extract_rules', {})
            
            result = scheduler.execute_single_task(url, parser_type, extract_rules)
            
        elif execution_type == 'batch':
            urls = data.get('urls', [])
            if not urls:
                return jsonify({'error': 'URL列表不能为空'}), 400
            
            parser_type = data.get('parser_type', 'html')
            extract_rules = data.get('extract_rules', {})
            
            result = scheduler.execute_batch_task(urls, parser_type, extract_rules)
            
        elif execution_type == 'async_batch':
            urls = data.get('urls', [])
            if not urls:
                return jsonify({'error': 'URL列表不能为空'}), 400
            
            parser_type = data.get('parser_type', 'html')
            
            result = scheduler.execute_async_batch_task(urls, parser_type)
            
        elif execution_type == 'parallel':
            urls = data.get('urls', [])
            if not urls:
                return jsonify({'error': 'URL列表不能为空'}), 400
            
            parser_type = data.get('parser_type', 'html')
            extract_rules = data.get('extract_rules', {})
            
            result = scheduler.execute_parallel_tasks(urls, parser_type, extract_rules)
            
        else:
            return jsonify({'error': '不支持的执行类型'}), 400
        
        return jsonify({
            'task_id': result.id,
            'status': 'executing',
            'message': '任务开始执行'
        })
        
    except Exception as e:
        logger.error(f"执行任务失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/cleanup', methods=['POST'])
def cleanup_tasks():
    """清理过期任务结果"""
    try:
        data = request.get_json() or {}
        hours = data.get('hours', 24)
        
        scheduler.cleanup_expired_results(hours)
        
        return jsonify({
            'message': f'清理了 {hours} 小时前的过期任务结果'
        })
        
    except Exception as e:
        logger.error(f"清理任务失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取配置信息"""
    try:
        config_info = {
            'redis_host': Config.REDIS_HOST,
            'redis_port': Config.REDIS_PORT,
            'max_workers': Config.MAX_WORKERS,
            'crawler_delay': Config.CRAWLER_DELAY,
            'crawler_timeout': Config.CRAWLER_TIMEOUT,
            'max_retries': Config.MAX_RETRIES,
            'use_proxy': Config.USE_PROXY,
            'user_agent_rotation': Config.USER_AGENT_ROTATION
        }
        return jsonify(config_info)
    except Exception as e:
        logger.error(f"获取配置失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    ) 