import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

def fetch_data(query):
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

def populate_treeview(tree, data, columns):
    tree.delete(*tree.get_children())
    for row in data:
        tree.insert("", "end", values=row)

def get_stock_quantity(product_id):
    cursor = db.cursor()
    cursor.execute("SELECT SUM(Quantity) FROM Restock WHERE Product_ID = %s", (product_id,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result[0] is not None else 0

def on_customer_select(event):
    selected_item = tree_customer.selection()
    if selected_item:
        values = tree_customer.item(selected_item[0], 'values')
        entry_name.delete(0, tk.END)
        entry_name.insert(0, values[1])
        entry_age.delete(0, tk.END)
        entry_age.insert(0, values[2])
        entry_phone.delete(0, tk.END)
        entry_phone.insert(0, values[3])
        button_update_customer.grid(row=3, column=1, pady=10)
        button_delete_customer.grid(row=3, column=2, pady=10)

def on_employee_select(event):
    selected_item = tree_employee.selection()
    if selected_item:
        values = tree_employee.item(selected_item[0], 'values')
        entry_employee_name.delete(0, tk.END)
        entry_employee_name.insert(0, values[1])
        button_update_employee.grid(row=1, column=1, pady=10)
        button_delete_employee.grid(row=1, column=2, pady=10)

def on_order_select(event):
    selected_item = tree_order.selection()
    if selected_item:
        values = tree_order.item(selected_item[0], 'values')
        entry_customer_id.delete(0, tk.END)
        entry_customer_id.insert(0, values[1])
        entry_order_date.delete(0, tk.END)
        entry_order_date.insert(0, values[2])
        entry_purchaser_amount.delete(0, tk.END)
        entry_purchaser_amount.insert(0, values[3])
        button_update_order.grid(row=3, column=1, pady=10)
        button_delete_order.grid(row=3, column=2, pady=10)

def on_order_line_select(event):
    selected_item = tree_order_line.selection()
    if selected_item:
        values = tree_order_line.item(selected_item[0], 'values')
        entry_order_id.delete(0, tk.END)
        entry_order_id.insert(0, values[0])
        entry_product_id.delete(0, tk.END)
        entry_product_id.insert(0, values[1])
        entry_quantity.delete(0, tk.END)
        entry_quantity.insert(0, values[2])
        button_update_order_line.grid(row=3, column=1, pady=10)
        button_delete_order_line.grid(row=3, column=2, pady=10)

def on_restock_select(event):
    selected_item = tree_restock.selection()
    if selected_item:
        values = tree_restock.item(selected_item[0], 'values')
        entry_restock_product_id.delete(0, tk.END)
        entry_restock_product_id.insert(0, values[0])
        entry_restock_date.delete(0, tk.END)
        entry_restock_date.insert(0, values[1])
        entry_stock_date.delete(0, tk.END)
        entry_stock_date.insert(0, values[2])
        entry_restock_quantity.delete(0, tk.END)
        entry_restock_quantity.insert(0, values[3])
        button_update_restock.grid(row=4, column=1, pady=10)
        button_delete_restock.grid(row=4, column=2, pady=10)

def on_product_select(event):
    selected_item = tree_product.selection()
    if selected_item:
        values = tree_product.item(selected_item[0], 'values')
        entry_product_name.delete(0, tk.END)
        entry_product_name.insert(0, values[1])
        entry_product_price.delete(0, tk.END)
        entry_product_price.insert(0, values[2])
        button_update_product.grid(row=2, column=1, pady=10)
        button_delete_product.grid(row=2, column=2, pady=10)

def insert_customer():
    name = entry_name.get()
    age = entry_age.get()
    phone = entry_phone.get()
    
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Customer (Customer_Name, Age, Phone) VALUES (%s, %s, %s)", (name, age, phone))
        db.commit()
        messagebox.showinfo("Success", "Customer added successfully")
        populate_treeview(tree_customer, fetch_data("SELECT * FROM Customer"), ["Customer_ID", "Customer_Name", "Age", "Phone"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def update_customer():
    selected_item = tree_customer.selection()[0]
    values = tree_customer.item(selected_item, 'values')
    customer_id = values[0]
    name = entry_name.get()
    age = entry_age.get()
    phone = entry_phone.get()

    try:
        cursor = db.cursor()
        cursor.execute("UPDATE Customer SET Customer_Name=%s, Age=%s, Phone=%s WHERE Customer_ID=%s", (name, age, phone, customer_id))
        db.commit()
        messagebox.showinfo("Success", "Customer updated successfully")
        populate_treeview(tree_customer, fetch_data("SELECT * FROM Customer"), ["Customer_ID", "Customer_Name", "Age", "Phone"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def delete_customer():
    selected_item = tree_customer.selection()[0]
    values = tree_customer.item(selected_item, 'values')
    customer_id = values[0]

    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Customer WHERE Customer_ID=%s", (customer_id,))
        db.commit()
        messagebox.showinfo("Success", "Customer deleted successfully")
        populate_treeview(tree_customer, fetch_data("SELECT * FROM Customer"), ["Customer_ID", "Customer_Name", "Age", "Phone"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def insert_employee():
    name = entry_employee_name.get()
    
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Employee (Employee_Name) VALUES (%s)", (name,))
        db.commit()
        messagebox.showinfo("Success", "Employee added successfully")
        populate_treeview(tree_employee, fetch_data("SELECT * FROM Employee"), ["Employee_ID", "Employee_Name"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def update_employee():
    selected_item = tree_employee.selection()[0]
    values = tree_employee.item(selected_item, 'values')
    employee_id = values[0]
    name = entry_employee_name.get()

    try:
        cursor = db.cursor()
        cursor.execute("UPDATE Employee SET Employee_Name=%s WHERE Employee_ID=%s", (name, employee_id))
        db.commit()
        messagebox.showinfo("Success", "Employee updated successfully")
        populate_treeview(tree_employee, fetch_data("SELECT * FROM Employee"), ["Employee_ID", "Employee_Name"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def delete_employee():
    selected_item = tree_employee.selection()[0]
    values = tree_employee.item(selected_item, 'values')
    employee_id = values[0]

    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Employee WHERE Employee_ID=%s", (employee_id,))
        db.commit()
        messagebox.showinfo("Success", "Employee deleted successfully")
        populate_treeview(tree_employee, fetch_data("SELECT * FROM Employee"), ["Employee_ID", "Employee_Name"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def insert_order():
    customer_id = entry_customer_id.get()
    date = entry_order_date.get()
    purchaser_amount = entry_purchaser_amount.get()
    
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO `Order` (Customer_ID, Date, Purchaser_amount) VALUES (%s, %s, %s)", (customer_id, date, purchaser_amount))
        db.commit()
        messagebox.showinfo("Success", "Order added successfully")
        populate_treeview(tree_order, fetch_data("SELECT * FROM `Order`"), ["Order_ID", "Customer_ID", "Date", "Purchaser_amount"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def update_order():
    selected_item = tree_order.selection()[0]
    values = tree_order.item(selected_item, 'values')
    order_id = values[0]
    customer_id = entry_customer_id.get()
    date = entry_order_date.get()
    purchaser_amount = entry_purchaser_amount.get()

    try:
        cursor = db.cursor()
        cursor.execute("UPDATE `Order` SET Customer_ID=%s, Date=%s, Purchaser_amount=%s WHERE Order_ID=%s", (customer_id, date, purchaser_amount, order_id))
        db.commit()
        messagebox.showinfo("Success", "Order updated successfully")
        populate_treeview(tree_order, fetch_data("SELECT * FROM `Order`"), ["Order_ID", "Customer_ID", "Date", "Purchaser_amount"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def delete_order():
    selected_item = tree_order.selection()[0]
    values = tree_order.item(selected_item, 'values')
    order_id = values[0]

    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM `Order` WHERE Order_ID=%s", (order_id,))
        db.commit()
        messagebox.showinfo("Success", "Order deleted successfully")
        populate_treeview(tree_order, fetch_data("SELECT * FROM `Order`"), ["Order_ID", "Customer_ID", "Date", "Purchaser_amount"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def insert_order_line():
    order_id = entry_order_id.get()
    product_id = entry_product_id.get()
    quantity = int(entry_quantity.get())
    stock_quantity = get_stock_quantity(product_id)
    
    if quantity > stock_quantity:
        messagebox.showerror("Error", "Order quantity exceeds stock quantity")
        return
    
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Order_Line (Order_ID, Product_ID, Quantity) VALUES (%s, %s, %s)", (order_id, product_id, quantity))
        db.commit()
        messagebox.showinfo("Success", "Order Line added successfully")
        populate_treeview(tree_order_line, fetch_data("SELECT * FROM Order_Line"), ["Order_ID", "Product_ID", "Quantity"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def update_order_line():
    selected_item = tree_order_line.selection()[0]
    values = tree_order_line.item(selected_item, 'values')
    order_id = values[0]
    product_id = values[1]
    quantity = int(entry_quantity.get())
    stock_quantity = get_stock_quantity(product_id)

    if quantity > stock_quantity:
        messagebox.showerror("Error", "Order quantity exceeds stock quantity")
        return

    try:
        cursor = db.cursor()
        cursor.execute("UPDATE Order_Line SET Quantity=%s WHERE Order_ID=%s AND Product_ID=%s", (quantity, order_id, product_id))
        db.commit()
        messagebox.showinfo("Success", "Order Line updated successfully")
        populate_treeview(tree_order_line, fetch_data("SELECT * FROM Order_Line"), ["Order_ID", "Product_ID", "Quantity"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def delete_order_line():
    selected_item = tree_order_line.selection()[0]
    values = tree_order_line.item(selected_item, 'values')
    order_id = values[0]
    product_id = values[1]

    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Order_Line WHERE Order_ID=%s AND Product_ID=%s", (order_id, product_id))
        db.commit()
        messagebox.showinfo("Success", "Order Line deleted successfully")
        populate_treeview(tree_order_line, fetch_data("SELECT * FROM Order_Line"), ["Order_ID", "Product_ID", "Quantity"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def insert_restock():
    product_id = entry_restock_product_id.get()
    restock_date = entry_restock_date.get()
    stock_date = entry_stock_date.get()
    quantity = entry_restock_quantity.get()
    
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Restock (Product_ID, Restock_Date, Stock_Date, Quantity) VALUES (%s, %s, %s, %s)", (product_id, restock_date, stock_date, quantity))
        db.commit()
        messagebox.showinfo("Success", "Restock added successfully")
        populate_treeview(tree_restock, fetch_data("SELECT * FROM Restock"), ["Product_ID", "Restock_Date", "Stock_Date", "Quantity"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def update_restock():
    selected_item = tree_restock.selection()[0]
    values = tree_restock.item(selected_item, 'values')
    product_id = values[0]
    restock_date = entry_restock_date.get()
    stock_date = entry_stock_date.get()
    quantity = entry_restock_quantity.get()

    try:
        cursor = db.cursor()
        cursor.execute("UPDATE Restock SET Restock_Date=%s, Stock_Date=%s, Quantity=%s WHERE Product_ID=%s", (restock_date, stock_date, quantity, product_id))
        db.commit()
        messagebox.showinfo("Success", "Restock updated successfully")
        populate_treeview(tree_restock, fetch_data("SELECT * FROM Restock"), ["Product_ID", "Restock_Date", "Stock_Date", "Quantity"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def delete_restock():
    selected_item = tree_restock.selection()[0]
    values = tree_restock.item(selected_item, 'values')
    product_id = values[0]
    restock_date = values[1]

    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Restock WHERE Product_ID=%s AND Restock_Date=%s", (product_id, restock_date))
        db.commit()
        messagebox.showinfo("Success", "Restock deleted successfully")
        populate_treeview(tree_restock, fetch_data("SELECT * FROM Restock"), ["Product_ID", "Restock_Date", "Stock_Date", "Quantity"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def insert_product():
    product_name = entry_product_name.get()
    price = entry_product_price.get()
    
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO Product (Product_Name, Price) VALUES (%s, %s)", (product_name, price))
        db.commit()
        messagebox.showinfo("Success", "Product added successfully")
        populate_treeview(tree_product, fetch_data("SELECT * FROM Product"), ["Product_ID", "Product_Name", "Price"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def update_product():
    selected_item = tree_product.selection()[0]
    values = tree_product.item(selected_item, 'values')
    product_id = values[0]
    product_name = entry_product_name.get()
    price = entry_product_price.get()

    try:
        cursor = db.cursor()
        cursor.execute("UPDATE Product SET Product_Name=%s, Price=%s WHERE Product_ID=%s", (product_name, price, product_id))
        db.commit()
        messagebox.showinfo("Success", "Product updated successfully")
        populate_treeview(tree_product, fetch_data("SELECT * FROM Product"), ["Product_ID", "Product_Name", "Price"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

def delete_product():
    selected_item = tree_product.selection()[0]
    values = tree_product.item(selected_item, 'values')
    product_id = values[0]

    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Product WHERE Product_ID=%s", (product_id,))
        db.commit()
        messagebox.showinfo("Success", "Product deleted successfully")
        populate_treeview(tree_product, fetch_data("SELECT * FROM Product"), ["Product_ID", "Product_Name", "Price"])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()

# เชื่อมต่อฐานข้อมูล
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stock"
)

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("Stock Management System")

# สร้าง Notebook สำหรับแท็บ
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both')

# แท็บสำหรับเพิ่มข้อมูลลูกค้า
tab_customer = ttk.Frame(notebook)
notebook.add(tab_customer, text='Customer')

label_name = tk.Label(tab_customer, text="Customer Name:")
label_name.grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(tab_customer)
entry_name.grid(row=0, column=1, padx=5, pady=5)

label_age = tk.Label(tab_customer, text="Age:")
label_age.grid(row=1, column=0, padx=5, pady=5)
entry_age = tk.Entry(tab_customer)
entry_age.grid(row=1, column=1, padx=5, pady=5)

label_phone = tk.Label(tab_customer, text="Phone:")
label_phone.grid(row=2, column=0, padx=5, pady=5)
entry_phone = tk.Entry(tab_customer)
entry_phone.grid(row=2, column=1, padx=5, pady=5)

button_add_customer = tk.Button(tab_customer, text="Add Customer", command=insert_customer)
button_add_customer.grid(row=3, column=0, pady=10)

button_update_customer = tk.Button(tab_customer, text="Update Customer", command=update_customer)
button_delete_customer = tk.Button(tab_customer, text="Delete Customer", command=delete_customer)

# Treeview สำหรับแสดงข้อมูลลูกค้า
tree_customer = ttk.Treeview(tab_customer, columns=("Customer_ID", "Customer_Name", "Age", "Phone"), show='headings')
tree_customer.heading("Customer_ID", text="Customer ID")
tree_customer.heading("Customer_Name", text="Customer Name")
tree_customer.heading("Age", text="Age")
tree_customer.heading("Phone", text="Phone")
tree_customer.grid(row=4, columnspan=3, pady=10, padx=5, sticky="nsew")
tree_customer.bind("<<TreeviewSelect>>", on_customer_select)

# เติมข้อมูลลงใน treeview
populate_treeview(tree_customer, fetch_data("SELECT * FROM Customer"), ["Customer_ID", "Customer_Name", "Age", "Phone"])

# แท็บสำหรับเพิ่มข้อมูลพนักงาน
tab_employee = ttk.Frame(notebook)
notebook.add(tab_employee, text='Employee')

label_employee_name = tk.Label(tab_employee, text="Employee Name:")
label_employee_name.grid(row=0, column=0, padx=5, pady=5)
entry_employee_name = tk.Entry(tab_employee)
entry_employee_name.grid(row=0, column=1, padx=5, pady=5)

button_add_employee = tk.Button(tab_employee, text="Add Employee", command=insert_employee)
button_add_employee.grid(row=1, column=0, pady=10)

button_update_employee = tk.Button(tab_employee, text="Update Employee", command=update_employee)
button_delete_employee = tk.Button(tab_employee, text="Delete Employee", command=delete_employee)

# Treeview สำหรับแสดงข้อมูลพนักงาน
tree_employee = ttk.Treeview(tab_employee, columns=("Employee_ID", "Employee_Name"), show='headings')
tree_employee.heading("Employee_ID", text="Employee ID")
tree_employee.heading("Employee_Name", text="Employee Name")
tree_employee.grid(row=2, columnspan=3, pady=10, padx=5, sticky="nsew")
tree_employee.bind("<<TreeviewSelect>>", on_employee_select)

# เติมข้อมูลลงใน treeview
populate_treeview(tree_employee, fetch_data("SELECT * FROM Employee"), ["Employee_ID", "Employee_Name"])

# แท็บสำหรับเพิ่มคำสั่งซื้อ
tab_order = ttk.Frame(notebook)
notebook.add(tab_order, text='Order')

label_customer_id = tk.Label(tab_order, text="Customer ID:")
label_customer_id.grid(row=0, column=0, padx=5, pady=5)
entry_customer_id = tk.Entry(tab_order)
entry_customer_id.grid(row=0, column=1, padx=5, pady=5)

label_order_date = tk.Label(tab_order, text="Order Date (YYYY-MM-DD):")
label_order_date.grid(row=1, column=0, padx=5, pady=5)
entry_order_date = tk.Entry(tab_order)
entry_order_date.grid(row=1, column=1, padx=5, pady=5)

label_purchaser_amount = tk.Label(tab_order, text="Purchaser Amount:")
label_purchaser_amount.grid(row=2, column=0, padx=5, pady=5)
entry_purchaser_amount = tk.Entry(tab_order)
entry_purchaser_amount.grid(row=2, column=1, padx=5, pady=5)

button_add_order = tk.Button(tab_order, text="Add Order", command=insert_order)
button_add_order.grid(row=3, column=0, pady=10)

button_update_order = tk.Button(tab_order, text="Update Order", command=update_order)
button_delete_order = tk.Button(tab_order, text="Delete Order", command=delete_order)

# Treeview สำหรับแสดงข้อมูลคำสั่งซื้อ
tree_order = ttk.Treeview(tab_order, columns=("Order_ID", "Customer_ID", "Date", "Purchaser_amount"), show='headings')
tree_order.heading("Order_ID", text="Order ID")
tree_order.heading("Customer_ID", text="Customer ID")
tree_order.heading("Date", text="Date")
tree_order.heading("Purchaser_amount", text="Purchaser Amount")
tree_order.grid(row=4, columnspan=3, pady=10, padx=5, sticky="nsew")
tree_order.bind("<<TreeviewSelect>>", on_order_select)

# เติมข้อมูลลงใน treeview
populate_treeview(tree_order, fetch_data("SELECT * FROM `Order`"), ["Order_ID", "Customer_ID", "Date", "Purchaser_amount"])

# แท็บสำหรับเพิ่มรายละเอียดคำสั่งซื้อ
tab_order_line = ttk.Frame(notebook)
notebook.add(tab_order_line, text='Order Line')

label_order_id = tk.Label(tab_order_line, text="Order ID:")
label_order_id.grid(row=0, column=0, padx=5, pady=5)
entry_order_id = tk.Entry(tab_order_line)
entry_order_id.grid(row=0, column=1, padx=5, pady=5)

label_product_id = tk.Label(tab_order_line, text="Product ID:")
label_product_id.grid(row=1, column=0, padx=5, pady=5)
entry_product_id = tk.Entry(tab_order_line)
entry_product_id.grid(row=1, column=1, padx=5, pady=5)

label_quantity = tk.Label(tab_order_line, text="Quantity:")
label_quantity.grid(row=2, column=0, padx=5, pady=5)
entry_quantity = tk.Entry(tab_order_line)
entry_quantity.grid(row=2, column=1, padx=5, pady=5)

button_add_order_line = tk.Button(tab_order_line, text="Add Order Line", command=insert_order_line)
button_add_order_line.grid(row=3, column=0, pady=10)

button_update_order_line = tk.Button(tab_order_line, text="Update Order Line", command=update_order_line)
button_delete_order_line = tk.Button(tab_order_line, text="Delete Order Line", command=delete_order_line)

# Treeview สำหรับแสดงข้อมูลรายละเอียดคำสั่งซื้อ
tree_order_line = ttk.Treeview(tab_order_line, columns=("Order_ID", "Product_ID", "Quantity"), show='headings')
tree_order_line.heading("Order_ID", text="Order ID")
tree_order_line.heading("Product_ID", text="Product ID")
tree_order_line.heading("Quantity", text="Quantity")
tree_order_line.grid(row=4, columnspan=3, pady=10, padx=5, sticky="nsew")
tree_order_line.bind("<<TreeviewSelect>>", on_order_line_select)

# เติมข้อมูลลงใน treeview
populate_treeview(tree_order_line, fetch_data("SELECT * FROM Order_Line"), ["Order_ID", "Product_ID", "Quantity"])

# แท็บสำหรับเติมสินค้า
tab_restock = ttk.Frame(notebook)
notebook.add(tab_restock, text='Restock')

label_restock_product_id = tk.Label(tab_restock, text="Product ID:")
label_restock_product_id.grid(row=0, column=0, padx=5, pady=5)
entry_restock_product_id = tk.Entry(tab_restock)
entry_restock_product_id.grid(row=0, column=1, padx=5, pady=5)

label_restock_date = tk.Label(tab_restock, text="Restock Date (YYYY-MM-DD):")
label_restock_date.grid(row=1, column=0, padx=5, pady=5)
entry_restock_date = tk.Entry(tab_restock)
entry_restock_date.grid(row=1, column=1, padx=5, pady=5)

label_stock_date = tk.Label(tab_restock, text="Stock Date (YYYY-MM-DD):")
label_stock_date.grid(row=2, column=0, padx=5, pady=5)
entry_stock_date = tk.Entry(tab_restock)
entry_stock_date.grid(row=2, column=1, padx=5, pady=5)

label_restock_quantity = tk.Label(tab_restock, text="Quantity:")
label_restock_quantity.grid(row=3, column=0, padx=5, pady=5)
entry_restock_quantity = tk.Entry(tab_restock)
entry_restock_quantity.grid(row=3, column=1, padx=5, pady=5)

button_add_restock = tk.Button(tab_restock, text="Add Restock", command=insert_restock)
button_add_restock.grid(row=4, column=0, pady=10)

button_update_restock = tk.Button(tab_restock, text="Update Restock", command=update_restock)
button_delete_restock = tk.Button(tab_restock, text="Delete Restock", command=delete_restock)

# Treeview สำหรับแสดงข้อมูลการเติมสินค้า
tree_restock = ttk.Treeview(tab_restock, columns=("Product_ID", "Restock_Date", "Stock_Date", "Quantity"), show='headings')
tree_restock.heading("Product_ID", text="Product ID")
tree_restock.heading("Restock_Date", text="Restock Date")
tree_restock.heading("Stock_Date", text="Stock Date")
tree_restock.heading("Quantity", text="Quantity")
tree_restock.grid(row=5, columnspan=3, pady=10, padx=5, sticky="nsew")
tree_restock.bind("<<TreeviewSelect>>", on_restock_select)

# เติมข้อมูลลงใน treeview
populate_treeview(tree_restock, fetch_data("SELECT * FROM Restock"), ["Product_ID", "Restock_Date", "Stock_Date", "Quantity"])

# แท็บสำหรับเพิ่มข้อมูลสินค้า
tab_product = ttk.Frame(notebook)
notebook.add(tab_product, text='Product')

label_product_name = tk.Label(tab_product, text="Product Name:")
label_product_name.grid(row=0, column=0, padx=5, pady=5)
entry_product_name = tk.Entry(tab_product)
entry_product_name.grid(row=0, column=1, padx=5, pady=5)

label_product_price = tk.Label(tab_product, text="Price:")
label_product_price.grid(row=1, column=0, padx=5, pady=5)
entry_product_price = tk.Entry(tab_product)
entry_product_price.grid(row=1, column=1, padx=5, pady=5)

button_add_product = tk.Button(tab_product, text="Add Product", command=insert_product)
button_add_product.grid(row=2, column=0, pady=10)

button_update_product = tk.Button(tab_product, text="Update Product", command=update_product)
button_delete_product = tk.Button(tab_product, text="Delete Product", command=delete_product)

# Treeview สำหรับแสดงข้อมูลสินค้า
tree_product = ttk.Treeview(tab_product, columns=("Product_ID", "Product_Name", "Price"), show='headings')
tree_product.heading("Product_ID", text="Product ID")
tree_product.heading("Product_Name", text="Product Name")
tree_product.heading("Price", text="Price")
tree_product.grid(row=3, columnspan=3, pady=10, padx=5, sticky="nsew")
tree_product.bind("<<TreeviewSelect>>", on_product_select)

# เติมข้อมูลลงใน treeview
populate_treeview(tree_product, fetch_data("SELECT * FROM Product"), ["Product_ID", "Product_Name", "Price"])

root.mainloop()

# ปิดการเชื่อมต่อฐานข้อมูลเมื่อโปรแกรมสิ้นสุดการทำงาน
db.close()
