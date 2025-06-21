from banking import *

s1 = SavingsAccount("Shivam", 1000, 0.05)
c1 = CheckingAccount("Ram", 500, 100)
b1 = BankAccount("Shyam", 300)

s1.deposit(200)
s1.withdraw(50)
c1.withdraw(550)
s1.apply_interest()

merged = s1 + c1

cust = Customer("Dhiraj")
cust.add_account(s1)
cust.add_account(c1)
cust.add_account(b1)
cust.add_account(merged)

cust.transfer(s1, c1, 100)

print_account_summary(s1)
print_account_summary(c1)

class Wallet:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

w = Wallet("Eve", 150)
print_account_summary(w)

for a in cust.accounts:
    print(a)
    print(repr(a))

print("Total balance of", cust.name, "is", cust.total_balance())
