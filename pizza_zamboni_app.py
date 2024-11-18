import tkinter as tk
from tkinter import messagebox

def calculate_cost():
    # Get selected size
    size = size_var.get()
    if not size:  # Check if size is selected
        messagebox.showerror("Error", "Please select a pizza size.")
        return
    
    # Get selected base pizza
    base = base_var.get()
    if not base:  # Check if base is selected
        messagebox.showerror("Error", "Please select a pizza type.")
        return
    
    # Get selected toppings
    selected_toppings = [topping for topping, var in toppings_vars.items() if var.get()]
    toppings_message = ", ".join(selected_toppings) if selected_toppings else "no toppings"
    
    # Display the order summary
    user_name = name_entry.get().strip()
    if not user_name:  # Ensure name is entered
        messagebox.showerror("Error", "Please enter your name.")
        return
    
    cost = {"Small": 3, "Medium": 4, "Large": 5}[size]
    messagebox.showinfo(
        "Order Summary",
        f"Thank you, {user_name}!\nYou ordered a {size} {base} pizza with {toppings_message}.\n"
        f"The cost is ${cost}.\nIt will take 5 minutes to get ready. Enjoy!"
    )

# Initialize the GUI window
root = tk.Tk()
root.title("Pizza Zamboni")

# Configure grid to be scalable
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# User name
tk.Label(root, text="Enter your name:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

# Pizza base selection
tk.Label(root, text="Choose your pizza type:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
base_var = tk.StringVar(value="")  # No default selection
bases = ["Cheese", "Pepperoni", "Sausage"]
for i, base in enumerate(bases, start=2):
    tk.Radiobutton(root, text=base, variable=base_var, value=base).grid(row=i, column=1, sticky="w", padx=10)

# Toppings selection
tk.Label(root, text="Choose your toppings:").grid(row=5, column=0, sticky="w", padx=10, pady=10)
toppings = [
    "Mushroom", "Broccoli", "Tomato", "Black Olives", 
    "Pineapple", "Bacon", "Cheesey Goodness"
]
toppings_vars = {topping: tk.BooleanVar(value=False) for topping in toppings}  # All unchecked by default
for i, topping in enumerate(toppings, start=6):
    tk.Checkbutton(root, text=topping, variable=toppings_vars[topping]).grid(row=i, column=1, sticky="w", padx=10)

# Pizza size selection
tk.Label(root, text="Choose your pizza size:").grid(row=13, column=0, sticky="w", padx=10, pady=10)
size_var = tk.StringVar(value="")  # No default selection
sizes = ["Small", "Medium", "Large"]
for i, size in enumerate(sizes, start=14):
    tk.Radiobutton(root, text=size, variable=size_var, value=size).grid(row=i, column=1, sticky="w", padx=10)

# Submit button
submit_button = tk.Button(root, text="Place Order", command=calculate_cost)
submit_button.grid(row=18, column=0, columnspan=2, pady=20, sticky="ew")

# Expand window and make it scalable
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)

# Run the GUI loop
root.mainloop()
