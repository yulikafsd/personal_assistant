from .record import Record
from collections import UserDict
from datetime import datetime, date, timedelta


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return f"New record for {record.name.value} was added to the book:\n{self.data}"

    def find(self, name):
        record = self.data.get(name)
        return record if record else None

    def delete(self, name):
        record = self.data.get(name)
        if not record:
            return f"No contact {name} was found"
        del self.data[name]
        return f"{name} deleted from contacts"

    def get_upcoming_birthdays(self, days_from_today) -> list:
        today = datetime.today().date()
        current_year = today.year

        upcoming_birthdays = []

        for record in self.data.values():

            if not record.birthday:
                continue

            bd = record.birthday.value.date()

            # 29 February error
            try:
                next_bd = bd.replace(year=current_year)
            except ValueError:
                # For 29.02 → 28.02
                next_bd = date(current_year, 2, 28)

            # If bd already was this year - change date to next year
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
