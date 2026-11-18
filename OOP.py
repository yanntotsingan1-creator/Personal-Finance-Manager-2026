# Personal Finance Management System

from datetime import datetime, timedelta
from enum import Enum
import math

class TransactionType(Enum):
    DEPOSIT = "Deposit"
    WITHDRAW = "Withdraw"
    TRANSFER = "Transfer"
    INTEREST = "Interest"
    CREDIT_CARD_INTEREST = "Credit Card Interest"
    CARD_CHARGE = "Card charge"
    CARD_PAYMENT = "Card payment"

class Account: 
    def __init__(self, account_number, account_holder, balance, isActive=True):
        self.transactions = []
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.isActive = isActive
    def show_balance(self):
        return(f"\nYour balance is: ${self.balance:.2f}")
    def deposit(self, amount, transaction_type=TransactionType.DEPOSIT, description=""):
            if not self.isActive:
                raise ValueError("Account is inactive.")
            if not math.isfinite(amount):
                raise ValueError("Amount must be a finite number")
            elif amount > 0:
                self.balance += amount
                self.transactions.append(Transaction(amount, transaction_type, description))
            else:
                raise ValueError("Deposit amount must be greater than zero.")
            return amount
    def withdraw(self, amount, transaction_type=TransactionType.WITHDRAW, description=""):
        if not self.isActive:
            raise ValueError("Account is inactive.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be greater than zero.")
        elif amount > self.balance:
            raise ValueError("Insufficient funds.")
        elif not math.isfinite(amount):
            raise ValueError("Amount must be a finite number")
        else:
            self.balance -= amount
            self.transactions.append(Transaction(amount, transaction_type, description))
        return amount
    def transfer(self, amount, target_account, transaction_type=TransactionType.TRANSFER):
        self.withdraw(amount, transaction_type, description=f"Transfer to ************{target_account.account_number[-4:]}")
        try:
            target_account.deposit(amount, transaction_type, description=f"Transfer from ************{self.account_number[-4:]}")
        except ValueError as e:
            self.deposit(amount, transaction_type=TransactionType.TRANSFER, description=f"Failed Transfer to ************{target_account.account_number[-4:]}")
            raise ValueError(f"Error transferring funds to ************{target_account.account_number[-4:]}: {e}") from e
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "balance": self.balance,
            "isActive": self.isActive,
            "transactions": [t.to_dict() for t in self.transactions]
        }
    @classmethod
    def from_dict(cls, data):
        account = cls(
            data["account_number"],
            data["account_holder"],
            data["balance"],
            isActive=data["isActive"],
        )
        account.transactions = [Transaction.from_dict(t) for t in data["transactions"]]
        return account
    

class CheckingAccount(Account): 
    def __init__(self, account_number, account_holder,  balance, isActive=True):
        super().__init__(account_number, account_holder, balance, isActive)
class SavingsAccount(Account):
    def __init__(self, account_number, account_holder, balance, interest_rate=0.03, last_interest_date=None, isActive=True):
        super().__init__(account_number, account_holder, balance, isActive)
        self.interest_rate = interest_rate
        if last_interest_date is None:
            last_interest_date = datetime.now()
        self.last_interest_date = last_interest_date

    def add_interest(self):
        if not self.isActive:
            raise ValueError("This Account is inactive.")

        now = datetime.now()
        elapsed_time = now - self.last_interest_date
        if elapsed_time.days < 30:
            raise ValueError("Interest can only be added once a month.")
        interest = round(self.balance * self.interest_rate / 12, 2)
        if interest == 0:
            return 0
            return("No interest to be added")
            
        self.last_interest_date = now
        self.balance += interest
        self.transactions.append(Transaction(interest, TransactionType.INTEREST))
        return interest
    def to_dict(self):
        data = super().to_dict()
        data["interest_rate"] = self.interest_rate
        data["last_interest_date"] = self.last_interest_date.isoformat()
        return data
    @classmethod
    def from_dict(cls, data):
        account = cls(
        data["account_number"],
        data["account_holder"],
        data["balance"],
        interest_rate=data["interest_rate"],
        last_interest_date=datetime.fromisoformat(data["last_interest_date"]),
        isActive=data["isActive"],
        )
        account.transactions = [Transaction.from_dict(t) for t in data["transactions"]]
        return account

class Card():
    def __init__(self, card_number, card_holder, expiration_date, cvv, account):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.account = account
    @property
    def is_expired(self):
        return datetime.now() >= self.expiration_date
    def __str__(self):
        status = "EXPIRED" if self.is_expired else "Active"
        return (f"{self.__class__.__name__}: ****-****-****-{self.card_number[-4:]} "
            f"| Expires {(self.expiration_date - timedelta(days=1)).strftime('%m/%y')} | {status}")
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "card_number": self.card_number,
            "card_holder": self.card_holder,
            "expiration_date": self.expiration_date.isoformat(),  # Converts datetime to string
            "cvv": self.cvv,
            "account": self.account.account_number  # Store ID reference
        }
    @classmethod
    def from_dict(cls, data, accounts):
        return cls(
            data["card_number"],
            data["card_holder"],
            datetime.fromisoformat(data["expiration_date"]),
            data["cvv"],
            accounts[data["account"]],
        )

