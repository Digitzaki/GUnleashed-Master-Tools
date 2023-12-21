import tkinter as tk

def main():
# Validate the RGB values to be in the range 0.00 - 1.00
    def validate_rgb_input(P):
        try:
            if not P:
                return True
            value = float(P)
            return 0.00 <= value <= 1.00
        except ValueError:
            return False

    # Function to create sliders for RGB colors
    def create_sliders(gradient_value, text_box):
        gradient_colors = int(gradient_value)
        
        # Clear previous sliders and labels
        for widget in sliders_frame.winfo_children():
            widget.destroy()

        # Calculate the number of existing RGB variables
        existing_rgb_count = len(rgb_vars)
        
        for i in range(gradient_colors):
            seg_num = i + 1
            seg_label = tk.Label(sliders_frame, text=f"(Stage {seg_num}) R: ", anchor="e")
            seg_label.grid(row=i, column=0, padx=5, pady=5)

            if i < existing_rgb_count // 3:
                # Use the existing RGB variables for existing segments
                r_var = rgb_vars[i * 3]
                g_var = rgb_vars[i * 3 + 1]
                b_var = rgb_vars[i * 3 + 2]
            else:
                # Create new RGB variables for new segments
                r_var = tk.DoubleVar()
                g_var = tk.DoubleVar()
                b_var = tk.DoubleVar()
                r_var.set(0.50)  # Default value
                g_var.set(0.50)  # Default value
                b_var.set(0.50)  # Default value
                r_var.index = i  # Assign an index to each RGB variable
                g_var.index = i
                b_var.index = i

            r_entry = tk.Entry(sliders_frame, width=8, textvariable=r_var, validate="key", validatecommand=(validate_rgb_input, '%P'))
            r_entry.grid(row=i, column=1)

            g_label = tk.Label(sliders_frame, text="G: ", anchor="e")
            g_label.grid(row=i, column=2, padx=5, pady=5)
            g_entry = tk.Entry(sliders_frame, width=8, textvariable=g_var, validate="key", validatecommand=(validate_rgb_input, '%P'))
            g_entry.grid(row=i, column=3)

            b_label = tk.Label(sliders_frame, text="B: ", anchor="e")
            b_label.grid(row=i, column=4, padx=5, pady=5)
            b_entry = tk.Entry(sliders_frame, width=8, textvariable=b_var, validate="key", validatecommand=(validate_rgb_input, '%P'))
            b_entry.grid(row=i, column=5)

            if i >= existing_rgb_count // 3:
                # Append new RGB variables to the list
                rgb_vars.extend((r_var, g_var, b_var))

            # Bind the <FocusOut> event to update colors in real-time
            r_entry.bind("<FocusOut>", lambda event, tb=text_box: update_colors(event, tb))
            g_entry.bind("<FocusOut>", lambda event, tb=text_box: update_colors(event, tb))
            b_entry.bind("<FocusOut>", lambda event, tb=text_box: update_colors(event, tb))

            # Bind the <KeyRelease> event to update colors in real-time when text box values change
            r_entry.bind("<KeyRelease>", lambda event, tb=text_box: update_colors(event, tb))
            g_entry.bind("<KeyRelease>", lambda event, tb=text_box: update_colors(event, tb))
            b_entry.bind("<KeyRelease>", lambda event, tb=text_box: update_colors(event, tb))

        # Call the function to create the rectangles and update colors
        create_rectangles(gradient_colors)
        update_colors(None, text_box)  # Update colors immediately when sliders are created

    # Function to create the rectangles
    def create_rectangles(gradient_colors):
        canvas.delete("rectangle")
        canvas.update_idletasks()  # Update the canvas to get the correct width
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        rectangle_count = gradient_colors

        # Calculate the maximum width of the rectangles to fit within the window
        max_rectangle_width = canvas_width / rectangle_count
        rectangle_width = min(max_rectangle_width, canvas_width)  # Ensure it fits within the window
        rectangle_height = canvas_height
        outline_width = 1  # Width of the outline for rectangles

        for i in range(rectangle_count):
            r = float(rgb_vars[i * 3].get())
            g = float(rgb_vars[i * 3 + 1].get())
            b = float(rgb_vars[i * 3 + 2].get())
            fill_color = f"#{int(255 * r):02X}{int(255 * g):02X}{int(255 * b):02X}"
            outline_color = "black"  # Outline color

            # Calculate the position for centering the rectangles
            rectangle_x = (canvas_width - (rectangle_count * rectangle_width)) / 2 + i * rectangle_width
            canvas.create_rectangle(rectangle_x,0,rectangle_x + rectangle_width,rectangle_height,fill=fill_color,outline=outline_color,width=outline_width,tags="rectangle")

    def format_hex_editor_value(value):
        # Convert to a string with 2 decimal places
        stringval = str(value)

        # If the value is not 0 or 1, ignore the first 0
        if value != 0 and value != 1 and stringval.startswith("0"):
            stringval = stringval[1:]

        # Replace each digit with "3{digit}"
        stringval = stringval.replace("3", "33 ").replace("9", "39 ").replace("8", "38 ").replace("7", "37 ").replace("6", "36 ").replace("5", "35 ").replace("4", "34 ").replace("2", "32 ").replace("1", "31 ").replace("0", "30 ").replace(".", "2E ")
        stringval = stringval.strip('[]')

        # Split the string into parts using ","
        parts = stringval.split(', ')

        # Initialize a list to store the filtered parts
        filtered_parts = [parts[0]]

        if parts:
            # Iterate through the parts and find the last consecutive part
            last_consecutive_index = len(parts) - 1
            for i in range(len(parts) - 2, -1, -1):
                if parts[i] == parts[i + 1]:
                    last_consecutive_index = i
                else:
                    break

            # Add the non-consecutive parts to the filtered_parts
            filtered_parts.extend(parts[1:last_consecutive_index + 1])

        result = ', '.join(filtered_parts)

        return result

    def update_colors(event, text_box):
        create_rectangles(int(gradient_slider.get()))

        # Filter the RGB values for active segments
        active_rgb_vars = [rgb_var for rgb_var in rgb_vars if rgb_var.index < int(gradient_slider.get())]

        text_box.config(state=tk.NORMAL)
        text_box.delete("1.0", tk.END)  # Clear the text

        red_values = [format_value(active_rgb_vars[i * 3].get()) for i in range(len(active_rgb_vars) // 3)]
        green_values = [format_value(active_rgb_vars[i * 3 + 1].get()) for i in range(len(active_rgb_vars) // 3)]
        blue_values = [format_value(active_rgb_vars[i * 3 + 2].get()) for i in range(len(active_rgb_vars) // 3)]
        r = len(format_hex_editor_value(red_values).replace("'","").replace(" ",""))
        g = len(format_hex_editor_value(green_values).replace("'","").replace(" ",""))
        b = len(format_hex_editor_value(blue_values).replace("'","").replace(" ",""))
        # Format the values as one string without brackets and spaces
        text_box.insert(tk.END, f"LO={'KA' if 2 <= r <= 6 else 'KE'}? (R): " + ''.join(map(str, format_hex_editor_value(red_values))).strip("[]'").replace(",", '').replace("'", '').replace("  ", " 20 ")  + "\n")
        text_box.insert(tk.END, f"LP={'KA' if 2 <= g <= 6 else 'KE'}? (G): " + ''.join(map(str, format_hex_editor_value(green_values))).strip("[]'").replace(",", '').replace("'", '').replace("  ", " 20 ")  + "\n")
        text_box.insert(tk.END, f"LQ={'KA' if 2 <= b <= 6 else 'KE'}? (B): " + ''.join(map(str, format_hex_editor_value(blue_values))).strip("[]'").replace(",", '').replace("'", '').replace("  ", " 20 ")  + "\n")
        
        text_box.config(state=tk.DISABLED)

    def format_value(value):
        formatted_value = f"{value:.2f}"  # Display two decimal places

        # Remove initial zero and unnecessary trailing zeros
        if formatted_value.startswith("0.") or formatted_value == "0.00":
            formatted_value = formatted_value[1:]
            if formatted_value.endswith("0"):
                formatted_value = formatted_value[:-1]
        
        return "1" if formatted_value == "1.00" else ("0" if formatted_value == ".0" else formatted_value)

    # Create a main window
    root = tk.Tk()
    root.title("Pipeworks Gradient Visualizer")
    root.geometry("825x465")  # Set the initial window size

    # Create a canvas for the rectangle
    canvas = tk.Canvas(root, width=800, height=50)
    canvas.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

    # Create a slider for the gradient amount
    gradient_slider = tk.Scale(root, label="Gradient Amount", from_=2, to=6, orient="horizontal", command=lambda x: create_sliders(gradient_slider.get(), text_box2))
    gradient_slider.set(2)
    gradient_slider.grid(row=1, column=0, columnspan=6, padx=10, pady=10)

    # Create a frame for sliders
    sliders_frame = tk.Frame(root)
    sliders_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

    # Create a list to store RGB entry variables
    rgb_vars = []

    # Add non-editable text boxes under the rectangle
    text_box1 = tk.Text(root, height=10, width=25)
    text_box1.insert(tk.END, "Usage Tips: \n - Slider: Segments \n - LO=KE? = RED\n - LP=KE? = GREEN\n - LQ=KE? = BLUE\n - LR=KE? (Unsupported)\n(Particle Color Lifetime)\n (Fades smoothly ingame)\n\n!Use 0 - 1 (up to 1.00)!")
    text_box1.config(state=tk.DISABLED)
    text_box1.grid(row=1, column=0, padx=5, pady=5)

    # Create a larger text box for "Text Box 2"
    text_box2 = tk.Text(root, height=10, width=25, wrap=tk.WORD)
    text_box2.insert(tk.END, "")
    text_box2.config(state=tk.DISABLED)
    text_box2.grid(row=1, column=5, padx=5, pady=5)

    create_sliders(2, text_box2)

    # Start the main loop for tkinter
    root.mainloop()

if __name__ == "__main__":
    main()