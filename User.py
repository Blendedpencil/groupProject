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
            print(user_data)
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
