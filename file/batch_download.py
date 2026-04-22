import os
import requests
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# =========================
# 创建带重试的 session
# =========================
def create_session(retries=5):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


# =========================
# 从 URL 推断文件名
# =========================
def get_filename_from_url(url):
    path = urlparse(url).path
    name = os.path.basename(path)
    return name if name else "downloaded_file"


# =========================
# 单文件下载（支持断点续传）
# =========================
def download_file(session, url, save_path, timeout=20):
    filename = get_filename_from_url(url)
    filepath = os.path.join(save_path, filename)
    temp_path = filepath + ".part"

    headers = {}

    # 断点续传
    if os.path.exists(temp_path):
        downloaded = os.path.getsize(temp_path)
        headers["Range"] = f"bytes={downloaded}-"
    else:
        downloaded = 0

    try:
        with session.get(url, stream=True, timeout=timeout, headers=headers) as r:
            if r.status_code == 404:
                print(f"❌ 404: {url}")
                return False

            if r.status_code not in (200, 206):
                print(f"⚠️ 状态码异常 {r.status_code}: {url}")
                return False

            mode = "ab" if downloaded > 0 else "wb"

            with open(temp_path, mode) as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        os.rename(temp_path, filepath)
        print(f"✅ 完成: {filename}")
        return True

    except Exception as e:
        print(f"⚠️ 下载失败: {url} -> {e}")
        return False


# =========================
# 主流程
# =========================
def main():
    # 输入目录
    save_dir = input("请输入下载保存目录: ").strip()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 读取 urls.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    url_file = os.path.join(script_dir, "urls.txt")

    if not os.path.exists(url_file):
        print(f"❌ 未找到 urls.txt: {url_file}")
        return

    with open(url_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"\n共 {len(urls)} 个任务\n")

    session = create_session()

    success = 0
    fail = 0

    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] {url}")

        ok = download_file(session, url, save_dir)

        if ok:
            success += 1
        else:
            fail += 1

    print("\n======================")
    print(f"完成: {success}")
    print(f"失败: {fail}")
    print("======================")


if __name__ == "__main__":
    main()