import tkinter as tk
from tkinter import ttk
import sqlite3 

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT NOT NULL,
                        order_detail TEXT NOT NULL,
                        status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def add_order():
    client_name = client_name_entry.get().strip()
    order_detail = order_detail_entry.get().strip()
    if not client_name or not order_detail:
        messagebox.showwarning("Пустые поля", "Заполни имя и детали заказа.")
        return

    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (client_name, order_detail, status) VALUES (?, ?, ?)",
        (client_name, order_detail, "Новый")
    )
    conn.commit()
    conn.close()

    # очистка полей
    client_name_entry.delete(0, tk.END)
    order_detail_entry.delete(0, tk.END)

    # КЛЮЧЕВОЕ: обновляем таблицу в окне
    view_orders()

def view_orders():
    for i in tree.get_children():
        tree.delete(i)
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()


app = tk.Tk()
app.title("Система управления заказами")

tk.Label(app, text="Имя клиента:", font=("Arial", 16)).pack(pady=10)

client_name_entry = tk.Entry(app, font=("Arial", 16))
client_name_entry.pack(pady=10)

tk.Label(app, text="Детали заказа:", font=("Arial", 16)).pack(pady=10)

order_detail_entry = tk.Entry(app, font=("Arial", 16))
order_detail_entry.pack(pady=10)

add_button = tk.Button(app, text="Добавить заказ", font=("Arial", 16), command=add_order)
add_button.pack(pady=20)
columns = ("id", "client_name", "order_detail", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(pady=20)

init_db()
view_orders()
app.mainloop()