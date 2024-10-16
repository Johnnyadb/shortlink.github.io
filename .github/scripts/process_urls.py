import os
import pandas as pd
import hashlib
import base64
import re
import argparse
import json

def shorten_url(long_url):
    # 使用 sha256 生成哈希值
    sha256_hash = hashlib.sha256((long_url + '-sk').encode()).digest()
    # 使用 base64 编码，并将结果转换为字符串，去除尾部的 '=' 填充字符
    base64_encoded = base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip('=')
    # 只保留 a-z, A-Z, 0-9 的字符
    filtered_chars = re.sub(r'[^a-zA-Z0-9]', '', base64_encoded)
    # 返回最多前12个合法字符，但不强制12个
    return filtered_chars[:12]

def process_urls(input_urls='', regenerate_all=False):
    tsv_path = '_o.tsv'
    s_dir = 's'

    # 确保s目录存在
    if not os.path.exists(s_dir):
        os.makedirs(s_dir)

    # 读取或初始化_o.tsv
    if os.path.exists(tsv_path):
        df = pd.read_csv(tsv_path, sep='\t', header=None, names=['Long URL', 'Short URL'])
    else:
        df = pd.DataFrame(columns=['Long URL', 'Short URL'])

    # 处理input_urls参数
    if input_urls:
        new_urls = [url.strip() for url in input_urls.split()]
        new_data = pd.DataFrame({'Long URL': new_urls, 'Short URL': pd.NA})
        df = pd.concat([df, new_data], ignore_index=True)

    # 去重处理，确保每个URL只被处理一次
    df.drop_duplicates(subset='Long URL', inplace=True, ignore_index=True)

    # 处理--all参数，删除s文件夹中所有文件，并重置短链接
    if regenerate_all:
        os.system(f'rm -rf {s_dir}/*')  # 清空s文件夹
        df['Short URL'] = pd.NA  # 重置短链接列

    # 生成短链接并更新s文件夹和_o.tsv文件（第2列）
    for index, row in df.iterrows():
        short_url = row['Short URL']
        file_path = f'{s_dir}/{short_url}.json'

        # 检查短链接是否存在，以及对应的文件是否存在
        if pd.isna(short_url) or not os.path.exists(file_path):
            # 重新生成短链接
            short_url = shorten_url(row['Long URL'])
            df.at[index, 'Short URL'] = short_url
            file_path = f'{s_dir}/{short_url}.json'  # 更新文件路径

        # 将长链接写入对应的短链接文件
        with open(file_path, 'w') as file:
            json.dump({"l": row['Long URL']}, file)

    # 更新_o.tsv
    df.to_csv(tsv_path, sep='\t', index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description="Process URLs for shortening")
    # '*' 允许接受零个或多个输入，这些输入将作为列表传入
    parser.add_argument('urls', nargs='*', default='', help='Space-separated list of URLs to shorten')
    parser.add_argument('--all', action='store_true', help='Regenerate all URLs')
    
    args = parser.parse_args()
    # 将 args.urls（现在是一个列表）直接传给 process_urls 函数
    # 因为 process_urls 函数期望的是字符串，所以使用 ' '.join(args.urls)
    input_urls = ' '.join(args.urls) if args.urls else ''
    process_urls(input_urls, args.all)

if __name__ == '__main__':
    main()
