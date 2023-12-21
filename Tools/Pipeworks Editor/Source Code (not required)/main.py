import tkinter as tk
import os

print ("Loading... (Console is for Error Handling, Minimize this Window if you'd like!)")
# Get the directory of the main script
current_directory = os.path.dirname(os.path.abspath(__file__))

def open_color_visualizer():
    try:
        os.system(f'python "{os.path.join(current_directory, "normalized decimal.py")}"')
    except FileNotFoundError:
        print("Error: 'normalized_decimal.py' not found.")

def open_gradient_visualizer():
    try:
        os.system(f'python "{os.path.join(current_directory, "gradient.py")}"')
    except FileNotFoundError:
        print("Error: 'gradient.py' not found.")

def open_generator():
    try:
        os.system(f'python "{os.path.join(current_directory, "mipgenerator.py")}"')
    except FileNotFoundError:
        print("Error: 'mipgenerator.py' not found.")

# Create the main window
root = tk.Tk()
root.title("PWKs Editor Version 1.21")
root.geometry("320x200")

# Create and configure the buttons
color_button = tk.Button(root, text="Color Visualizer", command=open_color_visualizer)
gradient_button = tk.Button(root, text="Gradient Visualizer", command=open_gradient_visualizer)
generator_button = tk.Button(root, text="Mipmap Generator", command=open_generator)

color_button.pack(pady=15)
gradient_button.pack(pady=15)
generator_button.pack(pady=15)

# Start the main loop
print ("Editor Loaded!")
root.mainloop()
