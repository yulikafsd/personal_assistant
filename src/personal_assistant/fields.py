from datetime import datetime
import re

from .errors import ValidationError


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
        """
        Приймає:
        - рядок у форматі DD.MM.YYYY
        - або datetime (на всякий випадок)
        """
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
    def __init__(self, value: str):
        if not value:
            raise ValidationError("Title cannot be empty")
        super().__init__(value)


class Content(Field):
    def __init__(self, value: str):
        super().__init__(value)


class Tags(Field):
    def __init__(self, value: str):
        value = value.strip()
        if not value:
            raise ValidationError("Tags cannot be empty")
        super().__init__(value)


class Address(Field):
    def __init__(self, value: str):
        clean = value.strip()
        if not clean:
            raise ValidationError("Address cannot be empty")
        super().__init__(clean)


