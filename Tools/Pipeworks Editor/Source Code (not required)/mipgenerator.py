from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog

def main():
    def generate_mipmaps(image_path, output_folder, mipmap_level):
        # Open the original image
        image = Image.open(image_path)

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Get the image's base name and extension
        base_name, extension = os.path.splitext(os.path.basename(image_path))

        # Generate mipmaps
        mipmaps = []
        mipmaps.append(image_path)  # Add the original image

        for i in range(1, mipmap_level + 1):
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

    def select_input_folder():
        global input_folder
        input_folder = filedialog.askdirectory()
        input_folder_entry.delete(0, tk.END)
        input_folder_entry.insert(0, input_folder)

    def select_output_folder():
        global output_folder
        output_folder = filedialog.askdirectory()
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, output_folder)

    def generate_mipmaps_for_selected_input():
        if not input_folder or not output_folder:
            return
        mipmap_level = int(mipmap_level_entry.get())
        output_text.delete(1.0, tk.END)  # Clear the output text

        # Create a single "mips" subfolder within the selected output folder
        first_mips_folder = os.path.join(output_folder, "mips")
        os.makedirs(first_mips_folder, exist_ok=True)

        # Iterate through the subfolders and files in the input directory
        for root, dirs, files in os.walk(input_folder):
            for filename in files:
                if filename.endswith(".png"):
                    image_path = os.path.join(root, filename)

                    # Create a "mips" subfolder within the current subfolder
                    output_subfolder = os.path.join(first_mips_folder, os.path.relpath(root, input_folder), "mips")
                    os.makedirs(output_subfolder, exist_ok=True)

                    # Generate mipmaps within the subfolder
                    mipmaps = generate_mipmaps(image_path, output_subfolder, mipmap_level)
                    result = f"Generated mipmaps for {filename} up to level {mipmap_level}:\n{', '.join(mipmaps)}\n\n"
                    output_text.insert(tk.END, result)

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Mipmap Generator")
    root.geometry("635x300")  # Set the window size

    # Create and configure the input folder label and entry
    input_folder_label = tk.Label(root, text="Input Folder:")
    input_folder_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
    input_folder_entry = tk.Entry(root)
    input_folder_entry.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    input_folder_button = tk.Button(root, text="Select Input Folder", command=select_input_folder)
    input_folder_button.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

    # Create and configure the output folder label and entry
    output_folder_label = tk.Label(root, text="Output Folder:")
    output_folder_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
    output_folder_entry = tk.Entry(root)
    output_folder_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
    output_folder_button = tk.Button(root, text="Select Output Folder", command=select_output_folder)
    output_folder_button.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

    # Create and configure the mipmap level label and entry
    mipmap_level_label = tk.Label(root, text="Mipmap Level (1-6):")
    mipmap_level_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
    mipmap_level_entry = tk.Entry(root)
    mipmap_level_entry.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

    # Create and configure the generate button
    generate_button = tk.Button(root, text="Generate Mipmaps", command=generate_mipmaps_for_selected_input)
    generate_button.grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

    # Create and configure the output text box on the right
    output_text = tk.Text(root, wrap=tk.WORD, width=40, height=15)
    output_text.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
