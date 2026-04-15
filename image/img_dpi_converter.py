import os
from PIL import Image

def convert_to_300dpi(input_folder, output_folder):
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        # 检查文件是否为图片
        if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # 打开图像文件
            image = Image.open(input_path)

            # 转换为 RGB 模式（如果不是 RGB 模式）
            image = image.convert("RGB")

            # 检查是否有 'dpi' 信息，若没有设置默认的 72 DPI
            if 'dpi' in image.info:
                dpi = image.info['dpi']
            else:
                dpi = (72, 72)

            # 直接修改并保存为 300 DPI，像素大小保持不变
            image.save(output_path, dpi=(300, 300))

if __name__ == "__main__": 
    input_folder = input("请输入要转换的文件夹路径：") 
    output_folder = input("请输入输出文件夹路径：")

    convert_to_300dpi(input_folder, output_folder)
    print("转换完成！")
