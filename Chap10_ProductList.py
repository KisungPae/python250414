import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import uic 
import sqlite3
import os.path 

class ProductDB:
    def __init__(self, db_path="ProductList.db"):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.initialize_db()

    def initialize_db(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                Price INTEGER
            );
        """)
        self.conn.commit()

    def add_product(self, name, price):
        self.cur.execute("INSERT INTO Products (Name, Price) VALUES (?, ?);", (name, price))
        self.conn.commit()

    def update_product(self, product_id, name, price):
        self.cur.execute("UPDATE Products SET Name = ?, Price = ? WHERE id = ?;", (name, price, product_id))
        self.conn.commit()

    def delete_product(self, product_id):
        self.cur.execute("DELETE FROM Products WHERE id = ?;", (product_id,))
        self.conn.commit()

    def get_all_products(self):
        self.cur.execute("SELECT * FROM Products;")
        return self.cur.fetchall()

    def close(self):
        self.conn.close()

form_class = uic.loadUiType("ProductList.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db = ProductDB()  # DB 인스턴스

        # 초기값
        self.id = 0

        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setHorizontalHeaderLabels(["제품ID", "제품명", "가격"])
        self.tableWidget.setTabKeyNavigation(False)

        self.prodID.returnPressed.connect(lambda: self.focusNextChild())
        self.prodName.returnPressed.connect(lambda: self.focusNextChild())
        self.prodPrice.returnPressed.connect(lambda: self.focusNextChild())

        self.tableWidget.doubleClicked.connect(self.doubleClick)

        self.getProduct()  # 초기 데이터 로딩

    def addProduct(self):
        name = self.prodName.text()
        price = self.prodPrice.text()
        if name and price.isdigit():
            self.db.add_product(name, int(price))
            self.getProduct()

    def updateProduct(self):
        product_id = self.prodID.text()
        name = self.prodName.text()
        price = self.prodPrice.text()
        if product_id.isdigit() and name and price.isdigit():
            self.db.update_product(int(product_id), name, int(price))
            self.getProduct()

    def removeProduct(self):
        product_id = self.prodID.text()
        if product_id.isdigit():
            self.db.delete_product(int(product_id))
            self.getProduct()

    def getProduct(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        for row_idx, item in enumerate(self.db.get_all_products()):
            self.tableWidget.insertRow(row_idx)

            itemID = QTableWidgetItem(str(item[0]))
            itemID.setTextAlignment(Qt.AlignRight)
            self.tableWidget.setItem(row_idx, 0, itemID)

            self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(item[1]))

            itemPrice = QTableWidgetItem(str(item[2]))
            itemPrice.setTextAlignment(Qt.AlignRight)
            self.tableWidget.setItem(row_idx, 2, itemPrice)

    def doubleClick(self):
        row = self.tableWidget.currentRow()
        self.prodID.setText(self.tableWidget.item(row, 0).text().strip())
        self.prodName.setText(self.tableWidget.item(row, 1).text().strip())
        self.prodPrice.setText(self.tableWidget.item(row, 2).text().strip())

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoForm = DemoForm()
    demoForm.show()
    sys.exit(app.exec_())
