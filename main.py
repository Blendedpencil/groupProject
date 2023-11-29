import sqlite3
from User import User
from Inventory import Inventory
from Cart import Cart


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
        elif choice == "8":
            print(user.getLoggedIn())
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
