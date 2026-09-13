total_inventory = 0
failed_entries = 0

while True:
    entry = input("Enter stock quantity (or type 'quit' to exit): ")

    if entry.lower() == 'quit':
        break

    if not entry.isdigit():
        print("Invalid entry. Please enter a valid number.")
        failed_entries += 1

        if failed_entries > 2:
            print("Too many invalid entries. Exiting the program.")
            break

        continue

    total_inventory += int(entry)

    if total_inventory > 500:
        print("Warning! Total Inventory exceeds 500 units.")
        break

print ("---End of Day Report---")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")