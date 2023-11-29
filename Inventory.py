import sqlite3

# Inventory Class
class Inventory:
    def __init__(self, databaseName='', tableName=''):
        self.databaseName = databaseName
        self.tableName = tableName

    def connect_to_db(self):
        # Replace this with your actual database connection logic
        return sqlite3.connect(self.databaseName)

    def viewInventory(self):
        # Displays all items in the inventory in some formatted way
        conn = self.connect_to_db()
        cursor = conn.execute(f"SELECT * FROM {self.tableName}")
        
        # Replace this with actual formatting logic based on your table structure
        for row in cursor.fetchall():
            print(row)

        conn.close()

    def searchInventory(self):
        # Asks for a *title*, checks the database to see if a result is returned on that name.
        # If so, display all results. If not, the user is informed their search failed
        title = input("Enter the title to search: ")

        conn = self.connect_to_db()
        query = f"SELECT * FROM {self.tableName} WHERE Title LIKE ?"
        cursor = conn.execute(query, ('%' + title + '%',))

        # Replace this with actual formatting logic based on your table structure
        for row in cursor.fetchall():
            print(row)

        conn.close()

    def decreaseStock(self, ISBN, quantity=1):
        # Called with a single ISBN parameter and decreases the stock number in the appropriate database for the appropriate ISBN
        conn = self.connect_to_db()

        # Replace this with actual database update logic based on your table structure
        query = f"UPDATE {self.tableName} SET Stock = Stock - ? WHERE ISBN = ?"
        conn.execute(query, (quantity, ISBN))
        conn.commit()

        print(f"Decreased stock for ISBN {ISBN}")

        conn.close()

# Main File
# (The rest of the code remains the same)
