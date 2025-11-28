import os
import sqlite3
from unicodedata import category


class Database:
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'shop.db'))
        self.cursor = self.con.cursor()

    # def created_tables(self):
    #     self.cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS categories(
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         name VARCHAR(50)
    #     );
    #     """)
    #
    #     self.cursor.execute("""
    #                         CREATE TABLE IF NOT EXISTS products
    #                         (
    #                             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                             name VARCHAR(100),
    #                             price FLOAT,
    #                             description TEXT,
    #                             image TEXT,
    #                             category_id INTEGER,
    #                             FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    #                             );
    #                         """)
    #
    #     self.cursor.execute("""
    #                         CREATE TABLE IF NOT EXISTS cart
    #                         (
    #                             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                             user_id VARCHAR(20),
    #                             product_id INTEGER,
    #                             count INTEGER DEFAULT 1,
    #                             total_price INTEGER,
    #                             FOREIGN KEY( user_id) REFERENCES users(user_id),
    #                             FOREIGN KEY(product_id) REFERENCES products(id)
    #                             )
    #                         """)
    #
    #     self.cursor.execute("""
    #                         CREATE TABLE IF NOT EXISTS orders
    #                         (
    #                             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                             user_id VARCHAR(20),
    #                             products TEXT,
    #                             phone TEXT,
    #                             lokation TEXT,
    #                             tolov_turi TEXT,
    #                             sana TEXT
    #                         )
    #     """)
    #     self.cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS users (
    #             user_id VARCHAR(20) PRIMARY KEY,
    #             locale TEXT
    #         );
    #     """)
    #
    #     self.con.commit()

    def set_user_locale(self, user_id: int, locale: str):
        self.cursor.execute("INSERT OR REPLACE INTO app_user (user_id, locale) VALUES (?, ?)", (user_id, locale))
        self.con.commit()

    def get_user_locale(self, user_id: int):
        self.cursor.execute("SELECT locale FROM app_user WHERE user_id = ?", (user_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def add_order(self, user_id, products, phone, lokation, tolov_turi, sana):
        self.cursor.execute("""
                            INSERT INTO app_order (user_id, products, phone, lokation, tolov_turi, sana)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """, (user_id, products, phone, lokation, tolov_turi, sana))
        self.con.commit()

    def get_orders(self, user_id):
        self.cursor.execute("SELECT * FROM app_order WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def get_orders_by_id(self, id):
        self.cursor.execute("SELECT * FROM app_order WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def add_cart_item(self, user_id, product_id, count, total_price):
        self.cursor.execute("""
                            INSERT INTO app_cart (user_id, product_id, count, total_price)
                            VALUES (?, ?, ?, ?)
                            """, (user_id, product_id, count, total_price))
        self.con.commit()

    def clear_cart_items(self, user_id):
        self.cursor.execute("DELETE FROM app_cart WHERE user_id=?", (user_id,))
        self.con.commit()

    def get_cart_items(self, user_id):
        self.cursor.execute("SELECT * FROM app_cart WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def get_categories(self):
        self.cursor.execute("SELECT * FROM app_category")
        return self.cursor.fetchall()

    def add_category(self, name):
        self.cursor.execute("INSERT INTO app_category (name) VALUES (?)", (name,))
        self.con.commit()

    def add_products(self, name, price, description, image, category_id):
        self.cursor.execute("""
                            INSERT INTO app_product (name, price, description, image, category_id)
                            VALUES (?, ?, ?, ?, ?)
                            """, (name, price, description, image, category_id))
        self.con.commit()

    def get_products_by_category(self, category_id):
        self.cursor.execute("SELECT * FROM app_product WHERE category_id = ?", (category_id,))
        return self.cursor.fetchall()

    def get_product(self, product_id):
        self.cursor.execute("SELECT * FROM app_product WHERE id = ?", (product_id,))
        return self.cursor.fetchone()

    def delete_table(self):
        self.cursor.execute("DROP TABLE ordered")
        self.con.commit()

db = Database()
# db.delete_table()
# db.created_tables()
# db.add_category('Mevalar')
# db.add_products('Olma', 2324, 'qizil olma golden', 'sdvsv', 1)
