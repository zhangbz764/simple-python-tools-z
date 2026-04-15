import os
from PIL import Image

def convert_images(folder_path, target_format):
    # Create output folder
    output_folder = os.path.join(folder_path, target_format)
    os.makedirs(output_folder, exist_ok=True)

    # Supported input formats
    supported_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif')

    for file in os.listdir(folder_path):
        if file.lower().endswith(supported_extensions):
            img_path = os.path.join(folder_path, file)
            try:
                img = Image.open(img_path)
                # Retain color mode where possible
                if target_format == 'jpg':
                    # JPEG requires RGB
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    new_name = os.path.splitext(file)[0] + '.jpg'
                elif target_format == 'png':
                    # PNG can retain modes, but convert CMYK to RGB if necessary
                    if img.mode == 'CMYK':
                        img = img.convert('RGB')
                    new_name = os.path.splitext(file)[0] + '.png'

                new_path = os.path.join(output_folder, new_name)
                img.save(new_path)
                print(f"Converted {file} to {new_name}")
            except Exception as e:
                print(f"Error converting {file}: {e}")

def main():
    folder_path = input("Enter folder path: ").strip()
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    target_format = input("Enter target format (jpg or png): ").strip().lower()
    if target_format not in ['jpg', 'png']:
        print("Invalid format. Choose 'jpg' or 'png'.")
        return

    convert_images(folder_path, target_format)

if __name__ == "__main__":
    main()
