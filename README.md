# 🏪 Shop Management System (Python + Tkinter + MySQL)

A desktop-based application for **shopkeepers** to manage products, sales, and revenue easily.  
Built with **Python (Tkinter)** for GUI and **MySQL** for database storage.

---

## 🌟 Features

✅ **Product Management**
- Add, update, delete, and view products.  
- Tracks product categories, prices, and quantities.  

✅ **Sales Management**
- Record sales with product quantity and total amount.  
- Auto-updates stock after each sale.  

✅ **Dashboard Overview**
- Displays **total revenue**, **total products**, and **low-stock alerts**.  
- Clean modern GUI with frames, colors, and icons.  

✅ **Reports**
- View daily sales summary and totals.  

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| Language | Python 3 |
| GUI Library | Tkinter |
| Database | MySQL |
| Image Library | Pillow (PIL) |
| Connector | mysql-connector-python |

---

## 🧱 Database Design

### **Products Table**
| Field | Type | Description |
|--------|------|-------------|
| product_id | INT (PK) | Unique Product ID |
| name | VARCHAR | Product Name |
| category | VARCHAR | Product Category |
| price | DECIMAL | Product Price |
| quantity | INT | Available Stock |

### **Sales Table**
| Field | Type | Description |
|--------|------|-------------|
| sale_id | INT (PK) | Unique Sale ID |
| product_id | INT (FK) | Linked Product |
| quantity | INT | Quantity Sold |
| total | DECIMAL | Total Amount |
| date | DATETIME | Date of Sale |

---

## 🗂️ Folder Structure

