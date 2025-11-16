from collections import UserDict
from datetime import datetime, date

from .record import Record
from .errors import ValidationError
from .colorize import Colorize


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return Colorize.success(f"New record for {record.name.value} was added to the book:\n{self.data}")

    def find(self, name: str) -> Record | None:
        record = self.data.get(name)
        return record if record else None

    def delete(self, name: str) -> str:
        record = self.data.get(name)
        if not record:
            return Colorize.error(f"No contact {name} was found")
        del self.data[name]
        return Colorize.success(f"{name} deleted from contacts")

    def get_upcoming_birthdays(self, days_from_today: int) -> list[dict]:
        """
        Повертає список контактів, у яких день народження
        в проміжку [сьогодні; сьогодні + days_from_today].
        """
        today = datetime.today().date()
        current_year = today.year

        upcoming_birthdays: list[dict] = []

        for record in self.data.values():
            # якщо в записі немає дня народження — пропускаємо
            if not record.birthday:
                continue

            bd = record.birthday.value.date()

            # 29 лютого — окремий випадок
            try:
                next_bd = bd.replace(year=current_year)
            except ValueError:
                # Для дати 29.02 використовуємо 28.02
                next_bd = date(current_year, 2, 28)

            # Якщо день народження вже був цього року — переносимо на наступний
            if next_bd < today:
                try:
                    next_bd = bd.replace(year=current_year + 1)
                except ValueError:
                    next_bd = date(current_year + 1, 2, 28)

            delta_days = (next_bd - today).days

            if 0 <= delta_days <= days_from_today:
                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": next_bd.strftime("%d.%m.%Y"),
                    }
                )

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
