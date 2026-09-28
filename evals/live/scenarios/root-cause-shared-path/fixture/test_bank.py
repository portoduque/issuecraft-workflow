import unittest

from bank import Account


class AccountTests(unittest.TestCase):
    def test_valid_transfer(self):
        source = Account(100)
        target = Account(20)
        source.transfer_to(target, 30)
        self.assertEqual(70, source.balance)
        self.assertEqual(50, target.balance)

    def test_valid_withdrawal(self):
        account = Account(100)
        account.withdraw(25)
        self.assertEqual(75, account.balance)


if __name__ == "__main__":
    unittest.main()
