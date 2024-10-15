import os
import pandas as pd
import hashlib
import argparse

def shorten_url(long_url):
    return hashlib.sha256(long_url.encode()).hexdigest()[:8]

def process_urls(input_urls, regenerate_all):
    # 确保s目录存在
    if not os.path.exists('s'):
        os.makedirs('s')

    # 读取或初始化 _o.tsv
    if os.path.exists('_o.tsv'):
        df = pd.read_csv('_o.tsv', sep='\t', header=None)
    else:
        df = pd.DataFrame(columns=[0, 1])

    if regenerate_all:
        os.system('rm -rf s/*')  # 清空s文件夹
        df[1] = None  # 清除所有短链接

    # 去重和去空白
    existing_urls = set(df[0].dropna().apply(str.strip))

    # 处理输入的URLs
    if input_urls:
        for url in input_urls.split():
            url = url.strip()
            if url not in existing_urls:
                df = df.append({0: url}, ignore_index=True)

    # 生成或复用短链接
    for index, row in df.iterrows():
        long_url = row[0].strip()
        short_url = row[1]
        if pd.isna(short_url):
            short_url = shorten_url(long_url)
            row[1] = short_url
            # 保存到文件
            with open(f's/{short_url}', 'w') as file:
                file.write(long_url)

    # 更新_o.tsv
    df.to_csv('_o.tsv', sep='\t', index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description="Process URLs for shortening")
    parser.add_argument('urls', nargs='?', default='', help='Space-separated list of URLs to shorten')
    parser.add_argument('--all', action='store_true', help='Regenerate all URLs')
    
    args = parser.parse_args()
    
    process_urls(args.urls, args.all)

if __name__ == '__main__':
    main()
