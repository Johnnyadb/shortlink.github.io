#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
短链接生成器
功能：将长URL转换为短链接，并生成对应的JSON文件
作者：Cursor AI
日期：2023-12-25
"""

import os
import pandas as pd
import hashlib
import base64
import re
import argparse
import json

def shorten_url(long_url):
    """
    将长URL转换为短码
    
    参数：
        long_url (str): 需要转换的长URL
        
    返回：
        str: 12位的短码，只包含字母和数字
        
    实现说明：
    1. 使用SHA256对URL进行哈希，加入'-sk'作为盐值增加唯一性
    2. 使用Base64编码转换为可读字符
    3. 过滤出字母和数字
    4. 截取前12位作为短码
    """
    # 使用 sha256 生成哈希值，添加盐值'-sk'增加唯一性
    sha256_hash = hashlib.sha256((long_url + '-sk').encode()).digest()
    # 使用 base64 编码，并将结果转换为字符串，去除尾部的 '=' 填充字符
    base64_encoded = base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip('=')
    # 只保留 a-z, A-Z, 0-9 的字符
    filtered_chars = re.sub(r'[^a-zA-Z0-9]', '', base64_encoded)
    # 返回最多前12个合法字符
    return filtered_chars[:12]

def process_urls(input_urls='', regenerate_all=False):
    """
    处理URL列表，生成短链接和相关文件
    
    参数：
        input_urls (str): 空格分隔的URL列表字符串
        regenerate_all (bool): 是否重新生成所有短链接
        
    文件说明：
        _o.tsv: 存储长URL和短码的对应关系
        s/: 存储短码对应的JSON文件
    """
    tsv_path = '_o.tsv'
    s_dir = 's'

    # 确保s目录存在
    if not os.path.exists(s_dir):
        os.makedirs(s_dir)

    # 读取或初始化_o.tsv文件
    # 文件格式：长URL\t短码
    if os.path.exists(tsv_path):
        df = pd.read_csv(tsv_path, sep='\t', header=None, names=['Long URL', 'Short URL'])
    else:
        df = pd.DataFrame(columns=['Long URL', 'Short URL'])

    # 处理新输入的URL列表
    if input_urls:
        new_urls = [url.strip() for url in input_urls.split()]
        new_data = pd.DataFrame({'Long URL': new_urls, 'Short URL': pd.NA})
        df = pd.concat([df, new_data], ignore_index=True)

    # 去重处理，确保每个URL只被处理一次
    df.drop_duplicates(subset='Long URL', inplace=True, ignore_index=True)

    # 如果需要重新生成所有短链接
    if regenerate_all:
        # 清理s目录中的JSON文件
        for file in os.listdir(s_dir):
            if file.endswith('.json'):
                os.remove(os.path.join(s_dir, file))
        # 重置短码列，准备重新生成
        df['Short URL'] = pd.NA

    # 处理每个URL，生成短链接和相关文件
    for index, row in df.iterrows():
        long_url = row['Long URL']
        short_url = row['Short URL']
        
        # 如果没有短码，生成新的短码
        if pd.isna(short_url):
            short_url = shorten_url(long_url)
            df.at[index, 'Short URL'] = short_url
        
        # 在s目录下创建JSON文件，存储URL信息
        json_path = os.path.join(s_dir, f'{short_url}.json')
        with open(json_path, 'w') as f:
            json.dump({"l": long_url}, f)

    # 更新_o.tsv文件，保存映射关系
    df.to_csv(tsv_path, sep='\t', index=False, header=False)
    
    # 打印生成的短链接
    print("\n生成的短链接：")
    for _, row in df.iterrows():
        print(f"{row['Short URL']} -> {row['Long URL']}")

def main():
    """
    主函数，处理命令行参数并执行URL处理
    
    命令行参数：
        urls: 空格分隔的URL列表
        --all: 是否重新生成所有短链接
        
    使用示例：
        1. 添加新URL：
           python process_urls.py "https://example.com"
        2. 添加多个URL：
           python process_urls.py "https://example1.com" "https://example2.com"
        3. 重新生成所有短链接：
           python process_urls.py --all
    """
    parser = argparse.ArgumentParser(description="短链接生成器")
    parser.add_argument('urls', nargs='*', default='', help='要转换的URL列表，用空格分隔')
    parser.add_argument('--all', action='store_true', help='重新生成所有短链接')
    
    args = parser.parse_args()
    input_urls = ' '.join(args.urls) if args.urls else ''
    process_urls(input_urls, args.all)

if __name__ == '__main__':
    main()
