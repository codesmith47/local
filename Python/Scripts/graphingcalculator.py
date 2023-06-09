import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main application window
root = tk.Tk()
root.title("Formula Graph")

# Configure the grid layout manager
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a frame to hold the graph
graph_frame = tk.Frame(root)
graph_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a frame to hold the formula and max y inputs
input_frame = tk.Frame(root)
input_frame.grid(row=1, column=0, padx=10, pady=5)

# Define the formulas
formula_1 = tk.StringVar()
formula_2 = tk.StringVar()

# Define the maximum y input
max_y = tk.IntVar()

# Set default values
formula_1.set("1000 * 2 ** (y / 8)")    # Example formula: y
formula_2.set("")                       # Placeholder for 2nd formula
max_y.set(100)                          # Default maximum y

# Define line variables
line1 = None
line2 = None

# Function to format large numbers
def format_number(number):
    units = ['', 'K', 'M', 'B', 'T']
    for unit in units:
        if abs(number) < 1000:
            return f"{number:.1f}{unit}"
        number /= 1000

# Function to calculate XP values based on the formulas and max y
def calculate_xp_values(formula_text, max_level_value):
    if formula_text:
        levels = np.arange(max_level_value + 1)
        xp_function = np.vectorize(lambda y: eval(formula_text.replace('y', str(y))))
        xp_values = xp_function(levels)
        return xp_values
    else:
        return None


# Function to update the graph
def update_graph():
    global line1, line2  # Declare line1 and line2 as global variables

    # Get the formulas and max y from the input fields
    formula_1_text = formula_1.get()
    formula_2_text = formula_2.get()
    max_level_value = max_y.get()

    # Calculate XP values for both formulas if provided
    xp_values_1 = calculate_xp_values(formula_1_text, max_level_value)
    xp_values_2 = calculate_xp_values(formula_2_text, max_level_value)

    # Clear the graph frame
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Create the graph figure
    fig, ax = plt.subplots()
    if xp_values_1 is not None:
        line1, = ax.plot(xp_values_1, label="Formula 1")
    if xp_values_2 is not None:
        line2, = ax.plot(xp_values_2, label="Formula 2")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()

    # Format the y-axis tick labels with shorthand notation
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: format_number(x)))

    # Create the graph canvas
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Function to handle hover event and display y and XP values
    def on_hover(event):
        if event.inaxes == ax:
            x = int(event.xdata)
            if 0 <= x <= max_level_value and x % 1 == 0:
                y_1 = xp_values_1[x] if xp_values_1 is not None else None
                y_2 = xp_values_2[x] if xp_values_2 is not None else None
                if y_1 is not None:
                    y_1_formatted = format_number(y_1)
                else:
                    y_1_formatted = 'None'
                if y_2 is not None:
                    y_2_formatted = format_number(y_2)
                else:
                    y_2_formatted = 'None'
                ax.set_title(f"Y: {x}, (Formula 1): {y_1_formatted}, (Formula 2): {y_2_formatted}")
                fig.canvas.draw_idle()

                # Draw a small circle on top of each line at the hovered point
                if line1 is not None:
                    line1.set_marker('None')
                    line1.set_markevery([x])
                    line1.set_marker('o')
                    line1.set_markersize(5)
                if line2 is not None:
                    line2.set_marker('None')
                    line2.set_markevery([x])
                    line2.set_marker('o')
                    line2.set_markersize(5)
                fig.canvas.draw()

    # Connect the hover event to the graph
    fig.canvas.mpl_connect('motion_notify_event', on_hover)

    # Function to handle window close event
    def on_close():
        root.quit()
        root.destroy()

    # Set the window close event handler
    root.protocol("WM_DELETE_WINDOW", on_close)

# Formula 1 input field
formula_1_label = tk.Label(input_frame, text="Formula 1: ")
formula_1_label.grid(row=0, column=0, padx=5, pady=5)
formula_1_entry = tk.Entry(input_frame, textvariable=formula_1)
formula_1_entry.grid(row=0, column=1, padx=5, pady=5)

# Formula 2 input field
formula_2_label = tk.Label(input_frame, text="Formula 2: ")
formula_2_label.grid(row=1, column=0, padx=5, pady=5)
formula_2_entry = tk.Entry(input_frame, textvariable=formula_2)
formula_2_entry.grid(row=1, column=1, padx=5, pady=5)

# Maximum y input field
max_level_label = tk.Label(input_frame, text="Max Y: ")
max_level_label.grid(row=2, column=0, padx=5, pady=5)
max_level_entry = tk.Entry(input_frame, textvariable=max_y)
max_level_entry.grid(row=2, column=1, padx=5, pady=5)

# Update graph button
update_button = tk.Button(input_frame, text="Update Graph", command=update_graph)
update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Configure the input frame row weights
input_frame.grid_rowconfigure(3, weight=1)

# Initialize the graph
update_graph()

# Start the main application loop
root.mainloop()
