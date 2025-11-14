from .errors import ValidationError
from datetime import datetime
from typing import Any
import re


class Field:
    def __init__(self, value):
        self.value = self.validate(value)

    def validate(self, value) -> Any:
        """Base validator: strip + non-empty. Subclasses may override."""
        value = self.base_validate(value)
        return value

    @staticmethod
    def base_validate(value):
        if not isinstance(value, str):
            raise ValidationError("Value must be a string")

        value = value.strip()
        if not value:
            raise ValidationError("Field cannot be empty")

        return value

    def update(self, new_value):
        self.value = self.validate(new_value)

    def __str__(self):
        return str(self.value)


# ---------------------------
# Specific Fields
# ---------------------------


class Name(Field):
    """Uses default base validation."""


class Phone(Field):
    def validate(self, value):
        number = self.base_validate(value)

        if len(number) != 10 or not number.isdigit():
            raise ValidationError("Phone must contain exactly 10 digits")

        return number


class Birthday(Field):
    DATE_PATTERN = re.compile(r"\d{2}\.\d{2}\.\d{4}$")

    def validate(self, value):
        if not isinstance(value, str):
            raise ValidationError("Birthday must be a string")

        birthday = value.strip()

        if not self.DATE_PATTERN.match(birthday):
            raise ValidationError(f"Invalid date format: {birthday}. Use DD.MM.YYYY")

        try:
            return datetime.strptime(birthday, "%d.%m.%Y")
        except ValueError:
            raise ValidationError(f"Invalid date: {birthday}")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Email(Field):
    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def validate(self, value):
        email = self.base_validate(value)

        if not self.EMAIL_PATTERN.match(email):
            raise ValidationError(f"Invalid email format: {email}")

        return email


class Address(Field):
    def validate(self, value):
        return self.base_validate(value)


class Title(Field):
    def validate(self, value):
        return self.base_validate(value)


class Content(Field):
    """Content may be empty, so override validation."""

    def validate(self, value):
        return value  # no validation


class Tags(Field):
    def validate(self, value):
        value = self.base_validate(value)
        return value
