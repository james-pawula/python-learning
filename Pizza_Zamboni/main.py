import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from PIL import Image, ImageTk

# Pricing
PRICES = {
    'Small': 8,
    'Medium': 10,
    'Large': 12,
    'Breadsticks': 5,
    'Tater Tots': 5,
    'Mac': 5,
    'Wings': 6
}
PIZZA_TYPES = ["Deep Dish", "Pan", "Thin Crust", "New York Style", "Stuffed Crust"]
TOPPINGS = [
    "Cheesy Goodness", "Bacon", "Broccoli", "Peppers",
    "Onion", "Mushrooms", "Black Olives", "Sausage", "Pepperoni", "Pineapple"
]
SIDES = ["Breadsticks", "Tater Tots", "Mac", "Wings"]
WING_FLAVORS = ["Plain", "BBQ", "Mild", "Super Ranchy", "Buffalo"]

class PizzaZamboniApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Zamboni Menu")
        self.root.geometry("1020x650")
        self.root.configure(bg='#1e1e1e')

        # Load images
        self.pizza_base = Image.open("img/base_pizza.png").resize((300,300),Image.LANCZOS).convert("RGBA")
        self.topping_images = {}
        for topping in TOPPINGS:
            path = f"img/toppings/{topping.replace(' ', '_')}.png"
            try:
                img = Image.open(path).resize((300,300),Image.LANCZOS).convert("RGBA")
                self.topping_images[topping] = img
            except FileNotFoundError:
                print(f"Missing topping image: {path}")

        self.orders = []
        self.current_order = {"name":"","type":None,"size":None,
                              "toppings":[],"sides":[],"wings_flavor":None}
        self.total_var = tk.StringVar(value="Total: $0")
        self.preview_imgtk = None
        self.show_welcome_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_window()
        try:
            img = Image.open("img/pizzaZamboni.png").resize((600,400),Image.LANCZOS)
            self.welcome_image = ImageTk.PhotoImage(img)
            ttk.Label(self.root, image=self.welcome_image, background="#1e1e1e").pack(pady=20)
        except Exception as e:
            print(e)
        ttk.Label(self.root, text="Welcome to Pizza Zamboni!", font=("Arial",18),
                  foreground="white", background="#1e1e1e").pack(pady=10)
        ttk.Button(self.root, text="Click here to Place Order",
                   command=self.create_widgets, style='success.TButton').pack(pady=20)

    def create_widgets(self):
        self.clear_window()
        self.total_var.set("Total: $0")

        main = tk.Frame(self.root, bg='#1e1e1e')
        main.pack(fill='both', expand=True, padx=10, pady=10)
        left = tk.Frame(main, bg='#1e1e1e')
        left.pack(side='left', fill='y', padx=(0,20))
        right = tk.Frame(main, bg='#1e1e1e')
        right.pack(side='right', fill='both', expand=True)

        # Name Entry
        ttk.Label(left, text="Enter Your Name:", foreground="white", background="#1e1e1e").pack(pady=5)
        self.name_entry = ttk.Entry(left, font=("Arial",14))
        self.name_entry.pack(pady=5)

        # Preview
        self.preview_label = ttk.Label(right, background="#1e1e1e")
        self.preview_label.place(relx=0.5, rely=0.5, anchor='center')
        self.update_preview()

        # Pizza Type
        ttk.Label(left, text="Select Pizza Type:", foreground="white", background="#1e1e1e").pack(pady=5)
        self.type_buttons = []
        type_frame = tk.Frame(left, bg='#1e1e1e')
        type_frame.pack(pady=5)
        for idx, ptype in enumerate(PIZZA_TYPES):
            btn = ttk.Button(type_frame, text=ptype, style='secondary.TButton')
            btn.grid(row=0, column=idx, padx=5)
            btn.bind('<Button-1>', lambda e, t=ptype: self.select_button(t, self.type_buttons, 'type'))
            self.type_buttons.append((btn, ptype))

        # Pizza Size
        ttk.Label(left, text="Select Pizza Size:", foreground="white", background="#1e1e1e").pack(pady=5)
        self.size_buttons = []
        size_frame = tk.Frame(left, bg='#1e1e1e')
        size_frame.pack(pady=5)
        for idx, size in enumerate(['Small','Medium','Large']):
            btn = ttk.Button(size_frame, text=size, style='secondary.TButton')
            btn.grid(row=0, column=idx, padx=5)
            btn.bind('<Button-1>', lambda e, s=size: self.select_button(s, self.size_buttons, 'size'))
            self.size_buttons.append((btn, size))

        # Toppings
        ttk.Label(left, text="Select Toppings:", foreground="white", background="#1e1e1e").pack(pady=5)
        self.topping_vars = {}
        toppings_frame = tk.Frame(left, bg='#1e1e1e')
        toppings_frame.pack()
        for i, topping in enumerate(TOPPINGS):
            var = tk.BooleanVar()
            btn = ttk.Button(toppings_frame, text=topping, style='secondary.TButton')
            btn.grid(row=i//3, column=i%3, padx=5, pady=2)
            btn.bind('<Button-1>', lambda e, t=topping: self.toggle_topping(t))
            self.topping_vars[topping] = (var, btn)

        # Sides
        ttk.Label(left, text="Select Sides:", foreground="white", background="#1e1e1e").pack(pady=5)
        self.side_vars = {}
        self.wings_flavor = tk.StringVar(value="Plain")
        sides_frame = tk.Frame(left, bg='#1e1e1e')
        sides_frame.pack()
        for i, side in enumerate(SIDES):
            var = tk.BooleanVar()
            btn = ttk.Button(sides_frame, text=side, style='secondary.TButton')
            btn.grid(row=0, column=i*2, padx=5, pady=2)
            btn.bind('<Button-1>', lambda e, s=side: self.toggle_side(s))
            self.side_vars[side] = (var, btn)
            if side == 'Wings':
                combo = ttk.Combobox(sides_frame, values=WING_FLAVORS, textvariable=self.wings_flavor, state='readonly', width=12)
                combo.grid(row=0, column=i*2+1, padx=5)
                combo.grid_remove()
                self.wings_combobox = combo

        # Total and Actions
        ttk.Label(left, textvariable=self.total_var, font=("Arial",14), foreground="white", background="#1e1e1e").pack(pady=10)
        ttk.Button(left, text="Add Pizza", command=self.add_pizza, style='primary.TButton').pack(pady=5)
        ttk.Button(left, text="Complete Order", command=self.confirm_order, style='danger.TButton').pack()

    def update_preview(self):
        composite = self.pizza_base.copy()
        toppings = self.current_order['toppings'][:]
        if "Cheesy Goodness" in toppings:
            toppings.remove("Cheesy Goodness")
            toppings.insert(0, "Cheesy Goodness")
        for topping in toppings:
            overlay = self.topping_images.get(topping)
            if overlay:
                composite = Image.alpha_composite(composite, overlay)
        self.preview_imgtk = ImageTk.PhotoImage(composite)
        self.preview_label.config(image=self.preview_imgtk)

    def toggle_topping(self, topping):
        var, btn = self.topping_vars[topping]
        selected = not var.get()
        var.set(selected)
        btn.config(style='primary.TButton' if selected else 'secondary.TButton')
        if selected:
            self.current_order['toppings'].append(topping)
        else:
            self.current_order['toppings'].remove(topping)
        self.update_preview()

    def toggle_side(self, side):
        var, btn = self.side_vars[side]
        selected = not var.get()
        var.set(selected)
        btn.config(style='primary.TButton' if selected else 'secondary.TButton')
        if selected:
            self.current_order['sides'].append(side)
            if side == 'Wings':
                self.wings_combobox.grid()
        else:
            self.current_order['sides'].remove(side)
            if side == 'Wings':
                self.wings_combobox.grid_remove()
        self.update_total()

    def select_button(self, value, button_list, field):
        self.current_order[field] = value
        for btn, val in button_list:
            btn.config(style='primary.TButton' if val == value else 'secondary.TButton')
        self.update_total()

    def update_total(self):
        total = 0
        if self.current_order['size']:
            total += PRICES.get(self.current_order['size'], 0)
        for sd in self.current_order['sides']:
            total += PRICES.get(sd, 0)
        self.total_var.set(f"Total: ${total}")

    def add_pizza(self):
        name = self.name_entry.get().strip()
        if not name:
            return messagebox.showerror("Missing Name", "Please enter your name before adding a pizza.")
        self.current_order['name'] = name
        if 'Wings' in self.current_order['sides']:
            self.current_order['wings_flavor'] = self.wings_flavor.get()
        self.orders.append(self.current_order.copy())
        self.current_order = {"name":name, "type":None, "size":None, "toppings":[], "sides":[], "wings_flavor":None}
        self.create_widgets()

    def confirm_order(self):
        if not self.orders:
            return messagebox.showerror("No Order", "Please add at least one pizza before completing the order.")
        self.clear_window()
        summary = ""
        total_price = 0
        for ord in self.orders:
            summary += f"{ord['name']} ordered:\n"
            summary += f"Type: {ord['type']}\n"
            summary += f"Size: {ord['size']} - ${PRICES.get(ord['size'], 0)}\n"
            total_price += PRICES.get(ord['size'], 0)
            if ord['toppings']:
                summary += "Toppings: " + ", ".join(ord['toppings']) + "\n"
            for sd in ord['sides']:
                price = PRICES.get(sd, 0)
                flavor = f" ({ord['wings_flavor']})" if sd == 'Wings' else ''
                summary += f"Side: {sd}{flavor} - ${price}\n"
                total_price += price
            summary += "\n"
        summary += f"Total Price: ${total_price}\n"
        ttk.Label(self.root, text=summary, font=("Arial",12), foreground="white", background="#1e1e1e").pack(pady=20)
        ttk.Button(self.root, text="Back", command=self.create_widgets, style='success.TButton').pack(pady=5)
        ttk.Button(self.root, text="Place Order", command=self.show_final_message, style='primary.TButton').pack(pady=5)

    def show_final_message(self):
        messagebox.showinfo("Order Placed", "Thank you for ordering at Pizza Zamboni! We will get that started right away.")

if __name__ == "__main__":
    root = tb.Window(themename='darkly')
    app = PizzaZamboniApp(root)
    root.mainloop()
