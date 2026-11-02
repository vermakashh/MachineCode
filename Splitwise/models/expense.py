from decimal import Decimal
from models.users import User
from models.split import Split


class Expense:
    def __init__(
        self,
        expense_id: str,
        payer: User,
        total_amount: Decimal,
        participants: list[User],
        split: Split,
        split_values: list[Decimal] = None,
    ):
        self.expense_id = expense_id
        self.payer = payer
        self.total_amount = Decimal(str(total_amount))
        self.participants = participants
        self.split = split
        self.split_values = split_values

    def calculate_split(self) -> list[Decimal]:
        return self.split.calculate_split(
            self.total_amount, self.participants, self.split_values
        )
