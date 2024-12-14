from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox, QSpinBox, QGridLayout, QCheckBox, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon
import sys

class PizzaOrderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pizza Zamboni")
        self.setMinimumSize(600, 800)
        self.initUI()

    def initUI(self):
        # Set window icon (favicon)
        self.setWindowIcon(QIcon("PizzaZamboni.png"))

        # Main container widget
        container = QWidget()
        self.setCentralWidget(container)

        # Main layout
        layout = QVBoxLayout()
        container.setLayout(layout)

        # Add image banner
        banner_label = QLabel()
        pixmap = QPixmap("PizzaZamboni.png")  
        pixmap_resized = pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
        banner_label.setPixmap(pixmap_resized)
        banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(banner_label)

        # User name input
        layout.addWidget(QLabel("Enter your name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # Scroll area for pizzas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.pizza_layout = QVBoxLayout()
        scroll_widget.setLayout(self.pizza_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        self.pizza_options = []  # To hold pizza configurations

        self.add_pizza_row()

        # Add pizza button
        self.add_pizza_button = QPushButton("Add Another Pizza")
        self.add_pizza_button.clicked.connect(self.add_pizza_row)
        layout.addWidget(self.add_pizza_button)

        # Submit button
        self.submit_button = QPushButton("Place Order")
        self.submit_button.clicked.connect(self.calculate_cost)
        layout.addWidget(self.submit_button)

        # Apply dark theme
        self.apply_dark_theme()

    def add_pizza_row(self):
        pizza_widget = QWidget()
        pizza_layout = QGridLayout()
        pizza_widget.setLayout(pizza_layout)
        
        row = len(self.pizza_options)

        # Size selection (buttons as rectangles)
        size_label = QLabel(f"Pizza {row + 1} Size:")
        pizza_layout.addWidget(size_label, 0, 0)

        size_buttons = []
        for i, size in enumerate(["Small", "Medium", "Large"]):
            button = QPushButton(size)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, b=button, others=size_buttons: self.handle_exclusive_buttons(b, others))
            pizza_layout.addWidget(button, 0, i + 1)
            size_buttons.append(button)

        # Toppings selection
        toppings_label = QLabel("Toppings:")
        pizza_layout.addWidget(toppings_label, 1, 0)

        toppings_checkboxes = []
        toppings = ["Mushroom", "Broccoli", "Tomato", "Black Olives", "Pineapple", "Bacon", "Cheesey Goodness", "Sausage", "Hot Dog"]
        for i, topping in enumerate(toppings):
            checkbox = QCheckBox(topping)
            toppings_checkboxes.append(checkbox)
            pizza_layout.addWidget(checkbox, 1 + (i // 3), (i % 3) + 1)

        # Quantity selection
        quantity_label = QLabel("Quantity:")
        pizza_layout.addWidget(quantity_label, len(toppings) // 3 + 2, 0)

        quantity_spinbox = QSpinBox()
        quantity_spinbox.setRange(1, 10)
        pizza_layout.addWidget(quantity_spinbox, len(toppings) // 3 + 2, 1)

        self.pizza_layout.addWidget(pizza_widget)

        self.pizza_options.append({
            "size_buttons": size_buttons,
            "toppings_checkboxes": toppings_checkboxes,
            "quantity_spinbox": quantity_spinbox
        })

    def handle_exclusive_buttons(self, button, others):
        if button.isChecked():
            for other in others:
                if other != button:
                    other.setChecked(False)

    def calculate_cost(self):
        user_name = self.name_input.text().strip()
        if not user_name:
            QMessageBox.critical(self, "Error", "Please enter your name.")
            return

        total_cost = 0
        order_summary = []

        for i, pizza in enumerate(self.pizza_options):
            size = next((b.text() for b in pizza["size_buttons"] if b.isChecked()), None)
            if not size:
                QMessageBox.critical(self, "Error", f"Please select a size for Pizza {i + 1}.")
                return

            selected_toppings = [c.text() for c in pizza["toppings_checkboxes"] if c.isChecked()]
            toppings_message = ", ".join(selected_toppings) if selected_toppings else "no toppings"

            quantity = pizza["quantity_spinbox"].value()

            cost = {"Small": 3, "Medium": 4, "Large": 5}[size] * quantity
            total_cost += cost

            order_summary.append(f"Pizza {i + 1}: {quantity} x {size} pizza(s) with {toppings_message} - ${cost}")

        QMessageBox.information(
            self,
            "Order Summary",
            f"Thank you, {user_name}!\n\n" + "\n".join(order_summary) + f"\n\nTotal Cost: ${total_cost}"
        )

    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(66, 66, 66))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        QApplication.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PizzaOrderApp()
    window.show()
    sys.exit(app.exec())
