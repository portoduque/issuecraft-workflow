class Account:
    def __init__(self, balance):
        self.balance = balance

    def _debit(self, amount):
        self.balance -= amount

    def transfer_to(self, other, amount):
        self._debit(amount)
        other.balance += amount

    def withdraw(self, amount):
        self._debit(amount)
