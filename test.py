from datetime import datetime, timedelta
from OOP import Account, CheckingAccount, Card, DebitCard, CreditCard, Transaction
import secrets
import string

id = ''.join(secrets.choice(string.digits) for i in range(9))  # generate a random 10-character ID

name = input("Type in your name: ")
starting_balance = float(input("Deposit your starting balance: $"))

CheckingAccount1 = Account(id, name, starting_balance)
card = CreditCard("1234-5678-9012-3477", "Yann", datetime(2026, 12, 31), "264", 5000, CheckingAccount1, 0)

print(CheckingAccount1.account_holder)