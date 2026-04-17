import os
import shutil


def flatten_folder(path):
    if not os.path.isdir(path):
        print(f"❌ 路径不存在或不是文件夹: {path}")
        return

    print(f"\n📂 处理目录: {path}\n")

    moved_count = 0

    for root, dirs, files in os.walk(path):
        # 跳过根目录
        if root == path:
            continue

        for file in files:

            # ===== 可选：只处理某类文件 =====
            # if not file.lower().endswith(".gml"):
            #     continue

            src = os.path.join(root, file)
            dst = os.path.join(path, file)

            # 处理重名文件
            if os.path.exists(dst):
                name, ext = os.path.splitext(file)
                counter = 1
                while True:
                    new_name = f"{name}_{counter}{ext}"
                    dst = os.path.join(path, new_name)
                    if not os.path.exists(dst):
                        break
                    counter += 1

            print(f"➡️  {src} -> {dst}")
            shutil.move(src, dst)
            moved_count += 1

    print("\n======================")
    print(f"✅ 完成，共移动文件: {moved_count}")
    print("======================")


if __name__ == "__main__":
    path = input("请输入目标文件夹路径: ").strip()
    flatten_folder(path)