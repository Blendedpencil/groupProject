import sqlite3

# User Class
class User:
    def __init__(self, databaseName='', tableName='User'):
        self.databaseName = databaseName
        self.tableName = tableName
        self.loggedIn = False
        self.userID = ''

    def connect_to_db(self):
        return sqlite3.connect(self.databaseName)

    def login(self):
        if not self.loggedIn:
            entered_email = input("Enter your email: ")
            entered_password = input("Enter your password: ")

            conn = self.connect_to_db()
            query = f"SELECT * FROM {self.tableName} WHERE Email = ? AND Password = ?"
            cursor = conn.execute(query, (entered_email, entered_password))
            user_data = cursor.fetchone()

            if user_data:
                print("Login successful!")
                self.userID = str(user_data[0])  # Adjust index if needed
                self.loggedIn = True
                conn.close()
                return True
            else:
                print("Invalid email or password. Login failed.")
                conn.close()
                return False
        else:
            print("You are already logged in.")
            return False

    def logout(self):
        if self.loggedIn:
            print("Logging out...")
            self.loggedIn = False
            self.userID = ''
            return True
        else:
            print("You are not logged in.")
            return False

    def viewAccountInformation(self):
        if self.loggedIn:
            conn = self.connect_to_db()
            query = f"SELECT * FROM {self.tableName} WHERE UserID = ?"
            cursor = conn.execute(query, (self.userID,))
            user_data = cursor.fetchone()

            if user_data:
                print(f"Viewing account information for user {self.userID}:")
                print(f"Email: {user_data[1]}")
                print(f"First Name: {user_data[3]}")
                print(f"Last Name: {user_data[4]}")
                print(f"Address: {user_data[5]}")
                print(f"City: {user_data[6]}")
                print(f"State: {user_data[7]}")
                print(f"Zip: {user_data[8]}")
            else:
                print("User not found.")

            conn.close()
        else:
            print("You need to be logged in to view account information.")

    def createAccount(self):
        if not self.loggedIn:
            new_email = input("Enter your email: ")
            new_password = input("Enter your password: ")
            new_first_name = input("Enter your first name: ")
            new_last_name = input("Enter your last name: ")
            new_address = input("Enter your address: ")
            new_city = input("Enter your city: ")
            new_state = input("Enter your state: ")
            new_zip = input("Enter your zip code: ")

            conn = self.connect_to_db()
            query = f"INSERT INTO {self.tableName} (Email, Password, FirstName, LastName, Address, City, State, Zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            conn.execute(query, (new_email, new_password, new_first_name, new_last_name, new_address, new_city, new_state, new_zip))
            conn.commit()

            cursor = conn.execute("SELECT last_insert_rowid()")
            self.userID = cursor.fetchone()[0]
            self.loggedIn = True

            print(f"Account created for {new_email} with UserID: {self.userID}")

            conn.close()
        else:
            print("You need to log out before creating a new account.")

    def _get_user_id(self, email):
        conn = self.connect_to_db()
        query = f"SELECT UserID FROM {self.tableName} WHERE Email = ?"
        cursor = conn.execute(query, (email,))
        user_id = cursor.fetchone()
        conn.close()

        if user_id:
            return str(user_id[0])
        else:
            return None

    def getLoggedIn(self):
        return self.loggedIn

    def getUserID(self):
        return self.userID

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

# Main File
def main():
    combined_db = "database.db"
    inventory_db = "database.db"

    user_table = "User"
    inventory_table = "Inventory"
    cart_table = "Cart"

    user = User(databaseName=combined_db, tableName=user_table)
    inventory = Inventory(databaseName=combined_db, tableName=inventory_table)
    cart = Cart(inventory, databaseName=combined_db, tableName=cart_table)

    while True:
        print("\nMain Menu:")
        print("1. Login")
        print("2. Create Account")
        print("3. Logout")
        print("4. View Account Information")
        print("5. Inventory Information")
        print("6. Cart Information")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user.login()
        elif choice == "2":
            user.createAccount()
        elif choice == "3":
            user.logout()
        elif choice == "4":
            user.viewAccountInformation()
        elif choice == "5":
            print("\nInventory Information Menu:")
            print("1. View Inventory")
            print("2. Search Inventory")
            print("3. Go Back")

            inventory_choice = input("Enter your choice: ")

            if inventory_choice == "1":
                inventory.viewInventory()
            elif inventory_choice == "2":
                inventory.searchInventory()
            elif inventory_choice == "3":
                continue
            else:
                print("Invalid choice. Please try again.")

        elif choice == "6":
            print("\nCart Information Menu:")
            print("1. View Cart")
            print("2. Add Items to Cart")
            print("3. Remove an Item from Cart")
            print("4. Check Out")
            print("5. Go Back")

            cart_choice = input("Enter your choice: ")

            if cart_choice == "1":
                cart.viewCart(user.getUserID())
            elif cart_choice == "2":
                ISBN = input("Enter the ISBN to add to the cart: ")
                cart.addToCart(user.getUserID(), ISBN)
            elif cart_choice == "3":
                ISBN = input("Enter the ISBN to remove from the cart: ")
                cart.removeFromCart(user.getUserID(), ISBN)
            elif cart_choice == "4":
                cart.checkOut(user.getUserID())
            elif cart_choice == "5":
                continue
            else:
                print("Invalid choice. Please try again.")

        elif choice == "7":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