class DebitCard(Card):
    def __init__(self, card_number, card_holder, expiration_date, cvv, account):
        super().__init__(card_number, card_holder, expiration_date, cvv, account)
    def pay(self, amount, transaction_type=TransactionType.CARD_PAYMENT):
        if self.is_expired:
            raise ValueError("Card has expired.")
        if amount <= 0:
            raise ValueError("Amount must be more than 0")
        else:
            self.account.withdraw(amount, transaction_type, description=f"****-****-****-{self.card_number[-4:]}")

class CreditCard(Card):
    def __init__(self, card_number, card_holder, expiration_date, cvv, credit_limit, account, balance_owed=0, card_interest_rate=0.22, last_interest_date=None):
        super().__init__(card_number, card_holder, expiration_date, cvv, account)
        self.credit_limit = credit_limit
        self.balance_owed = balance_owed
        self.account = account
        self.card_interest_rate = card_interest_rate
        if last_interest_date is None:
            last_interest_date = datetime.now()
        self.last_interest_date = last_interest_date
        self.transactions = []
    def __str__(self):
        return (super().__str__() +
                f" | Owed ${self.balance_owed:.2f} | Available ${self.credit_limit - self.balance_owed:.2f}")
    @property
    def maxed_out(self):
        return self.balance_owed >= self.credit_limit
    def charge(self, amount, transaction_type=TransactionType.CARD_CHARGE):
        if self.is_expired:
            raise ValueError("Card has expired.")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not math.isfinite(amount):
            raise ValueError("Amount must be a finite number")
        if self.maxed_out:
            raise ValueError ("Card is maxed out")
        if self.balance_owed + amount > self.credit_limit:
            raise ValueError(f"Charge denied. This charge would exceed your credit limit of ${self.credit_limit:.2f}. Current balance owed: ${self.balance_owed:.2f}")
        else:
            self.balance_owed += amount
            self.transactions.append(Transaction(amount, transaction_type, description=f"Credit Card (****-****-****-{self.card_number[-4:]})"))
    def pay_off(self, amount, source_account, transaction_type=TransactionType.CARD_PAYMENT):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if not math.isfinite(amount):
            raise ValueError("Amount must be a finite number")
        if amount > self.balance_owed:
            raise ValueError("This payment exceeds amount owed")
        else:
            source_account.withdraw(amount, transaction_type, description=f"Credit Card Payment")
            self.balance_owed -= amount
            self.transactions.append(Transaction(amount, transaction_type, description=f"Credit Card Payment"))
    def apply_interest(self, transaction_type=TransactionType.CREDIT_CARD_INTEREST):
        if self.is_expired:
            raise ValueError("This Card is Expired.")
        if not self.account.isActive:
            raise ValueError("The linked account is inactive.")
        now = datetime.now()
        elapsed_time = now - self.last_interest_date
        if elapsed_time.days < 30:
            raise ValueError("Interest can only be added once a month.")
        interest = round(self.balance_owed * self.card_interest_rate / 12, 2)
        if interest == 0:
            return 0
        self.last_interest_date = now
        self.balance_owed += interest
        self.transactions.append(Transaction(interest, TransactionType.CREDIT_CARD_INTEREST,
                    description=f"****-****-****-{self.card_number[-4:]}")
    )
        return interest
                
    def show_statement(self):  
        lines = [
            f"Credit limit: ${self.credit_limit:.2f}",
            f"You owe: ${self.balance_owed:.2f}",
            f"Available credit: ${self.credit_limit - self.balance_owed:.2f}",
        ]
        return ("\n".join(lines))
    def to_dict(self):
        data = super().to_dict()
        data["credit_limit"] = self.credit_limit
        data["account"] = self.account.account_number
        data["balance_owed"] = self.balance_owed
        data["card_interest_rate"] = self.card_interest_rate 
        data["last_interest_date"] = self.last_interest_date.isoformat() 
        data["transactions"] = [t.to_dict() for t in self.transactions]
        return data
    @classmethod
    def from_dict(cls, data, accounts):
        card = cls(
            data["card_number"],
            data["card_holder"],
            datetime.fromisoformat(data["expiration_date"]),
            data["cvv"],
            data["credit_limit"],
            accounts[data["account"]],
            balance_owed=data["balance_owed"],
            card_interest_rate=data["card_interest_rate"],
            last_interest_date=datetime.fromisoformat(data["last_interest_date"]),
        )
        card.transactions = [Transaction.from_dict(t) for t in data["transactions"]]
        return card

class Transaction:
    def __init__(self, amount, transaction_type, description=""):
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.date =datetime.now()
    def __str__(self):
        text = f"{self.transaction_type.value} of ${self.amount:.2f}"
        if self.description:
            text += f" ({self.description})"
        return text + f" on {self.date.strftime('%Y-%m-%d %H:%M')}"
    def __repr__(self):
        return f"Transaction({self.amount!r}, {self.transaction_type!r}, {self.description!r})"
    def to_dict(self):
            return {
                "amount": self.amount,
                "transaction_type": self.transaction_type.name,
                "description": self.description,
                "date": self.date.isoformat()
            }
    @classmethod
    def from_dict(cls, data):
        t = cls(data["amount"], TransactionType[data["transaction_type"]], data["description"])
        t.date = datetime.fromisoformat(data["date"])
        return t
