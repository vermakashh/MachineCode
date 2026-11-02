from decimal import Decimal
from collections import defaultdict


class BalanceManager:
    def __init__(self):
        self.balances = defaultdict(lambda: defaultdict(Decimal))

    def add_debt(self, debtor_id: str, creditor_id: str, amount: Decimal):
        amount = Decimal(str(amount))

        if debtor_id == creditor_id or amount == 0:
            return

        if amount < 0:
            raise ValueError("Debt amount cannot be negative")

        reverse_balance = self.balances[creditor_id][debtor_id]

        if reverse_balance > 0:
            if reverse_balance >= amount:
                self.balances[creditor_id][debtor_id] -= amount
            else:
                remaining = amount - reverse_balance
                self.balances[creditor_id][debtor_id] = Decimal("0")
                self.balances[debtor_id][creditor_id] += remaining
        else:
            self.balances[debtor_id][creditor_id] += amount

    def get_balance(self, user1_id: str, user2_id: str) -> Decimal:
        return self.balances.get(user1_id, {}).get(user2_id, Decimal("0"))

    def get_user_balances(self, user_id: str) -> dict:
        result = {}

        for other_id, amount in self.balances.get(user_id, {}).items():
            if amount > 0:
                result[other_id] = amount

        for other_id, other_balances in self.balances.items():
            if other_id == user_id:
                continue

            amount = other_balances.get(user_id, Decimal("0"))

            if amount > 0:
                result[other_id] = -amount

        return result
