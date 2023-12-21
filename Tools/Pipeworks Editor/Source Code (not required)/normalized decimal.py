import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
# Initialize RGB and alpha values
r, g, b, a, alpha = 0.5, 0.5, 0.5, 1, 1
alpha_multiplier = 3
use_alternate_mode = False
def main():
    # Function to format a number based on your guidelines
    def format_hex_editor_value(value):
        # Convert to a string with 2 decimal places
        stringval = str(value)
        # If the value is not 0 or 1, ignore the first 0
        if value != 0 and value != 1 and stringval.startswith("0"):
            stringval = stringval[1:]
        
        # Replace each digit with "3{digit}"
        stringval = stringval.replace("3", "33 ").replace("9", "39 ").replace("8", "38 ").replace("7", "37 ").replace("6", "36 ").replace("5", "35 ").replace("4", "34 ").replace("2", "32 ").replace("1", "31 ").replace("0", "30 ").replace(".", " 2E ")
        
        return stringval

    # Function to update the color and display
    def update_color():
        # Create an RGBA image
        size = 350
        image = Image.new("RGBA", (size, size))
        draw = ImageDraw.Draw(image)

        color = (int(r * 255), int(g * 255), int(b * 255), int(alpha * 255))
        draw.ellipse([25, 25, size - 25, size - 25], fill=color)  # Enlarged the circle
        
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo

        # Convert r_val, g_val, b_val to the specified HEX format
        rhex = format(int(r * 255), '02X')
        ghex = format(int(g * 255), '02X')
        bhex = format(int(b * 255), '02X')

        # Update HEX labels under the sliders with the formatted values
        red_hex_label.config(text=f"LO=KA? (Red) Hex: {format_hex_editor_value(r)}")
        green_hex_label.config(text=f"LP=KA? (Green) Hex: {format_hex_editor_value(g)}")
        blue_hex_label.config(text=f"LQ=KA? (Blue) Hex: {format_hex_editor_value(b)}")
        alpha_hex_label.config(text=f"LR=KA? (Alpha) Hex: {format_hex_editor_value(a)}")

        hex_color = f"{rhex} {ghex} {bhex}"
        hex_label.config(text=f"Unsigned Hex Value: {hex_color}")

    # Function to handle sliders and update HEX labels under the sliders
    def update_slider(val, slider):
        global r, g, b, alpha, a
        if slider == "red":
            r = float(val)
            red_hex_label.config(text=f"LO=KA? (Red) Hex: {format_hex_editor_value(r)}")
        elif slider == "green":
            g = float(val)
            green_hex_label.config(text=f"LP=KA? (Green) Hex: {format_hex_editor_value(g)}")
        elif slider == "blue":
            b = float(val)
            blue_hex_label.config(text=f"LQ=KA? (Blue) Hex: {format_hex_editor_value(b)}")
        update_alpha()
        update_color()

    def update_alpha_slider(val):
        global alpha_multiplier, a
        if not use_alternate_mode:
            alpha_multiplier = 1 + (5 - float(val)) * 0.25
        
        a = int(val)
        alpha_hex_label.config(text=f"LR=KA? (Alpha) Hex: {format_hex_editor_value(a)}")
        
        update_alpha()
        update_color()

    def update_alpha():
        global alpha,a
        if not use_alternate_mode:
            alpha = 1 - (r + g + b) / 3
            alpha = 1 - alpha
            alpha = alpha * alpha_multiplier
        else:
            alpha = alpha_multiplier
            alpha = alpha * (0.7**a)

    def toggle_alternate_mode():
        global use_alternate_mode
        use_alternate_mode = alternate_mode_checkbox_var.get()
        update_alpha()
        update_color()

    root = tk.Tk()
    root.title("PWKs Particle Color Visualizer")

    red_slider = tk.Scale(root, label="Red", from_=0, to=1, resolution=0.01, orient="horizontal", command=lambda val: update_slider(val, "red"))
    green_slider = tk.Scale(root, label="Green", from_=0, to=1, resolution=0.01, orient="horizontal", command=lambda val: update_slider(val, "green"))
    blue_slider = tk.Scale(root, label="Blue", from_=0, to=1, resolution=0.01, orient="horizontal", command=lambda val: update_slider(val, "blue"))

    red_slider.set(r)
    green_slider.set(g)
    blue_slider.set(b)

    red_slider.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    green_slider.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    blue_slider.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    red_hex_label = tk.Label(root, text=f"LO=KA? (Red) HEX: {format_hex_editor_value(r)}", width=30)
    green_hex_label = tk.Label(root, text=f"LP=KA? (Green) HEX: {format_hex_editor_value(g)}", width=30)
    blue_hex_label = tk.Label(root, text=f"LQ=KA? (Blue) HEX: {format_hex_editor_value(b)}", width=30)
    alpha_hex_label = tk.Label(root, text=f"LR=KA? (Alpha) Hex: {format_hex_editor_value(a)}", width=30)

    red_hex_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    green_hex_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    blue_hex_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    alpha_hex_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

    canvas = tk.Canvas(root, width=350, height=350)
    canvas.grid(row=0, column=1, rowspan=6, padx=10, pady=10)

    hex_label = tk.Label(root, text="Unsigned Hex Value:")
    hex_label.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

    alpha_slider = tk.Scale(root, label="LR=KA? (Alpha)", from_=1, to=5, resolution=1, orient="horizontal", command=update_alpha_slider)
    alpha_slider.set(alpha_multiplier)
    alpha_slider.grid(row=7, column=0, padx=10, pady=10, sticky="w")

    alternate_mode_checkbox_var = tk.BooleanVar()
    alternate_mode_checkbox = tk.Checkbutton(root, text="Alternate Mode", variable=alternate_mode_checkbox_var, command=toggle_alternate_mode)
    alternate_mode_checkbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    update_alpha()
    update_color()

    root.mainloop()

if __name__ == "__main__":
    main()