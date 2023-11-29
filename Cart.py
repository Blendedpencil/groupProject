import sqlite3

# Cart Class
class Cart:
    def __init__(self, inventory, databaseName='', tableName='Cart'):
        self.inventory = inventory
        self.databaseName = databaseName
        self.tableName = tableName
        self.cart_contents = {}

    def connect_to_db(self):
        return sqlite3.connect(self.databaseName)

    def viewCart(self, userID):
        print(f"Cart for user {userID}: {self.cart_contents}")

    def addToCart(self, userID, ISBN):
        if ISBN not in self.cart_contents:
            self.cart_contents[ISBN] = 1
        else:
            self.cart_contents[ISBN] += 1
        print(f"Added ISBN {ISBN} to the cart for user {userID}")

    def removeFromCart(self, userID, ISBN):
        if ISBN in self.cart_contents:
            if self.cart_contents[ISBN] > 1:
                self.cart_contents[ISBN] -= 1
            else:
                del self.cart_contents[ISBN]
            print(f"Removed one instance of ISBN {ISBN} from the cart for user {userID}")
        else:
            print(f"ISBN {ISBN} not found in the cart for user {userID}")

    def checkOut(self, userID):
        total_items = sum(self.cart_contents.values())
        print(f"Checked out {total_items} items from the cart for user {userID}")

        for ISBN, quantity in self.cart_contents.items():
            self.inventory.decreaseStock(ISBN, quantity)

        self.cart_contents.clear()
