from models.split import EqualSplit, ExactSplit, PercentSplit


def create_split(split_type: str):
    strategies = {
        "EQUAL": EqualSplit,
        "EXACT": ExactSplit,
        "PERCENT": PercentSplit,
    }

    split_class = strategies.get(split_type.upper())

    if split_class is None:
        raise ValueError(f"Unsupported split type: {split_type}")

    return split_class()
