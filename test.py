# User database - update once external database is made
users = {
    "operator": {"password": "operator", "type": "operator"},
    "buyer": {"password": "buyer", "type": "buyer"},
    "seller": {"password": "seller", "type": "seller"}
}

# Function to validate user login
def login(username, password):
    if username in users and users[username]["password"] == password:
        print(f"Welcome, {username}! You are logged in as {users[username]['type']}.")
        return True
    else:
        print("Invalid username or password.")
        return False

# Main function
def main():
    print("Welcome to the Python Login System")

    # Login loop
    while True:
        print("\nSelect user type:")
        print("1. operator")
        print("2. buyer")
        print("3. seller")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter operator username: ")
            password = input("Enter operator password: ")

            if login(username, password) and users[username]["type"] == "operator":
                # operator-specific actions can be performed here
                print("operator actions here...")
                # continue with operator solution

        elif choice == "2":
            username = input("Enter buyer username: ")
            password = input("Enter buyer password: ")

            if login(username, password) and users[username]["type"] == "buyer":
                # buyer-specific actions can be performed here
                print("buyer actions here...")
                # continue with choice solution

        elif choice == "3":
            username = input("Enter seller username: ")
            password = input("Enter seller password: ")

            if login(username, password) and users[username]["type"] == "seller":
                # Regular seller-specific actions can be performed here
                print("Regular user actions here...")
                # continue with seller solution

        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()