import os
from bs4 import BeautifulSoup

def extract_links():
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, 'html.html')
    urls_path = os.path.join(current_dir, 'urls.txt')
    
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found.")
        return

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        
        # 查找所有带有 data-v-f735cdbe 属性的 <a> 标签
        # 即使属性值为空字符串，attrs={'data-v-f735cdbe': True} 也能匹配到
        links = soup.find_all('a')
        
        extracted_links = []
        for link in links:
            href = link.get('href')
            if href and href.endswith('.zip'):
                extracted_links.append(href)
        
        # 打印链接并写入文件
        with open(urls_path, 'a', encoding='utf-8') as f:
            for url in extracted_links:
                print(url)
                f.write(url + '\n')
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    extract_links()