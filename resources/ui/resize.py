from PIL import Image
import os
import sys

def resize_image(input_path, output_path, new_size):
    """
    Resize an image and save it to the specified path.

    Args:
    input_path (str): The path to the original image.
    output_path (str): The path where the resized image will be saved.
    new_size (tuple): The new size of the image, e.g., (width, height).
    """
    # Open an image file
    with Image.open(input_path) as img:
        # Resize the image
        img = img.resize(new_size, Image.NEAREST)
        # Save the resized image
        img.save(output_path)

def main():
    if len(sys.argv) != 4:
        print("Usage: python resize.py <path_to_image> <width> <height>")
        return

    path_to_image = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    new_size = (width, height)

    # Check if the file exists
    if not os.path.exists(path_to_image):
        print("Error: The specified file does not exist.")
        return

    # Construct the output file path
    directory, filename = os.path.split(path_to_image)
    file_root, file_ext = os.path.splitext(filename)
    output_filename = f"{file_root}_resized{file_ext}"
    output_path = os.path.join(directory, output_filename)

    # Resize the image
    resize_image(path_to_image, output_path, new_size)
    print(f"Resized image saved as: {output_path}")

if __name__ == "__main__":
    main()
