from decimal import Decimal, InvalidOperation
from models.users import User
from models.expense import Expense
from services.expense_manager import ExpenseManager
from services.split_factory import create_split


def format_amount(amount: Decimal) -> str:
    return format(amount.normalize(), "f")


def parse_money(token: str, label: str) -> Decimal:
    try:
        value = Decimal(token)
    except InvalidOperation:
        raise ValueError(f"{label} is not a number: {token}") from None

    if not value.is_finite():
        raise ValueError(f"{label} must be a finite number: {token}")

    if -value.as_tuple().exponent > 2:
        raise ValueError(f"{label} cannot have more than 2 decimal places: {token}")

    return value


def create_users(manager: ExpenseManager):
    users = [
        User("u1", "user1", "user1@example.com", "1111111111"),
        User("u2", "user2", "user2@example.com", "2222222222"),
        User("u3", "user3", "user3@example.com", "3333333333"),
        User("u4", "user4", "user4@example.com", "4444444444"),
    ]

    for u in users:
        manager.add_user(u)


def show_balances(manager: ExpenseManager, user_id: str = None):
    balance_manager = manager.balance_manager
    output = []

    if user_id is not None:
        manager.get_user(user_id)

        balances = balance_manager.get_user_balances(user_id)

        for other_id, amount in balances.items():
            if amount > 0:
                debtor = manager.get_user(user_id)
                creditor = manager.get_user(other_id)
                output.append(
                    f"{debtor.name} owes {creditor.name}: " f"{format_amount(amount)}"
                )
            elif amount < 0:
                debtor = manager.get_user(other_id)
                creditor = manager.get_user(user_id)
                output.append(
                    f"{debtor.name} owes {creditor.name}: " f"{format_amount(-amount)}"
                )

    else:
        for debtor_id in manager.users:
            for creditor_id in manager.users:
                if debtor_id == creditor_id:
                    continue

                amount = balance_manager.get_balance(debtor_id, creditor_id)

                if amount > 0:
                    debtor = manager.get_user(debtor_id)
                    creditor = manager.get_user(creditor_id)

                    output.append(
                        f"{debtor.name} owes {creditor.name}: "
                        f"{format_amount(amount)}"
                    )

    if output:
        for line in output:
            print(line)
    else:
        print("No balances")


def process_expense(manager: ExpenseManager, tokens: list[str]):
    if len(tokens) < 5:
        raise ValueError("Invalid EXPENSE command")

    payer_id = tokens[1]
    amount = parse_money(tokens[2], "Expense amount")

    try:
        num_users = int(tokens[3])
    except ValueError:
        raise ValueError(
            f"Number of participants is not an integer: {tokens[3]}"
        ) from None

    if num_users <= 0:
        raise ValueError("Number of participants must be positive")

    split_type_index = 4 + num_users

    if len(tokens) <= split_type_index:
        raise ValueError(
            f"Expected {num_users} participant ids followed by a split type"
        )

    participant_ids = tokens[4:split_type_index]
    split_type = tokens[split_type_index].upper()
    split_values = tokens[split_type_index + 1 :]

    if split_type == "EQUAL":
        if split_values:
            raise ValueError("EQUAL split does not accept share values")
        values = None
    else:
        if len(split_values) != num_users:
            raise ValueError(f"{split_type} split requires {num_users} values")

        if split_type == "EXACT":
            values = [parse_money(value, "Share value") for value in split_values]
        else:
            try:
                values = [Decimal(value) for value in split_values]
            except InvalidOperation:
                raise ValueError("Percentages must be numbers") from None

            if any(not value.is_finite() for value in values):
                raise ValueError("Percentages must be finite numbers")

    payer = manager.get_user(payer_id)
    participants = [
        manager.get_user(participant_id) for participant_id in participant_ids
    ]

    split = create_split(split_type)

    expense = Expense(
        expense_id=str(len(manager.expenses) + 1),
        payer=payer,
        total_amount=amount,
        participants=participants,
        split=split,
        split_values=values,
    )

    manager.add_expense(expense)


def process_command(manager: ExpenseManager, line: str):
    tokens = line.strip().split()

    if not tokens:
        return

    command = tokens[0].upper()

    if command == "SHOW":
        if len(tokens) == 1:
            show_balances(manager)
        elif len(tokens) == 2:
            show_balances(manager, tokens[1])
        else:
            raise ValueError("Usage: SHOW [user_id]")

    elif command == "EXPENSE":
        process_expense(manager, tokens)

    else:
        raise ValueError(f"Unknown command: {command}")


def main():
    manager = ExpenseManager()
    create_users(manager)

    while True:
        try:
            line = input()
        except EOFError:
            break

        if not line.strip():
            continue

        try:
            process_command(manager, line)
        except (ValueError, ArithmeticError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
