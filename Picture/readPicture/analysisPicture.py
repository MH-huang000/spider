import pytesseract
import pandas as pd
import os
from PIL import Image

# Specify the directory containing the images
image_dir = '.\image'  # Replace with the actual directory path

# Iterate over the image files in the directory
for filename in os.listdir(image_dir):
    image_path = os.path.join(image_dir, filename)

    # Read the image
    image = pytesseract.image_to_string(Image.open(image_path),lang='chi_sim+eng')


    # Extract the image name without extension
    image_name, _ = os.path.splitext(filename)

    # Save the extracted text to a .txt file with the image name as the filename
    with open(f'{image_name}.txt', 'w', encoding='utf-8') as text_file:
        text_file.write(image)