import os
import requests
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
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

def download_file(session, url, save_path, timeout=20):
    filename = get_filename_from_url(url)
    filepath = os.path.join(save_path, filename)
    temp_path = filepath + ".part"

    # 已完成直接跳过（静默 or 简短提示）
    if os.path.exists(filepath):
        return True  # 建议静默，避免刷屏

    headers = {}
    downloaded = 0

    if os.path.exists(temp_path):
        downloaded = os.path.getsize(temp_path)
        headers["Range"] = f"bytes={downloaded}-"

    try:
        with session.get(url, stream=True, timeout=timeout, headers=headers) as r:
            if r.status_code == 404:
                tqdm.write(f"❌ 404: {filename}")
                return False

            if r.status_code not in (200, 206):
                tqdm.write(f"❌ HTTP {r.status_code}: {filename}")
                return False

            total_size = int(r.headers.get("content-length", 0)) + downloaded
            mode = "ab" if downloaded > 0 else "wb"

            with open(temp_path, mode) as f, tqdm(
                total=total_size,
                initial=downloaded,
                unit="B",
                unit_scale=True,
                desc=filename,
                ncols=80,
                leave=False   # 👈 关键：完成后自动消失
            ) as pbar:

                for chunk in r.iter_content(chunk_size=1024 * 256):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))

        os.rename(temp_path, filepath)
        return True

    except Exception as e:
        tqdm.write(f"❌ 失败: {filename} ({e})")
        return False


# =========================
# 主流程
# =========================
def main():
    save_dir = input("请输入下载保存目录: ").strip()
    os.makedirs(save_dir, exist_ok=True)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    url_file = os.path.join(script_dir, "urls.txt")

    with open(url_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"\n共 {len(urls)} 个任务\n")

    success = 0
    fail = 0

    # 👇 并行线程数（可调）
    MAX_WORKERS = 6

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(download_file, create_session(), url, save_dir): url
            for url in urls
        }

        failed_urls = []

        for future in as_completed(futures):
            url = futures[future]
            try:
                ok = future.result()
                if ok:
                    success += 1
                else:
                    fail += 1
                    failed_urls.append(url)
            except Exception as e:
                print(f"⚠️ 线程异常: {url} -> {e}")
                fail += 1
                failed_urls.append(url)

    print("\n======================")
    print(f"完成: {success}")
    print(f"失败: {fail}")
    print("======================")
    if failed_urls:
        print("\n❌ 失败链接列表：")
        for u in failed_urls:
            print(u)


if __name__ == "__main__":
    main()