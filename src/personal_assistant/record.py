from .fields import Name, Phone, Birthday, Address, Email
from .errors import ValidationError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None  # необов'язкове, тільки одне
        self.address: Address | None = None    # необов'язкова адреса
        self.emails: list[Email] = []          # список email-адрес

    # ---------------- Phones ----------------
    def add_phone(self, number: str):
        # перевіряємо, чи номер уже є в списку
        if any(phone_obj.value == number for phone_obj in self.phones):
            return f"{self.name.value}'s record already has the number: {number}"

        try:
            self.phones.append(Phone(number))
            return f"{self.name.value}'s record was updated with a new number: {number}"
        except ValidationError as e:
            return f"ERROR! No phone number was added! {e}"

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                try:
                    phone_obj.update(new_phone)
                    return f"{self.name.value}'s record was updated with a new number: {new_phone}"
                except ValidationError as e:
                    return f"ERROR! No phone number was added! {e}"

        return f"User {self.name.value} has no phone {old_phone}."

    # ---------------- Emails ----------------
    def add_email(self, email: str):
        """Додає новий email до списку, якщо його ще немає."""
        try:
            email_obj = Email(email)
        except ValidationError as e:
            return f"ERROR! No email was added! {e}"

        if any(e.value == email_obj.value for e in self.emails):
            return (
                f"{self.name.value}'s record already has the email: {email_obj.value}"
            )

        self.emails.append(email_obj)
        return f"{self.name.value}'s record was updated with a new email: {email_obj.value}"

    def edit_email(self, old_email: str, new_email: str):
        for email_obj in self.emails:
            if email_obj.value == old_email:
                try:
                    email_obj.update(new_email)
                    return (
                        f"{self.name.value}'s email was changed from "
                        f"{old_email} to {new_email}"
                    )
                except ValidationError as e:
                    return f"ERROR! No email was changed! {e}"

        return f"User {self.name.value} has no email {old_email}."

    def remove_email(self, email: str):
        for email_obj in self.emails:
            if email_obj.value == email:
                self.emails.remove(email_obj)
                remaining = (
                    ", ".join(e.value for e in self.emails) if self.emails else "None"
                )
                return (
                    f"Email '{email}' was removed from {self.name.value}'s record.\n"
                    f"Remaining emails: {remaining}"
                )

        return f"{self.name.value} has no email '{email}'."

    # ---------------- Birthday ----------------
    def add_birthday(self, birthday: str):
        if self.birthday is None:
            try:
                self.birthday = Birthday(birthday)
                return f"Birthday {birthday} is added to {self.name.value}'s record"
            except ValidationError as e:
                return f"ERROR! {e}"
        else:
            user_input = input(
                f"{self.name.value} already has a birthday.\nChange it? Y/N: "
            )
            if user_input.lower() == "n":
                return "Nothing changed"

            try:
                self.birthday = Birthday(birthday)
                return f"Birth date of {self.name.value} was changed to {birthday}"
            except ValidationError as e:
                return f"ERROR! {e}"

    # ============================
    # Методи для пошуку
    # ============================
    def matches_phone(self, phone: str) -> bool:
        return any(p.value == phone for p in self.phones)

    def matches_email(self, email: str) -> bool:
        return any(e.value == email for e in self.emails)

    def matches_birthday(self, date_str: str) -> bool:
        if not self.birthday:
            return False
        return str(self.birthday) == date_str  # Birthday.__str__ → "DD.MM.YYYY"

    # ============================
    # Address
    # ============================
    def add_address(self, address: str):
        try:
            self.address = Address(address)
            return f"Address '{address}' is added to {self.name.value}'s record"
        except ValidationError as e:
            return f"ERROR! {e}"

    # ---------------- String ----------------
    def __str__(self):
        phones_str = (
            f", phone(s): {'; '.join(p.value for p in self.phones)}"
            if self.phones
            else ""
        )
        emails_str = (
            f", email(s): {'; '.join(e.value for e in self.emails)}"
            if self.emails
            else ""
        )
        bday_str = f", birthday: {self.birthday}" if self.birthday else ""
        address_str = f", address: {self.address.value}" if self.address else ""
        return f"Contact name: {self.name.value}{phones_str}{emails_str}{bday_str}{address_str}"

