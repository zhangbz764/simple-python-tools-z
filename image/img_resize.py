import os
from PIL import Image


def resize_images_in_folder(folder_path, width, height):
    """
    Resize all images in the given folder to the specified width and height.

    :param folder_path: Path to the folder containing images
    :param width: Desired width in pixels
    :param height: Desired height in pixels
    """
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    # Create a folder to save the resized images
    output_folder = os.path.join(folder_path, "resized")
    os.makedirs(output_folder, exist_ok=True)

    # Supported image formats
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff")

    # Iterate through the folder
    count = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if the file is an image
        if os.path.isfile(file_path) and filename.lower().endswith(supported_formats):
            try:
                # Open the image
                img = Image.open(file_path)

                # Resize the image
                resized_img = img.resize((width, height))

                # Save the resized image in the output folder
                output_path = os.path.join(output_folder, filename)
                resized_img.save(output_path)

                count = count + 1
                print(f"Resized and saved: {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        else:
            print(f"Skipping non-image file: {filename}")

    print(f"All images resized and saved in '{output_folder}'.")


# Example usage
if __name__ == "__main__":
    # Input folder path and dimensions
    folder = input("Enter the folder path containing images: ").strip()
    width = int(input("Enter the new width in pixels: ").strip())
    height = int(input("Enter the new height in pixels: ").strip())

    # Resize images
    resize_images_in_folder(folder, width, height)
