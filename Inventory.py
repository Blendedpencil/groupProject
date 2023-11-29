import sqlite3
# Inventory Class
class Inventory:
    def __init__(self, databaseName='', tableName='Inventory'):
        self.databaseName = databaseName
        self.tableName = tableName

    def connect_to_db(self):
        return sqlite3.connect(self.databaseName)

    def viewInventory(self):
        conn = self.connect_to_db()
        cursor = conn.execute(f"SELECT * FROM {self.tableName}")
        
        for row in cursor.fetchall():
            print(row)

        conn.close()

    def searchInventory(self):
        title = input("Enter the title to search: ")

        conn = self.connect_to_db()
        query = f"SELECT * FROM {self.tableName} WHERE Title LIKE ?"
        cursor = conn.execute(query, ('%' + title + '%',))

        for row in cursor.fetchall():
            print(row)

        conn.close()

    def decreaseStock(self, ISBN, quantity=1):
        conn = self.connect_to_db()

        query = f"UPDATE {self.tableName} SET Stock = Stock - ? WHERE ISBN = ?"
        conn.execute(query, (quantity, ISBN))
        conn.commit()

        print(f"Decreased stock for ISBN {ISBN}")

        conn.close()

