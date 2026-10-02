import json

def load_inventory():
    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)
            print("inventory.json found.")
            print("Inventory loaded successfully.")
            return data
    except FileNotFoundError:
        print("inventory.json not found. Starting with default inventory.")
        return [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
    ]

def save_inventory(inventory):
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)
    print("Inventory saved successfully.")

def display_all(inventory):
    print("Current Inventory")
    print("-" * 50)
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 50)

def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    }

    inventory.append(new_product)
    print("Product added successfully!")

def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ")

    for product in inventory:
        if product["id"] == product_id:
            print("Product Found:")
            print(f"Name: {product['name']}")
            print(f"Current Stock: {product['stock']}")
            new_stock = int(input("New Stock Quantity: "))
            product["stock"] = new_stock
            print("Stock updated successfully!")
            return

    print("Product not found.")

def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ")

    for product in inventory:
        if product["id"] == product_id:
            print("Product Found")
            print("-" * 50)
            print(f"ID: {product['id']}")
            print(f"Name: {product['name']}")
            print(f"Price: ${product['price']:.2f}")
            print(f"Stock: {product['stock']}")
            print("-" * 50)
            return

    print("Product not found.")

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        choice = input("Enter option: ")

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("Saving inventory...")
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.")

main()