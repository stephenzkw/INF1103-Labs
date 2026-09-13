total_inventory = 0
failed_entries = 0

while True:
    entry = input("Enter stock quantity (or type 'quit' to exit): ")

    if entry.lower() == 'quit':
        break

    if failed_entries > 2:
        print("Too many failed entries, exiting the program.")
        break

    if not entry.isdigit():
        print("Invalid input. Please enter a valid number.")
        failed_entries += 1
        continue

    total_inventory += int(entry)

    if total_inventory > 500:
        print("Warning: Total inventory exceeds 500 units.")
