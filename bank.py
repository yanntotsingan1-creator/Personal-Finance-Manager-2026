# Banking Program

def show_balance(balance):
    print(f"Your balance is: ${balance:.2f}")

def deposit(balance):
    amount = float(input("Enter the amount to deposit: $"))
    if amount <= 0:
        print("Deposit amount must be greater than zero.")
        return balance
    balance += amount
    return balance

def withdraw(balance):
    amount = float(input("Enter the amount to withdraw: $"))
    if amount > balance:
        print("Insufficient funds.")
    else:
        balance -= amount
    return balance

def main():
    balance = 0
    is_running = True

    while is_running:
        print("========================================")
        print("   Banking Program Menu   ")
        print("========================================")
        print("1. Show Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")
        print("========================================")
        choice = input("Enter your choice: ")

        if choice == "1":
            show_balance(balance)
        elif choice == "2":
            balance = deposit(balance)
        elif choice == "3":
            balance = withdraw(balance)
        elif choice == "4":
            is_running = False
        else:
            print("========================================")
            print("Invalid choice. Please try again.")
            print("========================================")
    print("========================================")
    print("Thank you, Have a nice day!")
    print("========================================")

if __name__ == "__main__":
    main()