# user class
import sqlite3
class User:
    
    def __init__(self, databaseName=None, tableName=None):
        self.databaseName = "databaseTables.db"
        self.tableName = "Users"
        self.loggedIn = False
        self.userID = ''

    def connectDB(self):
        return sqlite3.connect(self.databaseName)
    
    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        conn = self.connectDB()
        cur = conn.cursor()
        cur.execute(f"SELECT UserID FROM {self.tableName} WHERE Username = ? AND Password = ?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            self.userID = user[0]
            self.loggedIn = True
            return True
        else:
            print("Error: incorrect password or username.")

    
    def logout(self):
        if self.loggedIn:
            print("Logging out...")
            self.loggedIn = False
            self.userID = ''
            return True
        else:
            print("You are not logged in.")
            return False
    
    def viewAccInfo(self):
        if self.loggedIn:
            conn = self.connectDB()
            query = f"SELECT * FROM {self.tableName} WHERE UserID = ?"
            cursor = conn.execute(query, (self.userID,))
            user_data = cursor.fetchone()

            print(f"Debug: self.userID = {self.userID}, user_data = {user_data}")  # Debug line

            if user_data:
                print(f"Viewing account information for user {self.userID}:")
                print(f"Username: {user_data[1]}")
                print(f"Email: {user_data[2]}")
                print(f"First Name: {user_data[4]}")
                print(f"Last Name: {user_data[5]}")
                print(f"Address: {user_data[6]}")
                print(f"City: {user_data[7]}")
                print(f"State: {user_data[8]}")
                print(f"Zip: {user_data[9]}")
                print(f"Payment: {user_data[10]}")
                
            else:
                print("User not found.")

            conn.close()
        else:
            print("You need to be logged in to view account information.")
    
    def createAcc(self):
        if not self.loggedIn:
            new_username = input("Enter your Username: ")
            new_email = input("Enter your email: ")
            new_password = input("Enter your password: ")
            new_first_name = input("Enter your first name: ")
            new_last_name = input("Enter your last name: ")
            new_address = input("Enter your address: ")
            new_city = input("Enter your city: ")
            new_state = input("Enter your state: ")
            new_zip = input("Enter your zip code: ")
            new_payment = input("Enter your payment method: ")

            conn = self.connectDB()
            query = f"INSERT INTO {self.tableName} (Username, Email, Password, FirstName, LastName, Address, City, State, Zip, Payment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            conn.execute(query, (new_username, new_email, new_password, new_first_name, new_last_name, new_address, new_city, new_state, new_zip, new_payment))
            conn.commit()

            # Retrieve the last inserted row id (UserID)
            cursor = conn.execute("SELECT last_insert_rowid()")
            self.userID = cursor.fetchone()[0]
            self.loggedIn = True

            print(f"Debug: new_email = {new_email}, self.userID = {self.userID}")  # Debug line

            print(f"Account created for {new_email} with UserID: {self.userID}")  # Include UserID in the output

            conn.close()
        else:
            print("You need to log out before creating a new account.")


    
    def getLoggedIn(self):
        return self.loggedIn
    
    def getUserID(self):
        return self.userID
