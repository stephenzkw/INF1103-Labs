import json
from abc import ABC, abstractmethod


class Supplier:
    """Supplies products. Exists independently of any Product."""

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Supplier Name: {self.__name}")
        print(f"Contact Email: {self.__contact_email}")

    def to_dict(self) -> dict:
        return {
            "id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Supplier":
        return cls(data["id"], data["name"], data["contact_email"])

class CanBeShipped(ABC):
    """Contract for anything that can be shipped."""

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the cost of shipping this item."""
        pass


class Product(ABC):
    """Common data and behaviour shared by all products."""

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier: Supplier = supplier

    # Read-only access (getters)
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_supplier(self) -> Supplier:
       return self.__supplier

    # Behaviour shared by all products
    def update_stock(self, quantity):
        """Set the stock to a new quantity. The Product decides what is valid."""
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    def __str__(self):
        """One-line summary of the common details."""
        return (f"ID: {self.__product_id} | Name: {self.__name} | "
                f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }

    # Abstract: every subclass MUST implement this
    @abstractmethod
    def get_fulfilment_info(self):
        pass


# Physical Product
class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped. Weight is in kilograms."""

    BASE_SHIPPING = 5.00     # Flat fee in dollars
    RATE_PER_KG = 2.00       # Dollars per kilogram

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def __str__(self):
        return super().__str__() + f" | Weight: {self.__weight} kg"

    def get_fulfilment_info(self):
        return "Physical product: requires storage and physical shipping."

    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING + self.RATE_PER_KG * self.__weight

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data, supplier: Supplier):
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier, data.get("weight", 0.0))


# Digital Product
class DigitalProduct(Product):
    """A product delivered digitally. Download size is in megabytes."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def __str__(self):
        return super().__str__() + f" | Download Size: {self.__download_size} MB"

    def get_fulfilment_info(self):
        return "Digital product: delivered digitally by download, no shipping needed."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data, supplier: Supplier):
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   supplier, data["download_size"])


# Inventory
class Inventory:

    def __init__(self):
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add an existing Product. Returns False if the ID already exists."""
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        """Remove the Product from this inventory and hand it back."""
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        """Return the matching Product, or None if it cannot be found."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("Current Inventory")
        print("-" * 50)
        for product in self.__products:
            print(product)
        print("-" * 50)

    def get_all_products(self) -> list[Product]:
        return list(self.__products)


# OrderLine
class OrderLine:
    """One product and quantity within an Order. Created and managed only by Order."""

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} x {self.__quantity} "
              f"@ ${self.__product.get_price():.2f} = ${self.calculate_subtotal():.2f}")


# Order
class Order:
    """An order made up of order lines. The Order creates and manages its own lines."""

    def __init__(self, order_id: str):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove line for this product. Returns False if none."""
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        print("-" * 50)
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Total: ${self.calculate_total():.2f}")
        print("-" * 50)

# File handling
PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def create_product_from_dict(data: dict, suppliers: dict) -> Product:
    """Rebuild a product. Products with the same supplier id share one Supplier object."""
    supplier_data = data["supplier"]
    supplier_id = supplier_data["id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier.from_dict(supplier_data)
    product_type = data.get("type", "physical")
    return PRODUCT_TYPES[product_type].from_dict(data, suppliers[supplier_id])


def load_inventory():
    inventory = Inventory()
    suppliers = {}
    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)
            for item in data:
                inventory.add_product(create_product_from_dict(item, suppliers))
            print("inventory.json found.")
            print("Inventory loaded successfully.")
    except FileNotFoundError:
        print("inventory.json not found. Starting with default inventory.")
        tech = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")
        software = Supplier("S002", "SoftWorks Pte Ltd", "hello@softworks.com")
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, tech, 2.1))
        inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, tech, 0.1))
        inventory.add_product(PhysicalProduct("P003", "Keyboard", 45.00, 25, tech, 0.8))
        inventory.add_product(DigitalProduct("P004", "Antivirus License", 59.90, 100, software, 150.0))
    return inventory


def save_inventory(inventory):
    data = [product.to_dict() for product in inventory.get_all_products()]
    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=4)
    print("Inventory saved successfully.")


# Menu actions
def add_product(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type: ")
    if product_type not in ("1", "2"):
        print("Invalid product type. Product not added.")
        return

    product_id = input("Product ID: ")
    name = input("Product Name: ")
    print("Supplier details")
    supplier = Supplier(input("Supplier ID: "), input("Supplier Name: "),
                        input("Supplier Email: "))
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == "1":
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
        else:
            download_size = float(input("Download Size (MB): "))
            product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
    except ValueError as error:
        print(f"Invalid input. Product not added. ({error})")
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("A product with that ID already exists.")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ")

    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    try:
        new_stock = int(input("New Stock Quantity: "))
        product.update_stock(new_stock)
        print("Stock updated successfully!")
    except ValueError as error:
        """Covers both non-numeric input and Product, rejecting negative value"""
        print(f"Stock not updated: {error}")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ")

    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 50)
    product.display_information()
    product.get_supplier().display_information()
    print(product.get_fulfilment_info())
    # Only products that signed the CanBeShipped contract have a shipping cost
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 50)


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
            inventory.display_all()
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


if __name__ == "__main__":
    main()