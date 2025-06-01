import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from PIL import Image, ImageTk

# Pricing
PRICES = {'Small': 8, 'Medium': 10, 'Large': 12,
          'Breadsticks': 5, 'Tater Tots': 5, 'Mac': 5, 'Wings': 6}
PIZZA_TYPES = ["Deep Dish", "Pan", "Thin Crust", "New York Style"]
TOPPINGS = [
    "Cheesy Goodness", "Bacon", "Broccoli", "Peppers",
    "Onion", "Mushrooms", "Black Olives", "Sausage", "Pepperoni", "Pineapple"
]
SIDES = ["Breadsticks", "Tater Tots", "Mac", "Wings"]
WING_FLAVORS = ["Plain", "BBQ", "Mild", "Super Ranchy"]

class PizzaZamboniApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Zamboni Menu")
        self.root.geometry("820x650")
        self.root.configure(bg='#1e1e1e')

        self.orders = []
        self.current_order = {
            "name": "", "type": None, "size": None,
            "toppings": [], "sides": [], "wings_flavor": None
        }
        self.total_var = tk.StringVar(value="Total: $0")
        self.show_welcome_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_window()
        try:
            image = Image.open("img/pizzaZamboni.png")
            image = image.resize((600, 400), Image.LANCZOS)
            self.welcome_image = ImageTk.PhotoImage(image)
            ttk.Label(self.root, image=self.welcome_image, background="#1e1e1e").pack(pady=20)
        except Exception as e:
            print(f"Error loading image: {e}")

        ttk.Label(
            self.root,
            text="Welcome to Pizza Zamboni!",
            font=("Arial", 18),
            foreground="white",
            background="#1e1e1e"
        ).pack(pady=10)
        ttk.Button(
            self.root,
            text="Click here to Place Order",
            command=self.create_widgets,
            style='success.TButton'
        ).pack(pady=20)

    def create_widgets(self):
        self.clear_window()
        self.total_var.set("Total: $0")

        # Customer name
        ttk.Label(
            self.root, text="Enter Your Name:",
            foreground="white", background="#1e1e1e"
        ).pack(pady=5)
        self.name_entry = ttk.Entry(self.root, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        # Pizza type
        ttk.Label(
            self.root, text="Select Pizza Type:",
            foreground="white", background="#1e1e1e"
        ).pack(pady=5)
        self.type_buttons = []
        type_frame = ttk.Frame(self.root)
        type_frame.pack(pady=5)
        for i, ptype in enumerate(PIZZA_TYPES):
            btn = ttk.Button(type_frame, text=ptype, style='secondary.TButton')
            btn.grid(row=0, column=i, padx=10)
            btn.bind(
                "<Button-1>",
                lambda e, t=ptype: self.select_button(t, self.type_buttons, 'type', 18)
            )
            self.add_hover_effect(btn, hover_scale=17)
            self.type_buttons.append((btn, ptype))

        # Pizza size
        ttk.Label(
            self.root, text="Select Pizza Size:",
            foreground="white", background="#1e1e1e"
        ).pack(pady=5)
        self.size_buttons = []
        size_frame = ttk.Frame(self.root)
        size_frame.pack(pady=5)
        for i, size in enumerate(['Small', 'Medium', 'Large']):
            btn = ttk.Button(size_frame, text=size, style='secondary.TButton')
            btn.grid(row=0, column=i, padx=10)
            btn.bind(
                "<Button-1>",
                lambda e, s=size: self.select_button(s, self.size_buttons, 'size', 18)
            )
            self.add_hover_effect(btn, hover_scale=17)
            self.size_buttons.append((btn, size))

        # Toppings
        ttk.Label(
            self.root, text="Select Toppings:",
            foreground="white", background="#1e1e1e"
        ).pack(pady=5)
        self.topping_vars = {}
        toppings_frame = ttk.Frame(self.root)
        toppings_frame.pack()
        for i, topping in enumerate(TOPPINGS):
            var = tk.BooleanVar()
            btn = ttk.Button(toppings_frame, text=topping, style='secondary.TButton')
            btn.grid(row=i//3, column=i%3, padx=5, pady=2)
            btn.bind(
                "<Button-1>",
                lambda e, t=topping: self.toggle_option(t, self.topping_vars, 'toppings', 15)
            )
            self.add_hover_effect(btn, hover_scale=15)
            self.topping_vars[topping] = (var, btn)

        # Sides
        ttk.Label(
            self.root, text="Select Sides:",
            foreground="white", background="#1e1e1e"
        ).pack(pady=5)
        self.side_vars = {}
        self.wings_flavor = tk.StringVar(value="Plain")
        sides_frame = ttk.Frame(self.root)
        sides_frame.pack()
        for i, side in enumerate(SIDES):
            var = tk.BooleanVar()
            btn = ttk.Button(sides_frame, text=side, style='secondary.TButton')
            btn.grid(row=0, column=i*2, padx=5, pady=2)
            btn.bind("<Button-1>", lambda e, s=side: self.toggle_side(s))
            self.add_hover_effect(btn, hover_scale=15)
            self.side_vars[side] = (var, btn)
            if side == "Wings":
                self.wings_flavor_menu = ttk.Combobox(
                    sides_frame,
                    values=WING_FLAVORS,
                    textvariable=self.wings_flavor,
                    state="readonly",
                    width=15
                )
                self.wings_flavor_menu.grid(row=0, column=i*2+1, padx=5)
                self.wings_flavor_menu.grid_remove()

        # Live total
        ttk.Label(
            self.root,
            textvariable=self.total_var,
            font=("Arial", 14),
            foreground="white", background="#1e1e1e"
        ).pack(pady=10)

        ttk.Button(self.root, text="Add Pizza", command=self.add_pizza, style='primary.TButton').pack(pady=5)
        ttk.Button(
            self.root, text="Complete Order",
            command=self.confirm_order, style='danger.TButton'
        ).pack(pady=5)

    def add_hover_effect(self, btn, hover_scale=15):
        def on_enter(e): btn.configure(width=hover_scale)
        def on_leave(e): btn.configure(width=14)
        btn.configure(width=14)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def toggle_option(self, name, storage_dict, field, scale_up=15):
        var, btn = storage_dict[name]
        var.set(not var.get())
        selected = var.get()
        btn.configure(style='primary.TButton' if selected else 'secondary.TButton')
        btn.configure(width=scale_up if selected else 14)
        if selected:
            self.current_order[field].append(name)
        else:
            self.current_order[field].remove(name)
        self.update_total()

    def toggle_side(self, side):
        var, btn = self.side_vars[side]
        var.set(not var.get())
        selected = var.get()
        btn.configure(style='primary.TButton' if selected else 'secondary.TButton')
        btn.configure(width=15 if selected else 14)
        if selected:
            self.current_order['sides'].append(side)
            if side == "Wings": self.wings_flavor_menu.grid()
        else:
            self.current_order['sides'].remove(side)
            if side == "Wings": self.wings_flavor_menu.grid_remove()
        self.update_total()

    def select_button(self, value, button_list, field, scale_up=18):
        self.current_order[field] = value
        for btn, val in button_list:
            is_selected = (val == value)
            btn.configure(style='primary.TButton' if is_selected else 'secondary.TButton')
            btn.configure(width=scale_up if is_selected else 14)
        self.update_total()

    def update_total(self):
        total = 0
        if self.current_order.get('size'):
            total += PRICES[self.current_order['size']]
        for side in self.current_order.get('sides', []):
            total += PRICES[side]
        self.total_var.set(f"Total: ${total}")

    def add_pizza(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Missing Name", "Please enter your name before adding a pizza.")
            return
        self.current_order['name'] = name
        if "Wings" in self.current_order['sides']:
            self.current_order['wings_flavor'] = self.wings_flavor.get()
        self.orders.append(dict(self.current_order))
        # reset for next pizza
        self.current_order = {"name": name, "type": None, "size": None,
                              "toppings": [], "sides": [], "wings_flavor": None}
        self.create_widgets()

    def confirm_order(self):
        if not self.orders:
            messagebox.showerror("No Order", "Add at least one pizza first.")
            return
        self.clear_window()
        summary = ""
        total_price = 0
        for ord in self.orders:
            summary += f"{ord['name']} ordered:\n"
            summary += f"Type: {ord['type']}\n"
            summary += f"Size: {ord['size']} - ${PRICES[ord['size']]}\n"
            total_price += PRICES[ord['size']]
            if ord['toppings']:
                summary += "Toppings: " + ", ".join(ord['toppings']) + "\n"
            for sd in ord['sides']:
                price = PRICES[sd]
                flavor = f" ({ord['wings_flavor']})" if sd == "Wings" else ""
                summary += f"Side: {sd}{flavor} - ${price}\n"
                total_price += price
            summary += "\n"
        summary += f"Total Price: ${total_price}\n"
        ttk.Label(self.root, text=summary, foreground="white", background="#1e1e1e", font=("Arial", 12)).pack(pady=20)
        ttk.Button(self.root, text="Back", command=self.create_widgets, style='success.TButton').pack(pady=5)
        ttk.Button(self.root, text="Place Order", command=self.show_final_message, style='primary.TButton').pack(pady=5)

    def show_final_message(self):
        messagebox.showinfo(
            "Order Placed",
            "Thank you for ordering at Pizza Zamboni, we'll get that started right away!"
        )

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = PizzaZamboniApp(root)
    root.mainloop()
