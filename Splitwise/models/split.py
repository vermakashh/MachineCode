from abc import ABC, abstractmethod
from decimal import Decimal


class Split(ABC):
    @abstractmethod
    def calculate_split(
        self, total: Decimal, participants: list, values: list = None
    ) -> list[Decimal]:
        pass


class EqualSplit(Split):
    def calculate_split(
        self, total: Decimal, participants: list, values: list = None
    ) -> list[Decimal]:
        if not participants:
            raise ValueError("Atleast one participant is required.")

        if total == 0:
            raise ValueError("Total amount cannot be zero.")

        total = Decimal(str(total))
        total_amt = int(total * 100)

        base_amt = total_amt // len(participants)
        remainder = total_amt % len(participants)

        shares = []

        for i in range(len(participants)):
            amt = base_amt + (1 if i < remainder else 0)
            shares.append(Decimal(amt) / Decimal(100))

        return shares


class ExactSplit(Split):
    def calculate_split(
        self, total: Decimal, participants: list, values: list
    ) -> list[Decimal]:
        if not participants:
            raise ValueError("Atleast one participant is required.")

        if not values or len(values) != len(participants):
            raise ValueError("Values must be provided for each participant.")

        shares = [Decimal(str(value)) for value in values]

        if any(share < 0 for share in shares):
            raise ValueError("Values cannot be negative.")

        if sum(shares) != total:
            raise ValueError("Sum of values must be equal to total amount.")

        return shares


class PercentSplit(Split):
    def calculate_split(
        self, total: Decimal, participants: list, values: list
    ) -> list[Decimal]:
        if not participants:
            raise ValueError("Atleast one participant is required.")

        if not values or len(values) != len(participants):
            raise ValueError("Values must be provided for each participant.")

        percentages = [Decimal(str(value)) for value in values]

        if any(value < 0 or value > 100 for value in percentages):
            raise ValueError("Percentages must be between 0 and 100")

        if sum(percentages) != Decimal("100"):
            raise ValueError("Percentages must sum to 100")

        total = Decimal(str(total))
        total_amt = int(total * 100)

        exact = [
            Decimal(total_amt) * percentage / Decimal("100")
            for percentage in percentages
        ]
        cents = [int(value) for value in exact]
        leftover = total_amt - sum(cents)

        order = sorted(
            range(len(exact)),
            key=lambda i: (exact[i] - cents[i], -i),
            reverse=True,
        )

        for i in order[:leftover]:
            cents[i] += 1

        return [Decimal(amt) / Decimal(100) for amt in cents]
