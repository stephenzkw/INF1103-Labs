def get_valid_input():
    entry = input("Enter stock quantity (or type 'quit' to exit): ")

    if entry.lower() == 'quit':
        return "quit"

    if entry.startswith("-") and entry[1:].isdigit(): 
        print("Negative values are not allowed")
        return None

    if not entry.isdigit():
        print("Invalid entry. Please enter a valid number.")
        return None

    return int(entry)

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return round(amount * 0.10, 2)

def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()
            total = int(lines[0].strip())
            history = [int(line.strip()) for line in lines[1:]]
            return total, history
    except FileNotFoundError:
        return 0, []

def save_inventory(total, history):
    with open("inventory.txt", "w") as file:
        file.write(str(total) + "\n")
        for entry in history:
            file.write(str(entry) + "\n")

def generate_report(total_units, failed_attempts, exit_reason):
    if exit_reason == "too many invalid inputs":
        print("\n🚫 Process Terminated: too many invalid inputs.")
        print("Please restart and enter valid stock quantities.")
    elif exit_reason == "capacity exceeded":
        print("\n📦 Process Halted: storage capacity exceeded!")
        print(f"Total Units Processed: {total_units}")
        print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    else:
        print("\n--- End of Day Report ---")
        print(f"Total Units Processed: {total_units}")
        print(f"Number of Failed/Rejected Entries: {failed_attempts}")

def main():
    total_inventory = 0
    failed_entries = 0
    exit_reason = "quit"  #only changes if forced exit happens

    while True:
        entry = get_valid_input()

        if entry == "quit":
            break

        if entry is None:
            failed_entries += 1
            if failed_entries > 2:
                exit_reason = "too many invalid inputs"
                break
            continue

        total_inventory = process_delivery(total_inventory, entry)
        print(f"Added {entry} units. Current total units: {total_inventory}")

        if total_inventory > 500:
            exit_reason = "capacity exceeded"
            break
        elif total_inventory > 450:
            print(f"Alert! Approaching capacity ({total_inventory}/500).")

    generate_report(total_inventory, failed_entries, exit_reason)

main()