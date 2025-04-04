import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from PIL import Image, ImageTk  

# Pricing dictionary
PRICES = {'Small': 8, 'Medium': 10, 'Large': 12, 'Breadsticks': 5, 'Tater Tots': 5, 'Mac': 5}
TOPPINGS = [
    "Cheesy Goodness", "Bacon", "Broccoli", "Peppers",
    "Onion", "Mushrooms", "Black Olives", "Sausage", "Pepperoni"
]
SIDES = ["Breadsticks", "Tater Tots", "Mac"]

class PizzaZamboniApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Zamboni Menu")
        self.root.geometry("800x500")  
        self.root.configure(bg='#1e1e1e')

        self.orders = []
        self.current_order = {"name": "", "size": None, "toppings": [], "side": None}

        self.show_welcome_screen()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_welcome_screen(self):
        self.clear_window()
        try:
            image = Image.open("pizzaZamboni.png")
            image = image.resize((500, 500), Image.LANCZOS)
            self.welcome_image = ImageTk.PhotoImage(image)
            ttk.Label(self.root, image=self.welcome_image, background="#1e1e1e").pack(pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")
        
        ttk.Label(self.root, text="Welcome to Pizza Zamboni!", font=("Arial", 18), foreground="white", background="#1e1e1e").pack(pady=10)
        ttk.Button(self.root, text="Click here to Place Order", command=self.create_widgets, style='success.TButton').pack(pady=20)
    
    def create_widgets(self):
        self.clear_window()
        ttk.Label(self.root, text="Enter Your Name:", foreground="white", background="#1e1e1e").pack(pady=5)
        self.name_entry = ttk.Entry(self.root, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        ttk.Label(self.root, text="Select Pizza Size:", foreground="white", background="#1e1e1e").pack(pady=5)
        self.size_var = tk.StringVar()
        self.size_buttons = []
        for size in ['Small', 'Medium', 'Large']:
            btn = ttk.Button(self.root, text=size, command=lambda s=size: self.select_size(s), style='secondary.TButton')
            btn.pack(pady=2, fill='x', padx=20)
            self.size_buttons.append((btn, size))

        ttk.Label(self.root, text="Select Toppings:", foreground="white", background="#1e1e1e").pack(pady=5)
        self.topping_vars = {}
        toppings_frame = ttk.Frame(self.root)
        toppings_frame.pack()
        for i, topping in enumerate(TOPPINGS):
            var = tk.BooleanVar()
            btn = ttk.Button(toppings_frame, text=topping, command=lambda t=topping: self.toggle_topping(t), style='secondary.TButton')
            btn.grid(row=i//3, column=i%3, padx=5, pady=2)
            self.topping_vars[topping] = (var, btn)

        ttk.Label(self.root, text="Select Sides:", foreground="white", background="#1e1e1e").pack(pady=5)
        self.side_buttons = {}
        sides_frame = ttk.Frame(self.root)
        sides_frame.pack()
        for i, side in enumerate(SIDES):
            btn = ttk.Button(sides_frame, text=side, command=lambda s=side: self.toggle_side(s), style='secondary.TButton')
            btn.grid(row=0, column=i, padx=5, pady=2)
            self.side_buttons[side] = btn

        ttk.Button(self.root, text="Add Pizza", command=self.add_pizza, style='primary.TButton').pack(pady=5)
        ttk.Button(self.root, text="Complete Order", command=self.confirm_order, style='danger.TButton').pack(pady=5)
    
    def toggle_topping(self, topping):
        var, btn = self.topping_vars[topping]
        var.set(not var.get())
        btn.configure(style='primary.TButton' if var.get() else 'secondary.TButton')
        if var.get():
            self.current_order['toppings'].append(topping)
        else:
            self.current_order['toppings'].remove(topping)

    def toggle_side(self, side):
        if self.current_order['side'] == side:
            self.current_order['side'] = None
            self.side_buttons[side].configure(style='secondary.TButton')
        else:
            self.current_order['side'] = side
            for s, btn in self.side_buttons.items():
                btn.configure(style='primary.TButton' if s == side else 'secondary.TButton')

    def select_size(self, size):
        self.current_order['size'] = size
        for btn, s in self.size_buttons:
            btn.configure(style='primary.TButton' if s == size else 'secondary.TButton')

    def add_pizza(self):
        if not self.name_entry.get().strip():
            messagebox.showerror("Error", "Please enter your name before adding a pizza.")
            return
        
        self.current_order["name"] = self.name_entry.get()
        self.orders.append(self.current_order.copy())
        self.current_order = {"name": self.name_entry.get(), "size": None, "toppings": [], "side": None}
        self.create_widgets()

    def confirm_order(self):
        customer_name = self.name_entry.get()
        self.clear_window()
        summary_text = f"Thank you {customer_name}, your order is complete!\n\n"
        total_price = 0
        for order in self.orders:
            summary_text += f"Pizza Size: {order['size']} - ${PRICES.get(order['size'], 0)}\n"
            total_price += PRICES.get(order['size'], 0)
            if order['toppings']:
                summary_text += "Toppings: " + ", ".join(order['toppings']) + "\n"
            if order['side']:
                summary_text += f"Side: {order['side']} - ${PRICES.get(order['side'], 0)}\n"
                total_price += PRICES.get(order['side'], 0)
            summary_text += "\n"
        summary_text += f"Total Price: ${total_price}\n"
        
        ttk.Label(self.root, text=summary_text, foreground="white", background="#1e1e1e", font=("Arial", 12)).pack(pady=20)
        ttk.Button(self.root, text="Back", command=self.create_widgets, style='success.TButton').pack(pady=10)

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = PizzaZamboniApp(root)
    root.mainloop()
