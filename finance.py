# Personal Finance Management System

from OOP import Account, CheckingAccount, SavingsAccount, Transaction, Card, DebitCard, CreditCard
from datetime import datetime, timedelta
import json
import secrets
import string

file_path = 'data.json.bak'

def save(accounts, cards):
    data = {
        "accounts": [a.to_dict() for a in accounts.values()],
        "cards": [c.to_dict() for c in cards.values()],
    }
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except OSError as e:
        print(f"Could not save data: {e}")

def load():
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return None                      # first run, nothing saved yet
    except json.JSONDecodeError:
        print("Save file is corrupted. Starting fresh.\n")
        return None

    account_classes = {"CheckingAccount": CheckingAccount, "SavingsAccount": SavingsAccount}
    card_classes = {"DebitCard": DebitCard, "CreditCard": CreditCard}

    accounts = {}
    for entry in data["accounts"]:
        account = account_classes[entry["type"]].from_dict(entry)
        accounts[account.account_number] = account

    cards = {}
    for entry in data["cards"]:
        card = card_classes[entry["type"]].from_dict(entry, accounts)
        cards[card.card_number] = card

    return accounts, cards

def create_account(accounts, account_class, name=None):
    while True:
        id = ''.join(secrets.choice(string.digits) for i in range(9)) 
        if id not in accounts:
            break
    if name is None:
        name = input("Type in your name: ")
    while True:
        try:
            starting_balance = float(input("\nDeposit your starting balance: $"))
        except ValueError:
            print("Invalid starting balance. Please enter a valid number.")
        else:
            if starting_balance < 0:
                print("Invalid starting balance. Please enter a valid number.")
            else:
                break
    account = account_class(id, name, 0)
    if starting_balance > 0:
        account.deposit(starting_balance, description="Opening deposit")
    accounts[id] = account
    print(f"\nYour {account_class.__name__} number is {id}.")
    return account

def open_card(cards, card_class, account):
    while True:
        card_id = ''.join(secrets.choice(string.digits) for i in range(16))
        if card_id not in cards:
            break
    formatted_card = '-'.join(card_id[i:i+4] for i in range(0, len(card_id), 4)) 
    cvv = ''.join(secrets.choice(string.digits) for i in range(3))
    now = datetime.now()
    month = now.month + 1
    year = now.year + 5 + (1 if month > 12 else 0)
    month = 1 if month > 12 else month
    expiration_date = datetime(year, month, 1)
    if card_class == CreditCard:
        card = CreditCard(card_id, account.account_holder, expiration_date, cvv, 5000, account)
    else:
        card = DebitCard(card_id, account.account_holder, expiration_date, cvv, account)
    cards[card_id] = card
    print(f"Your {card_class.__name__} number is {formatted_card} and your CVV number is {cvv}. It expires in {(expiration_date - timedelta(days=1)).strftime('%m/%y')}")
    return card


loaded = load()
# Open the File
if loaded is None:
    accounts = {}
    cards = {}
    checking = create_account(accounts, CheckingAccount)
    debit = open_card(cards, DebitCard, checking)
    while True:
        create_savings = input('Would you like to open a Savings Account? (Yes/No) ').lower()
        if create_savings == 'yes':
            savings = create_account(accounts, SavingsAccount, name=checking.account_holder)
            break
        elif create_savings == 'no':
            break
        else:
            print("Invalid Choice. Please Choose Again.")
else:
    accounts, cards = loaded


def select_account(accounts, expected_class):
    user_input = input("Enter your Account #: ")
    acc = accounts.get(user_input)
    if acc is None:
        print("Invalid account number. Please try again.")
        return None
    if not isinstance(acc, expected_class):
        print(f"That is not a {expected_class.__name__}. Please try again.")
        return None
    return acc

# Choose the current account
current_account = None
on = True
while on:
    account_type = input("\nEnter account type (1 for Checking Account, 2 for Savings Account, or 3 to Create an Account. Type exit to quit.): ")
    if account_type == "1":
        acc = select_account(accounts, CheckingAccount)
        if acc is not None:
            if acc.isActive:
                current_account = acc
                on = False
            else:
                print("The selected account is inactive. Please contact the bank for assistance.")
    elif account_type == "2":
        acc = select_account(accounts, SavingsAccount)
        if acc is not None:
            if acc.isActive:
                current_account = acc
                on = False
            else:
                print("The selected account is inactive. Please contact the bank for assistance.")
    elif account_type == "3":
        create_account_type = input("Enter account type (1 for Checking Account, 2 for Savings Account. Type exit to quit): ")
        if create_account_type == "1":
            new_account = create_account(accounts, CheckingAccount)
            open_card(cards, DebitCard, new_account)
            save(accounts, cards)
        elif create_account_type == "2":
            create_account(accounts, SavingsAccount)
            save(accounts, cards)
        elif create_account_type == "exit":
            on = False
        else:
            print("Invalid account type. Please Try Again.")
    elif account_type == "exit":
        on = False
    else:
        print("Invalid Choice. Please Try Again.")

is_running = current_account is not None

