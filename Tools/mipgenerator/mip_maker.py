# Follow the read me to set up and use.

from PIL import Image
import os

def generate_mipmaps(image_path, output_folder):
    # Open the original image
    image = Image.open(image_path)

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get the image's base name and extension
    base_name, extension = os.path.splitext(os.path.basename(image_path))

    # Generate mipmaps
    mipmaps = []
    mipmaps.append(image_path)  # Add the original image

    for i in range(1, 4):
        # Resize the image for the next mipmap
        width = max(1, int(image.width * 0.5))
        height = max(1, int(image.height * 0.5))
        image = image.resize((width, height), Image.LANCZOS)

        # Save the mipmap with the appropriate name in the output folder
        mip_name = f"{base_name}_mip{i}{extension}"
        output_path = os.path.join(output_folder, mip_name)
        image.save(output_path)
        mipmaps.append(output_path)

    return mipmaps

# Provide the path to the input and output folders
input_folder = r'[input folder path goes here]'
output_folder = r'[output folder path goes here]'

# Process each PNG file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        image_path = os.path.join(input_folder, filename)

        mipmaps = generate_mipmaps(image_path, output_folder)
        print(f"Generated mipmaps for {filename}: {mipmaps}")