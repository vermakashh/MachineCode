from decimal import Decimal
from models.users import User
from models.expense import Expense
from services.balance_manager import BalanceManager


class ExpenseManager:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.balance_manager = BalanceManager()
        self.expenses: list[Expense] = []

    def add_user(self, new_user: User):
        if new_user.user_id in self.users:
            raise ValueError(f"user already exists: {new_user.user_id}")

        self.users[new_user.user_id] = new_user

    def get_user(self, user_id: str) -> User:
        if user_id not in self.users:
            raise ValueError(f"user does not exist: {user_id}")

        return self.users[user_id]

    def add_expense(self, expense: Expense):
        if expense.total_amount <= 0:
            raise ValueError("Expense amount must be positive")

        if expense.payer.user_id not in self.users:
            raise ValueError("Payer is not a registered user")

        if not expense.participants:
            raise ValueError("At least one participant is required")

        participant_ids = [person.user_id for person in expense.participants]

        if len(participant_ids) != len(set(participant_ids)):
            raise ValueError("Duplicate participants are not allowed")

        for user_id in participant_ids:
            if user_id not in self.users:
                raise ValueError(f"Unknown participant: {user_id}")

        shares = expense.calculate_split()

        if sum(shares) != expense.total_amount:
            raise ValueError("Shares must sum to the total expense")

        for participant, share in zip(expense.participants, shares):
            if participant.user_id == expense.payer.user_id:
                continue

            self.balance_manager.add_debt(
                participant.user_id,
                expense.payer.user_id,
                share,
            )

        self.expenses.append(expense)
