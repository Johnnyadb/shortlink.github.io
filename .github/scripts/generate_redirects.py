#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
短链接重定向页面生成器
功能：根据JSON配置文件生成对应的重定向页面
作者：Cursor AI
日期：2023-12-25
"""

import os
import json
import glob
import shutil
import logging
import argparse
from typing import Set, Dict, List, Optional
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_CONFIG = {
    'json_dir': 's',
    'log_level': 'INFO',
    'verify_urls': False,
    'show_progress': True,
    'require_https': False  # 是否要求HTTPS
}

class ConfigurationError(Exception):
    """配置错误"""
    pass

class URLValidationError(Exception):
    """URL验证错误"""
    pass

class FileOperationError(Exception):
    """文件操作错误"""
    pass

class Config:
    """配置管理类"""
    
    @staticmethod
    def load_from_file(file_path: str) -> Dict:
        """从文件加载配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"配置文件格式错误: {e}")
        except Exception as e:
            raise ConfigurationError(f"读取配置文件失败: {e}")

    @staticmethod
    def load_from_args(args: argparse.Namespace) -> Dict:
        """从命令行参数加载配置"""
        config = DEFAULT_CONFIG.copy()
        
        if args.config and os.path.isfile(args.config):
            try:
                file_config = Config.load_from_file(args.config)
                config.update(file_config)
            except ConfigurationError as e:
                logger.error(str(e))
        
        # 命令行参数覆盖配置文件
        if args.json_dir:
            config['json_dir'] = args.json_dir
        if args.log_level:
            config['log_level'] = args.log_level
        if args.no_verify:
            config['verify_urls'] = False
        if args.no_progress:
            config['show_progress'] = False
            
        return config

class URLValidator:
    """URL验证器"""
    
    @staticmethod
    def validate(url: str, require_https: bool = True) -> bool:
        """验证URL格式是否正确"""
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise URLValidationError("URL缺少必要的组件")
            if require_https and result.scheme != 'https':
                raise URLValidationError("URL必须使用HTTPS协议")
            return True
        except Exception as e:
            raise URLValidationError(f"URL格式错误: {e}")

class FileManager:
    """文件管理器"""
    
    @staticmethod
    def ensure_directory(path: str) -> None:
        """确保目录存在"""
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            raise FileOperationError(f"创建目录失败: {e}")
    
    @staticmethod
    def clean_directory(path: str) -> None:
        """清理目录内容"""
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)
        except Exception as e:
            raise FileOperationError(f"清理目录失败: {e}")
    
    @staticmethod
    def write_file(path: str, content: str) -> None:
        """写入文件内容"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise FileOperationError(f"写入文件失败: {e}")
    
    @staticmethod
    def read_json(path: str) -> Dict:
        """读取JSON文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise FileOperationError(f"JSON格式错误: {e}")
        except Exception as e:
            raise FileOperationError(f"读取文件失败: {e}")

class RedirectGenerator:
    """重定向页面生成器类"""
    
    def __init__(self, config: Dict = None):
        """初始化生成器"""
        self.config = config or DEFAULT_CONFIG
        self.json_dir = self.config.get('json_dir', 's')
        self.existing_codes: Set[str] = set()
        self.protected_dirs = {'.git', '.github', 's'}
        
        # 更新日志级别
        logger.setLevel(getattr(logging, self.config.get('log_level', 'INFO').upper()))

    def generate_redirect_html(self, target_url: str) -> str:
        """生成重定向HTML内容"""
        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="referrer" content="no-referrer">
    <meta http-equiv="refresh" content="0;url={target_url}">
    <script>
        window.location.replace("{target_url}");
    </script>
