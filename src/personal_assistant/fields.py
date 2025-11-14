from .errors import ValidationError
from datetime import datetime
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)


class Phone(Field):
    def __init__(self, number: str):
        super().__init__(self.validate_number(number))

    def validate_number(self, number: str) -> str:
        number = number.strip()
        if len(number) == 10 and number.isdigit():
            return number
        raise ValidationError(
            "Phone must contain 10 digits and consist of digits only"
        )

    def update(self, new_number: str) -> None:
        self.value = self.validate_number(new_number)


class Birthday(Field):
    def __init__(self, birthday):
        # рядок виду "10.04.1995"
        if isinstance(birthday, str) and re.match(r"\d{2}\.\d{2}\.\d{4}$", birthday):
            dt = datetime.strptime(birthday, "%d.%m.%Y")
            super().__init__(dt)
        # дозволимо одразу datetime — раптом хтось створює так
        elif isinstance(birthday, datetime):
            super().__init__(birthday)
        else:
            raise ValidationError(
                f"Invalid date format of {birthday}. Use DD.MM.YYYY"
            )

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Email(Field):
    def __init__(self, value: str):
        value = value.strip()
        # дуже проста валідація email
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, value):
            raise ValidationError(f"Invalid email format: {value}")
        super().__init__(value)


class Title(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value:
            raise ValidationError("Title cannot be empty")


class Content(Field):
    def __init__(self, value):
        super().__init__(value)


class Tags(Field):
    def __init__(self, value):
        super().__init__(value)
        if not value:
            raise ValidationError("Tags cannot be empty")