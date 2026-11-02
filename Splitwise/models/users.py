class User:
    def __init__(self, user_id, name, email, mobile):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.mobile = mobile

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"User({self.user_id!r}, {self.name!r})"
