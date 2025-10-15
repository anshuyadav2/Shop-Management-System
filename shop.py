import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

# -------------------- DATABASE CONNECTION -------------------- #
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="python"
)
cursor = db.cursor()

# -------------------- CREATE TABLES IF NOT EXISTS -------------------- #
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    quantity INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT,
    total DECIMAL(10,2),
    date DATETIME,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
)
""")
db.commit()

# -------------------- MAIN APPLICATION -------------------- #
class ShopManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shop Management System")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f2f5")

        # -------------------- DASHBOARD -------------------- #
        self.dashboard_frame = tk.Frame(self.root, bg="#1f2e3d", height=150)
        self.dashboard_frame.pack(fill=tk.X)

        self.label_total_revenue = tk.Label(self.dashboard_frame, text="Total Revenue: ₹0", fg="white", bg="#1f2e3d", font=("Arial", 16, "bold"))
        self.label_total_revenue.pack(side=tk.LEFT, padx=20, pady=20)

        self.label_total_products = tk.Label(self.dashboard_frame, text="Total Products: 0", fg="white", bg="#1f2e3d", font=("Arial", 16, "bold"))
        self.label_total_products.pack(side=tk.LEFT, padx=20, pady=20)

        self.label_low_stock = tk.Label(self.dashboard_frame, text="Low Stock: 0", fg="white", bg="#1f2e3d", font=("Arial", 16, "bold"))
        self.label_low_stock.pack(side=tk.LEFT, padx=20, pady=20)

        # -------------------- TAB CONTROL -------------------- #
        self.tab_control = ttk.Notebook(self.root)
        self.tab_products = tk.Frame(self.tab_control, bg="#f0f2f5")
        self.tab_sales = tk.Frame(self.tab_control, bg="#f0f2f5")
        self.tab_reports = tk.Frame(self.tab_control, bg="#f0f2f5")

        self.tab_control.add(self.tab_products, text="Products")
        self.tab_control.add(self.tab_sales, text="Sales")
        self.tab_control.add(self.tab_reports, text="Reports")
        self.tab_control.pack(expand=1, fill="both")

        # Initialize tabs
        self.products_tab()
        self.sales_tab()
        self.reports_tab()
        self.update_dashboard()

    # -------------------- PRODUCTS TAB -------------------- #
    def products_tab(self):
        frame = self.tab_products

        # Left Frame - Form
        form_frame = tk.LabelFrame(frame, text="Product Details", bg="#f0f2f5", padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(form_frame, text="Name:", bg="#f0f2f5").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_name = tk.Entry(form_frame, width=25)
        self.entry_name.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Category:", bg="#f0f2f5").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_category = tk.Entry(form_frame, width=25)
        self.entry_category.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Price:", bg="#f0f2f5").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_price = tk.Entry(form_frame, width=25)
        self.entry_price.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Quantity:", bg="#f0f2f5").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_quantity = tk.Entry(form_frame, width=25)
        self.entry_quantity.grid(row=3, column=1, pady=5)

        tk.Button(form_frame, text="Add Product", command=self.add_product, bg="#4CAF50", fg="white", width=20).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(form_frame, text="Update Product", command=self.update_product, bg="#2196F3", fg="white", width=20).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(form_frame, text="Delete Product", command=self.delete_product, bg="#f44336", fg="white", width=20).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(form_frame, text="Clear Fields", command=self.clear_product_fields, width=20).grid(row=7, column=0, columnspan=2, pady=5)

        # Right Frame - Treeview
        tree_frame = tk.Frame(frame, bg="#f0f2f5")
        tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        self.product_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Category", "Price", "Quantity"), show="headings", height=18)
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Name", text="Name")
        self.product_tree.heading("Category", text="Category")
        self.product_tree.heading("Price", text="Price")
        self.product_tree.heading("Quantity", text="Quantity")
        self.product_tree.column("ID", width=50)
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        self.product_tree.bind("<ButtonRelease-1>", self.select_product)

        self.load_products()

    # -------------------- SALES TAB -------------------- #
    def sales_tab(self):
        frame = self.tab_sales

        form_frame = tk.LabelFrame(frame, text="Sell Product", padx=10, pady=10, bg="#f0f2f5")
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(form_frame, text="Product:", bg="#f0f2f5").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.combo_products = ttk.Combobox(form_frame, width=22)
        self.combo_products.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Quantity:", bg="#f0f2f5").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_sale_qty = tk.Entry(form_frame, width=25)
        self.entry_sale_qty.grid(row=1, column=1, pady=5)

        tk.Button(form_frame, text="Sell Product", command=self.sell_product, bg="#4CAF50", fg="white", width=20).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(form_frame, text="Clear Fields", command=self.clear_sale_fields, width=20).grid(row=3, column=0, columnspan=2, pady=5)

        # Right Frame - Sales Treeview
        tree_frame = tk.Frame(frame, bg="#f0f2f5")
        tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.sales_tree = ttk.Treeview(tree_frame, columns=("Sale ID", "Product", "Quantity", "Total", "Date"), show="headings", height=18)
        self.sales_tree.heading("Sale ID", text="ID")
        self.sales_tree.heading("Product", text="Product")
        self.sales_tree.heading("Quantity", text="Quantity")
        self.sales_tree.heading("Total", text="Total")
        self.sales_tree.heading("Date", text="Date")
        self.sales_tree.column("Sale ID", width=50)
        self.sales_tree.pack(fill=tk.BOTH, expand=True)

        self.load_products_combobox()
        self.load_sales()

    # -------------------- REPORTS TAB -------------------- #
    def reports_tab(self):
        frame = self.tab_reports
        tk.Label(frame, text="Daily Sales Report", font=("Arial", 14, "bold"), bg="#f0f2f5").pack(pady=10)
        self.report_tree = ttk.Treeview(frame, columns=("Product", "Quantity", "Total"), show="headings", height=20)
        self.report_tree.heading("Product", text="Product")
        self.report_tree.heading("Quantity", text="Quantity Sold")
        self.report_tree.heading("Total", text="Total Amount")
        self.report_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Button(frame, text="Load Today's Report", command=self.load_report, bg="#2196F3", fg="white", width=20).pack(pady=5)

    # -------------------- PRODUCT FUNCTIONS -------------------- #
    def add_product(self):
        name = self.entry_name.get()
        category = self.entry_category.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()
        if name == "" or price == "" or quantity == "":
            messagebox.showerror("Error", "Please fill all required fields!")
            return
        cursor.execute("INSERT INTO Products (name, category, price, quantity) VALUES (%s, %s, %s, %s)",
                       (name, category, float(price), int(quantity)))
        db.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        self.load_products()
        self.load_products_combobox()
        self.clear_product_fields()
        self.update_dashboard()

    def update_product(self):
        selected = self.product_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a product to update")
            return
        data = self.product_tree.item(selected)
        product_id = data["values"][0]
        name = self.entry_name.get()
        category = self.entry_category.get()
        price = self.entry_price.get()
        quantity = self.entry_quantity.get()
        cursor.execute("UPDATE Products SET name=%s, category=%s, price=%s, quantity=%s WHERE product_id=%s",
                       (name, category, float(price), int(quantity), product_id))
        db.commit()
        messagebox.showinfo("Success", "Product updated successfully!")
        self.load_products()
        self.load_products_combobox()
        self.clear_product_fields()
        self.update_dashboard()

    # -------------------- SAFE DELETE PRODUCT -------------------- #
    def delete_product(self):
        selected = self.product_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select a product to delete")
            return

        data = self.product_tree.item(selected)
        product_id = data["values"][0]

        # Check if any sales exist for this product
        cursor.execute("SELECT COUNT(*) FROM Sales WHERE product_id=%s", (product_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            messagebox.showerror("Error", "Cannot delete this product because sales exist!")
            return

        # Safe to delete
        cursor.execute("DELETE FROM Products WHERE product_id=%s", (product_id,))
        db.commit()
        messagebox.showinfo("Success", "Product deleted successfully!")
        self.load_products()
        self.load_products_combobox()
        self.clear_product_fields()
        self.update_dashboard()

    def load_products(self):
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)
        cursor.execute("SELECT * FROM Products")
        for product in cursor.fetchall():
            self.product_tree.insert("", tk.END, values=product)
        self.update_dashboard()

    def select_product(self, event):
        selected = self.product_tree.focus()
        if selected:
            data = self.product_tree.item(selected)["values"]
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, data[1])
            self.entry_category.delete(0, tk.END)
            self.entry_category.insert(0, data[2])
            self.entry_price.delete(0, tk.END)
            self.entry_price.insert(0, data[3])
            self.entry_quantity.delete(0, tk.END)
            self.entry_quantity.insert(0, data[4])

    def clear_product_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

    # -------------------- SALES FUNCTIONS -------------------- #
    def load_products_combobox(self):
        cursor.execute("SELECT name FROM Products")
        products = [p[0] for p in cursor.fetchall()]
        self.combo_products["values"] = products

    def sell_product(self):
        product_name = self.combo_products.get()
        qty = self.entry_sale_qty.get()
        if product_name == "" or qty == "":
            messagebox.showerror("Error", "Please select product and enter quantity")
            return
        cursor.execute("SELECT product_id, price, quantity FROM Products WHERE name=%s", (product_name,))
        product = cursor.fetchone()
        if not product:
            messagebox.showerror("Error", "Product not found!")
            return
        product_id, price, stock_qty = product
        qty = int(qty)
        if qty > stock_qty:
            messagebox.showerror("Error", "Not enough stock!")
            return
        total = price * qty
        cursor.execute("INSERT INTO Sales (product_id, quantity, total, date) VALUES (%s, %s, %s, %s)",
                       (product_id, qty, total, datetime.now()))
        cursor.execute("UPDATE Products SET quantity=%s WHERE product_id=%s", (stock_qty - qty, product_id))
        db.commit()
        messagebox.showinfo("Success", f"Sold {qty} x {product_name} = ₹{total}")
        self.load_products()
        self.load_products_combobox()
        self.load_sales()
        self.clear_sale_fields()
        self.update_dashboard()

    def load_sales(self):
        for row in self.sales_tree.get_children():
            self.sales_tree.delete(row)
        cursor.execute("""
            SELECT s.sale_id, p.name, s.quantity, s.total, s.date 
            FROM Sales s JOIN Products p ON s.product_id = p.product_id
        """)
        for sale in cursor.fetchall():
            self.sales_tree.insert("", tk.END, values=sale)

    def clear_sale_fields(self):
        self.combo_products.set("")
        self.entry_sale_qty.delete(0, tk.END)

    # -------------------- REPORTS FUNCTIONS -------------------- #
    def load_report(self):
        for row in self.report_tree.get_children():
            self.report_tree.delete(row)
        today = datetime.now().date()
        cursor.execute("""
            SELECT p.name, SUM(s.quantity), SUM(s.total) 
            FROM Sales s JOIN Products p ON s.product_id = p.product_id
            WHERE DATE(s.date) = %s
            GROUP BY s.product_id
        """, (today,))
        for row in cursor.fetchall():
            self.report_tree.insert("", tk.END, values=row)

    # -------------------- DASHBOARD UPDATE -------------------- #
    def update_dashboard(self):
        cursor.execute("SELECT SUM(total) FROM Sales")
        total_revenue = cursor.fetchone()[0] or 0
        self.label_total_revenue.config(text=f"Total Revenue: ₹{total_revenue}")

        cursor.execute("SELECT COUNT(*) FROM Products")
        total_products = cursor.fetchone()[0]
        self.label_total_products.config(text=f"Total Products: {total_products}")

        cursor.execute("SELECT COUNT(*) FROM Products WHERE quantity < 5")
        low_stock = cursor.fetchone()[0]
        self.label_low_stock.config(text=f"Low Stock: {low_stock}")

# -------------------- RUN APPLICATION -------------------- #
root = tk.Tk()
app = ShopManagementApp(root)
root.mainloop()
