total_inventory = 0
failed_entries = 0
exit_reason = "quit" #only changes if forced exit happens

while True:
    entry = input("Enter stock quantity (or type 'quit' to exit): ")

    if entry.lower() == 'quit':
        break

    if entry.startswith("-") and entry[1:].isdigit():
        print("Negative values are not allowed")
        failed_entries += 1

        if failed_entries > 2:
            exit_reason = "too many invalid inputs"
            break

        continue

    if not entry.isdigit():
        print("Invalid entry. Please enter a valid number.")
        failed_entries += 1

        if failed_entries > 2:
            exit_reason = "too many invalid inputs"
            break

        continue

    total_inventory += int(entry)
    print(f"Added {entry} units. Current total units: {total_inventory}")

    if total_inventory > 500:
        exit_reason = "capacity exceeded"
        break
    elif total_inventory > 450:
        print(f"Alert! Approaching capacity ({total_inventory}/500).")

if exit_reason == "too many invalid inputs":
    print("\n🚫 Process Terminated: too many invalid inputs.")
    print("Please restart and enter valid stock quantities.")

elif exit_reason == "capacity exceeded":
    print("\n📦 Process Halted: storage capacity exceeded!")
    print(f"Total Units Processed: {total_inventory}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")

else:
    print ("\n---End of Day Report---")
    print(f"Total Units Processed: {total_inventory}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")