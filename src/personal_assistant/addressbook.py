from collections import UserDict
from datetime import datetime, timedelta

from .record import Record
from .errors import ValidationError


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return f"New record for {record.name.value} was added to the book:\n{self.data}"

    def find(self, name: str) -> Record | None:
        record = self.data.get(name)
        return record if record else None

    def delete(self, name: str) -> str:
        record = self.data.get(name)
        if not record:
            return f"No contact {name} was found"
        del self.data[name]
        return f"{name} deleted from contacts"

    def get_upcoming_birthdays(self) -> list[dict]:
        current_date = datetime.today().date()
        upcoming_birthdays: list[dict] = []

        for record in self.data.values():
            if record.birthday:
                contact_bd = record.birthday.value.date()
                current_year = current_date.year
                is_coming = contact_bd.replace(year=current_year) >= current_date
                congratulation_year = (
                    current_year if is_coming else current_date.year + 1
                )
                congratulation_date = contact_bd.replace(year=congratulation_year)
                is_next_week = 0 < (congratulation_date - current_date).days <= 7

                if is_next_week:
                    bd_weekday = congratulation_date.weekday()
                    if bd_weekday == 5:  # субота
                        congratulation_date += timedelta(days=2)
                    if bd_weekday == 6:  # неділя
                        congratulation_date += timedelta(days=1)

                    congrat_date_string = congratulation_date.strftime("%d.%m.%Y")
                    coming_bd = {
                        "name": record.name.value,
                        "congratulation_date": congrat_date_string,
                    }
                    upcoming_birthdays.append(coming_bd)

        return upcoming_birthdays

    # ===============================
    # 🔍 Пошук для твого завдання
    # ===============================

    def search_by_phone(self, phone: str) -> list[Record]:
        """Пошук контактів за точним номером телефону."""
        return [rec for rec in self.data.values() if rec.matches_phone(phone)]

    def search_by_email(self, email: str) -> list[Record]:
        """Пошук контактів за точним email."""
        return [rec for rec in self.data.values() if rec.matches_email(email)]

    def search_by_birthday(self, date_str: str) -> list[Record]:
        """Пошук контактів за точною датою народження (DD.MM.YYYY)."""
        result: list[Record] = []
        for rec in self.data.values():
            try:
                if rec.matches_birthday(date_str):
                    result.append(rec)
            except ValidationError:
                # якщо користувач ввів неправильну дату в пошуку — просто пропускаємо
                continue
        return result
