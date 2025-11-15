from datetime import datetime
from typing import Any
import re

from .errors import ValidationError


class Field:
    """Base class for all fields: stores value and provides minimal validation."""

    def __init__(self, value):
        self.value = self.validate(value)

    def validate(self, value) -> Any:
        """Base validator: check string type, strip spaces, ensure not empty."""
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
        """Updates field value with validation."""
        self.value = self.validate(new_value)

    def __str__(self) -> str:
        return str(self.value)


# ===============================
#       SPECIFIC FIELDS
# ===============================

class Name(Field):
    """Name uses only base validation."""
    pass


class Phone(Field):
    """
    Phone now supports normalization:
    - Removes spaces, parentheses, dashes, '+'
    - Validates 10 digits
    """

    NORMALIZE_PATTERN = re.compile(r"[^\d]")  # everything except digits

    def validate(self, value):
        raw = self.base_validate(value)

        # Remove all non-digit characters (normalization)
        number = re.sub(self.NORMALIZE_PATTERN, "", raw)

        if len(number) != 10:
            raise ValidationError(
                "Phone must contain exactly 10 digits after normalization"
            )

        return number


class Birthday(Field):
    """Stores birthday as datetime. Input must be DD.MM.YYYY."""

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

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Email(Field):
    """Simple email validator based on regex."""

    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def validate(self, value):
        email = self.base_validate(value)
        if not self.EMAIL_PATTERN.match(email):
            raise ValidationError(f"Invalid email format: {email}")
        return email


class Address(Field):
    """
    Minimal address validation:
    - Not empty
    - Minimal length: 5
    - Allowed characters: letters, digits, comma, dot, dash, space
    """

    ALLOWED_PATTERN = re.compile(r"^[A-Za-z0-9а-яА-ЯёЁіІїЇєЄ ,.\-\/]+$")

    def validate(self, value):
        address = self.base_validate(value)

        if len(address) < 5:
            raise ValidationError("Address is too short")

        if not self.ALLOWED_PATTERN.match(address):
            raise ValidationError("Address contains forbidden characters")

        return address


class Title(Field):
    """Title must be a non-empty string."""
    def validate(self, value):
        return self.base_validate(value)


class Content(Field):
    """Content may be empty."""
    def validate(self, value):
        return value


class Tags(Field):
    """Tags are comma-separated text, non-empty."""
    def validate(self, value):
        return self.base_validate(value)