while is_running: 
    print("\n========================================")
    print("   Banking Program Menu   ")
    print(f"   User: {current_account.account_holder}   ")
    print(f"   Account #: {current_account.account_number}   ")
    print(f"   Active: {current_account.isActive}   ")

    print("========================================")
    print("1. Show Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Apply Interest (Savings Account Only)")
    print("5. Switch Account")
    print("6. Transfer Funds")
    print("7. View Cards")
    print("8. Make a Payment")
    print("9. Show Credit Card Statement")
    print("10. Open A Credit Card")
    print("11. Show Transaction History")
    print("12. Exit")
    print("========================================")
    choice = input("\nEnter your choice: ")

    if choice == "1":
            print(current_account.show_balance())
    elif choice == "2":
        try:
            amount = float(input("\nEnter deposit amount: $"))
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
        else:
            try:
                current_account.deposit(amount)
                print(f"Deposited ${amount:.2f} successfully.")
                save(accounts, cards)
            except ValueError as e:
                print(f"Error: {e}")
    elif choice == "3":
        try:
            amount = float(input("\nEnter withdrawal amount: $"))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        else:
            try:
                current_account.withdraw(amount)
                print(f"Withdrew ${amount:.2f} successfully.")
                save(accounts, cards)
            except ValueError as e:
                print(f"Error: {e}")
    elif choice == "4":
        if isinstance(current_account, SavingsAccount):
            try:
                paid = current_account.add_interest()
                if paid == 0:
                    print("No Interest to be added")
                else:
                    print(f"\nInterest of ${paid:.2f} applied successfully.")
                save(accounts, cards)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            print("Interest can only be applied to Savings Accounts.")
    elif choice == "5":
        account_type = input("\nEnter account type (1 for Checking Account, 2 for Savings Account.): ")
        if account_type == "1":
            acc = select_account(accounts, CheckingAccount)
        elif account_type == "2":
            acc = select_account(accounts, SavingsAccount)
        else:
            acc = None
            print("Invalid account type. No changes made.")

        if acc is not None:
            if acc.isActive:
                current_account = acc
            else:
                print("The selected account is inactive. Please contact the bank for assistance.")
    elif choice == "6":
        try:
            amount = float(input("\nEnter transfer amount: $"))
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        else:
            target_account_number = input("Enter target account number: ")
            target = accounts.get(target_account_number)
            if target is None:
                print("Target account not found.")
            elif target is current_account:
                print("Cannot transfer to the same account.")
            elif target.isActive:
                try:
                    current_account.transfer(amount, target)
                    print(f"\nTransferred ${amount:.2f} successfully.\n")
                    save(accounts, cards)
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("The selected account is inactive. Please contact the bank for assistance.")
    elif choice == "7":
        found = False
        for card in cards.values():
            if card.account is current_account:
                print(card)
                found = True
        if not found:
            print("No cards linked to this account.")
    elif choice == "8":
        my_cards = [c for c in cards.values()
            if c.account is current_account and isinstance(c, CreditCard)]
                
        if not my_cards:
            print("No credit cards linked to this account.")
        else:
            for number, card in enumerate(my_cards, start=1):
                print(f"{number}. {card}")
            try:
                pick = int(input('\nEnter the number of the card you would like to pay off: '))
            except ValueError:
                print("Invalid input. Please enter a number.")
            else:
                if 1 <= pick <= len(my_cards):
                    card = my_cards[pick - 1]
                    try:
                        amount = float(input("Enter Credit Card Payment amount: $"))
                    except ValueError:
                        print("Invalid input. Please enter a valid number.")
                    else:
                        try:
                            card.pay_off(amount, current_account)
                            print(f"Paid ${amount:.2f} successfully.")
                            save(accounts, cards)
                        except ValueError as e:
                            print(f"Error: {e}")
                else:
                    print("That card number isn't in the list.")
    elif choice == "9":
        my_cards = [c for c in cards.values()
            if c.account is current_account and isinstance(c, CreditCard)]

        if not my_cards:
            print("No credit cards linked to this account.")
        else:
            for number, card in enumerate(my_cards, start=1):
                print(f"{number}. {card}")

            try:
                pick = int(input('\nEnter the number of the card you would like to view: '))
            except ValueError:
                print("Invalid input. Please enter a number.")
            else:
                if 1 <= pick <= len(my_cards):
                    print(my_cards[pick - 1].show_statement())
                else:
                    print("That card number isn't in the list.")
    elif choice == "10":
        while True:
            open_credit = input('\nWould you like to open a Credit Card? (Yes/No) ').lower()
            if open_credit == 'yes':
                credit = open_card(cards, CreditCard, current_account)
                save(accounts, cards)
                break
            elif open_credit == 'no':
                break
            else:
                print("Invalid Choice. Please Choose Again.")
    elif choice == "11":
        for t in current_account.transactions:
            print(t)
            
    elif choice == "12":
        is_running = False
    else:
        print("========================================")
        print("Invalid choice. Please try again.")
        print("========================================")
save(accounts, cards)
print("========================================")
print("Thank you, Have a nice day!")
print("========================================")


