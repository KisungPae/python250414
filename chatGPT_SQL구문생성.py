import sqlite3
import random

class ProductDatabase:
    def __init__(self, db_name="electronics.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Create the products table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.connection.commit()

    def insert_product(self, product_name, price):
        """Insert a new product into the database."""
        self.cursor.execute('''
            INSERT INTO products (product_name, price)
            VALUES (?, ?)
        ''', (product_name, price))
        self.connection.commit()

    def update_product(self, product_id, product_name=None, price=None):
        """Update an existing product's name and/or price."""
        if product_name and price:
            self.cursor.execute('''
                UPDATE products
                SET product_name = ?, price = ?
                WHERE product_id = ?
            ''', (product_name, price, product_id))
        elif product_name:
            self.cursor.execute('''
                UPDATE products
                SET product_name = ?
                WHERE product_id = ?
            ''', (product_name, product_id))
        elif price:
            self.cursor.execute('''
                UPDATE products
                SET price = ?
                WHERE product_id = ?
            ''', (price, product_id))
        self.connection.commit()

    def delete_product(self, product_id):
        """Delete a product from the database."""
        self.cursor.execute('''
            DELETE FROM products
            WHERE product_id = ?
        ''', (product_id,))
        self.connection.commit()

    def select_products(self):
        """Retrieve all products from the database."""
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.connection.close()

# Sample data generation and usage
if __name__ == "__main__":
    db = ProductDatabase()

    # Insert 100 sample products
    for i in range(1, 101):
        product_name = f"Product_{i}"
        price = round(random.uniform(10.0, 1000.0), 2)
        db.insert_product(product_name, price)

    # Fetch and display all products
    products = db.select_products()
    for product in products:
        print(product)

    # Example operations
    db.update_product(1, product_name="Updated_Product_1", price=999.99)
    db.delete_product(2)

    # Fetch and display updated products
    print("\nAfter Updates:")
    products = db.select_products()
    for product in products:
        print(product)

    db.close()