</head>
</html>'''

    def is_redirect_directory(self, dir_name: str) -> bool:
        """检查是否是重定向目录"""
        try:
            # 检查目录名长度和字符
            if not (len(dir_name) == 12 and dir_name.isalnum()):
                return False
                
            # 检查 index.html 是否存在
            index_path = os.path.join(dir_name, 'index.html')
            if not os.path.isfile(index_path):
                return False
                
            # 检查文件内容
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return '<meta http-equiv="refresh"' in content and 'window.location.replace' in content
        except Exception as e:
            logger.error(f"检查目录 {dir_name} 失败: {e}")
            return False

    def clean_old_redirects(self) -> None:
        """清理不再使用的重定向文件和目录"""
        try:
            for dir_name in os.listdir('.'):
                # 跳过非目录和受保护的目录
                if (not os.path.isdir(dir_name) or 
                    dir_name in self.protected_dirs or 
                    dir_name in self.existing_codes):
                    continue
                
                # 检查是否是重定向目录
                if not self.is_redirect_directory(dir_name):
                    logger.debug(f"跳过非重定向目录: {dir_name}")
                    continue
                
                # 删除目录
                try:
                    shutil.rmtree(dir_name)
                    logger.info(f"已删除旧目录: {dir_name}")
                except Exception as e:
                    logger.error(f"删除目录 {dir_name} 失败: {e}")
        except Exception as e:
            logger.error(f"清理过程中发生错误: {e}")

    def process_json_file(self, json_file: str, total: int, current: int) -> bool:
        """处理单个JSON文件"""
        try:
            # 读取JSON文件
            data = FileManager.read_json(json_file)
            target_url = data.get('l')
            
            if not target_url:
                raise FileOperationError(f"JSON文件中没有找到目标URL")
            
            # 验证URL
            if self.config.get('verify_urls', True):
                URLValidator.validate(
                    target_url, 
                    require_https=self.config.get('require_https', True)
                )
            
            # 获取短码
            short_code = Path(json_file).stem
            self.existing_codes.add(short_code)
            
            # 创建或清理短码目录
            FileManager.clean_directory(short_code)
            
            # 生成并写入重定向HTML
            html_content = self.generate_redirect_html(target_url)
            html_path = os.path.join(short_code, 'index.html')
            FileManager.write_file(html_path, html_content)
            
            # 显示进度
            if self.config.get('show_progress', True):
                progress = (current + 1) / total * 100
                logger.info(f"进度: [{current + 1}/{total}] {progress:.1f}% - {html_path} -> {target_url}")
            else:
                logger.info(f"已生成重定向页面: {html_path} -> {target_url}")
            
            return True
            
        except (FileOperationError, URLValidationError) as e:
            logger.error(f"处理 {json_file} 失败: {e}")
            return False
        except Exception as e:
            logger.error(f"处理 {json_file} 时发生未知错误: {e}")
            return False

    def run(self) -> bool:
        """执行主要处理流程"""
        try:
            start_time = datetime.now()
            
            # 获取所有JSON文件
            json_files = glob.glob(os.path.join(self.json_dir, '*.json'))
            if not json_files:
                logger.warning(f"在 {self.json_dir} 目录中没有找到JSON文件")
                return True
            
            # 处理所有JSON文件
            success_count = 0
            total = len(json_files)
            
            for i, json_file in enumerate(json_files):
                if self.process_json_file(json_file, total, i):
                    success_count += 1
            
            # 清理旧的重定向文件
            self.clean_old_redirects()
            
            # 计算执行时间
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"处理完成: 成功 {success_count}/{total} (用时: {duration:.2f}秒)")
            
            return success_count == total
            
        except Exception as e:
            logger.error(f"程序执行失败: {e}")
            return False

def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="短链接重定向页面生成器")
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--json-dir', help='JSON文件目录')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='日志级别')
    parser.add_argument('--no-verify', action='store_true', help='禁用URL验证')
    parser.add_argument('--no-progress', action='store_true', help='禁用进度显示')
    return parser.parse_args()

def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_args()
        
        # 加载配置
        config = Config.load_from_args(args)
        
        # 创建生成器实例并运行
        generator = RedirectGenerator(config)
        success = generator.run()
        
        # 根据执行结果设置退出码
        exit(0 if success else 1)
    except Exception as e:
        logger.error(f"程序异常退出: {e}")
        exit(1)

if __name__ == '__main__':
    main() 