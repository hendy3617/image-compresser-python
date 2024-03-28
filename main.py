import os
import datetime
from PIL import Image


def log_activity(activity):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {activity}')
# create a function that will go into every folder in the current working directory and compress the images


def compress_images(directory=None, quality=80):
    """Recursively compresses all images in a given directory.

    Args:
        directory (str, optional): Directory to search for images.
            Defaults to the current working directory.
        quality (int, optional): Quality factor to use when saving images.
            Defaults to 10.
    """
    if directory is None:
        directory = os.getcwd()

    img_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']

    resized_folder = os.path.join(directory, 'Resized')
    os.makedirs(resized_folder, exist_ok=True)

    for root, _, filenames in os.walk(directory):
        relative_path = os.path.relpath(root, directory)
        for filename in filenames:
            lower_filename = filename.lower()
            if any(lower_filename.endswith(ext) for ext in img_extensions):
                img_path = os.path.join(root, filename)
                try:
                    with Image.open(img_path) as img:
                        width, height = img.size
                        if width > 512 or height > 512:
                            scale = 512 / max(width, height)
                            new_width = int(width * scale)
                            new_height = int(height * scale)
                            img = img.resize((new_width, new_height))
                            resized_subfolder = os.path.join(
                                resized_folder, relative_path)
                            os.makedirs(resized_subfolder, exist_ok=True)
                            resized_filename = os.path.join(
                                resized_subfolder, filename)
                            log_activity(f'Compressing {img_path}')
                            img.save(resized_filename,
                                     format=img.format, quality=quality)
                except (FileNotFoundError, OSError) as e:
                    log_activity(f"Error processing {img_path}: {e}")


def main():
    log_activity(f'Starting image compression on directory {os.getcwd()}')
    compress_images()
    log_activity('Finished image compression')


if __name__ == '__main__':
    main()
