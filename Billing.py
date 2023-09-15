import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import random
from datetime import datetime
import re  # Import the regular expressions module

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Management App")
        
        self.products = {
            "Product A": 10,
            "Product B": 15,
            "Product C": 20,
        }
        
        self.cart = {}
        self.discount = 0
        self.user_name = ""
        self.phone_number = ""
        
        self.create_widgets()
        
    def create_widgets(self):
        # User information frame
        user_info_frame = tk.Frame(self.root)
        user_info_frame.pack(side=tk.TOP, padx=10, pady=10)
        
        tk.Label(user_info_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(user_info_frame)
        self.name_entry.grid(row=0, column=1)
        
        tk.Label(user_info_frame, text="Phone Number:").grid(row=1, column=0)
        self.phone_entry = tk.Entry(user_info_frame)
        self.phone_entry.grid(row=1, column=1)
        
        # Product selection frame
        product_frame = tk.Frame(self.root)
        product_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(product_frame, text="Products").pack()
        self.product_listbox = tk.Listbox(product_frame, selectmode=tk.MULTIPLE)
        for product in self.products.keys():
            self.product_listbox.insert(tk.END, product)
        self.product_listbox.pack()
        
        tk.Button(product_frame, text="Add to Cart", command=self.prompt_quantity).pack()
        
        # Discount and Cart frame
        discount_and_cart_frame = tk.Frame(self.root)
        discount_and_cart_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Discount frame
        discount_frame = tk.Frame(discount_and_cart_frame)
        discount_frame.pack()
        
        tk.Label(discount_frame, text="Discount (%)").pack()
        self.discount_entry = tk.Entry(discount_frame)
        self.discount_entry.pack()
        
        # Cart frame
        cart_frame = tk.Frame(discount_and_cart_frame)
        cart_frame.pack()
        
        tk.Label(cart_frame, text="Cart").pack()
        self.cart_listbox = tk.Listbox(cart_frame)
        self.cart_listbox.pack()
        
        tk.Button(cart_frame, text="Checkout", command=self.checkout).pack()
    
    def prompt_quantity(self):
        selected_products = self.product_listbox.curselection()
        for index in selected_products:
            product = self.product_listbox.get(index)
            quantity = self.get_product_quantity(product)
            if quantity > 0:
                if product in self.cart:
                    self.cart[product] += quantity
                else:
                    self.cart[product] = quantity
        
        self.update_cart_listbox()
    
    def get_product_quantity(self, product):
        quantity = 0
        try:
            quantity = int(simpledialog.askstring("Quantity", f"Enter quantity for {product}:"))
            if quantity < 0:
                messagebox.showerror("Invalid Input", "Quantity cannot be negative.")
                return 0
        except ValueError:
            pass  # Quantity not provided or invalid
        
        return max(quantity, 0)
        
    def update_cart_listbox(self):
        self.cart_listbox.delete(0, tk.END)
        for product, quantity in self.cart.items():
            self.cart_listbox.insert(tk.END, f"{product} - {quantity} x ${self.products[product]}")
        
    def checkout(self):
        total_cost = sum(self.products[product] * quantity for product, quantity in self.cart.items())
        discount_percentage = self.get_discount_percentage()
        if discount_percentage < 0:
            messagebox.showerror("Invalid Input", "Discount cannot be negative.")
            return
        total_cost_before = total_cost
        total_cost -= (total_cost * (discount_percentage / 100))
        
        # Calculate GST (18%)
        gst = 0.18 * total_cost_before
        
        #Grand Total
        bill_amount = total_cost + gst
        
        # Generate a random order number
        order_number = random.randint(30, 250)
        
        # Get current date and time
        order_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get user name and phone number
        self.user_name = self.name_entry.get()
        self.phone_number = self.phone_entry.get()
        
        # Validate phone number using regular expressions
        phone_pattern = r"^\d{10}$"  # Assumes a 10-digit phone number
        if not re.match(phone_pattern, self.phone_number):
            messagebox.showerror("Invalid Input", "Invalid phone number format. Please enter a 10-digit number.")
            return
        
        order_summary = f"Order Summary: \n\n"
        order_summary += f"Order Number: {order_number}\n"
        order_summary += f"Order Date & Time: {order_date_time}\n\n"
        order_summary += f"Customer Details:\nCustomer Name: {self.user_name} \nPhone: {self.phone_number}\n\n"
        for product, quantity in self.cart.items():
            product_total = self.products[product] * quantity
            order_summary += f"{product} - {quantity} x ${self.products[product]} = ${product_total:.2f}\n"
        order_summary += f"\n\nItem total : ${total_cost_before:.2f}\n\n"
        order_summary += f"Discount: {discount_percentage}%\n\n"
        order_summary += f"Total Cost : ${total_cost:.2f}\n"
        order_summary += f"(after discount)\n\n"
        order_summary += f"GST (18%): ${gst:.2f}\n\n"
        order_summary += f"Grand Total: ${bill_amount:.2f}"
        
        messagebox.showinfo("Order Summary", order_summary)
        self.cart = {}
        self.update_cart_listbox()
    
    def get_discount_percentage(self):
        try:
            return float(self.discount_entry.get())
        except ValueError:
            return 0  # Default to no discount if the input is not a valid float

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
