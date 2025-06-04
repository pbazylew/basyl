import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = 'inventory.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Lagerbestand Verwaltung')
        self.geometry('600x400')
        self.create_widgets()
        self.refresh_products()

    def create_widgets(self):
        form = ttk.Frame(self)
        form.pack(fill='x', padx=10, pady=10)

        ttk.Label(form, text='Produktname').grid(row=0, column=0, sticky='w')
        self.entry_name = ttk.Entry(form)
        self.entry_name.grid(row=0, column=1, sticky='ew')

        ttk.Label(form, text='Anzahl').grid(row=1, column=0, sticky='w')
        self.entry_quantity = ttk.Entry(form)
        self.entry_quantity.grid(row=1, column=1, sticky='ew')

        ttk.Label(form, text='Preis').grid(row=2, column=0, sticky='w')
        self.entry_price = ttk.Entry(form)
        self.entry_price.grid(row=2, column=1, sticky='ew')

        form.columnconfigure(1, weight=1)

        self.add_btn = ttk.Button(form, text='Produkt hinzufügen', command=self.add_product)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self, columns=('name', 'quantity', 'price'), show='headings', selectmode='browse')
        self.tree.heading('name', text='Name')
        self.tree.heading('quantity', text='Anzahl')
        self.tree.heading('price', text='Preis')
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        actions = ttk.Frame(self)
        actions.pack(fill='x', padx=10, pady=5)
        ttk.Button(actions, text='Aktualisieren', command=self.edit_product).pack(side='left')
        ttk.Button(actions, text='Löschen', command=self.delete_product).pack(side='left')

    def refresh_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        for row in cur.execute('SELECT id, name, quantity, price FROM products'):
            self.tree.insert('', 'end', iid=row[0], values=row[1:])
        conn.close()

    def add_product(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        if not name or not quantity or not price:
            messagebox.showerror('Fehler', 'Bitte alle Felder ausfüllen.')
            return
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror('Fehler', 'Ungültiger Wert für Anzahl oder Preis.')
            return
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)', (name, quantity, price))
        conn.commit()
        conn.close()
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        self.refresh_products()

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('Info', 'Bitte ein Produkt auswählen.')
            return
        pid = selected[0]
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('DELETE FROM products WHERE id=?', (pid,))
        conn.commit()
        conn.close()
        self.refresh_products()

    def edit_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo('Info', 'Bitte ein Produkt auswählen.')
            return
        pid = selected[0]
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()
        if not name or not quantity or not price:
            messagebox.showerror('Fehler', 'Bitte alle Felder ausfüllen.')
            return
        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror('Fehler', 'Ungültiger Wert für Anzahl oder Preis.')
            return
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute('UPDATE products SET name=?, quantity=?, price=? WHERE id=?', (name, quantity, price, pid))
        conn.commit()
        conn.close()
        self.refresh_products()


if __name__ == '__main__':
    init_db()
    app = InventoryApp()
    app.mainloop()
