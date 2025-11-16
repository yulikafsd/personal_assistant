from typing import Any, Callable

from .utils import input_error
from .addressbook import AddressBook
from .record import Record
from .notes import Notes
from .colorize import Colorize


# ============================
# 📇 Контакти
# ============================
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)

    if not record:
        record = Record(name_capitalized)
        book.add_record(record)
    else:
        user_input = input(
            Colorize.warning(f"Contact {name_capitalized} already exists.\nAdd another phone number to the contact? Y/N: ")
        )
        if user_input.lower() == "n":
            return Colorize.info("Nothing changed")

    return record.add_phone(phone)


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)

    if not record:
        user_input = input(
            (Colorize.warning(f"Contact with name {name_capitalized} was not found.\nAdd a new contact? Y/N: "))
        )
        if user_input.lower() == "y":
            return add_contact([name_capitalized, new_phone], book)
        else:
            return Colorize.info("Nothing changed")

    return record.edit_phone(old_phone, new_phone)


@input_error
def delete_contact(args, book: AddressBook):
    if not args:
        raise IndexError
    name = args[0].capitalize()
    record = book.find(name)
    if not record:
        return Colorize.info(f"Contact with name {name} was not found.")
    book.delete(name)
    return Colorize.success(f"Contact {name} was deleted successfully.")


# ----------------------- Хелпери для відображення -----------------------
def _show_generic(
    record: Any,
    field_name: str,
    display_func: Callable[[Any], str] = str,
    plural_name: str | None = None,
) -> str:
    """Універсальний хелпер для show_* полів."""
    value = getattr(record, field_name)

    if not value:
        return Colorize.error(f"{record.name.value} has no {plural_name or field_name} yet.")

    if isinstance(value, list):
        return (
            f"{record.name.value}'s {plural_name or field_name}: "
            f"{', '.join(display_func(v) for v in value)}"
        )

    return f"{record.name.value}'s {plural_name or field_name}: {display_func(value)}"


def _show_field(args, book, show_func):
    """Універсальна обгортка для show_* команд."""
    name = args[0].capitalize()
    record = book.find(name)
    if not record:
        return Colorize.error(f"Contact with name {name} was not found.")
    return show_func(record)


# ----------------------- Show команди -----------------------
@input_error
def show_phone(args, book: AddressBook):
    return _show_field(
        args, book, lambda r: _show_generic(r, "phones", lambda p: p.value, "phone(s)")
    )


@input_error
def show_email(args, book: AddressBook):
    return _show_field(
        args, book, lambda r: _show_generic(r, "emails", lambda e: e.value, "email(s)")
    )


@input_error
def show_birthday(args, book: AddressBook):
    return _show_field(
        args, book, lambda r: _show_generic(r, "birthday", lambda b: str(b))
    )


@input_error
def show_address(args, book: AddressBook):
    return _show_field(
        args, book, lambda r: _show_generic(r, "address", lambda a: a.value)
    )


# ----------------------- Show contact (усі поля разом) -----------------------
@input_error
def show_contact(args, book: AddressBook):
    """Показує всі дані контакта в одному рядку, пропускаючи порожні поля."""
    name = args[0].capitalize()
    record = book.find(name)
    if not record:
        return Colorize.error(f"Contact with name {name} was not found.")

    fields = [
        ("Phones", lambda r: _show_generic(r, "phones", lambda p: p.value, "phone(s)")),
        ("Emails", lambda r: _show_generic(r, "emails", lambda e: e.value, "email(s)")),
        ("Birthday", lambda r: _show_generic(r, "birthday", lambda b: str(b))),
        ("Address", lambda r: _show_generic(r, "address", lambda a: a.value)),
    ]

    results = []
    for _, func in fields:
        info = func(record)
        # Пропускаємо поля, що повертають 'has no ...'
        if "has no" not in info:
            results.append(info)

    if not results:
        return Colorize.error(f"{record.name.value} has no info yet.")

    return "---\n" + "\n".join(results) + "\n---"


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return Colorize.error("No contacts were found.")
    return "\n".join(str(record) for record in book.data.values())


# ============================
# 🏠 Address
# ============================
@input_error
def add_address(args, book: AddressBook) -> str:
    """
    Додати/оновити адресу контакта.

    Виклик: add-address <name> <address...>
    """
    if len(args) < 2:
        return Colorize.warning("You must provide name and address.")

    name, *address_parts = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)

    if not record:
        return Colorize.error(f"Contact with name {name_capitalized} was not found.")

    address = " ".join(address_parts)
    return record.add_address(address)


# ============================
# ✉ Email-и
# ============================
@input_error
def add_email(args, book: AddressBook):
    name, email, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)

    if not record:
        user_input = input(
            Colorize.warning(f"Contact with name {name_capitalized} was not found.\nAdd a new contact? Y/N: ")
        )
        if user_input.lower() == "y":
            record = Record(name_capitalized)
            book.add_record(record)
        else:
            return Colorize.info("Nothing changed")

    return record.add_email(email)


@input_error
def change_email(args, book: AddressBook):
    name, old_email, new_email, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)

    if not record:
        user_input = input(
            Colorize.warning(f"Contact with name {name_capitalized} was not found.\nAdd a new contact? Y/N: ")
        )
        if user_input.lower() == "y":
            record = Record(name_capitalized)
            record.add_email(new_email)
            book.add_record(record)
            return Colorize.success(f"Contact {name_capitalized} created with email {new_email}")
        else:
            return Colorize.info("Nothing changed")

    return record.edit_email(old_email, new_email)


@input_error
def delete_email(args, book: AddressBook):
    name, email, *_ = args
    name_capitalized = name.capitalize()

    record = book.find(name_capitalized)
    if not record:
        return Colorize.error(f"Contact {name_capitalized} was not found.")

    result = record.remove_email(email)
    return result


# ============================
# 🎂 Дні народження
# ============================
@input_error
def add_birthday(args, book: AddressBook):
    name, new_birthday, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        return Colorize.error(f"Contact with name {name_capitalized} was not found.")
    return record.add_birthday(new_birthday)


@input_error
def birthdays(args, book: AddressBook):
    if not book.data:
        return Colorize.error("No contacts were found.")

    days_from_today = 7 if not args else int(args[0])
    upcoming_bds = book.get_upcoming_birthdays(days_from_today)
    if not upcoming_bds:
        return Colorize.error(f"No birthdays in the next {days_from_today} days.")
    return ", ".join(
        f"{user['name']}: {user['congratulation_date']}" for user in upcoming_bds
    )


# ============================
# 🔍 Пошук контактів (phone/email/birthday)
# ============================
@input_error
def search_contacts(args, book: AddressBook) -> str:
    """
    search <field> <value>
    field: phone / email / birthday
    birthday: у форматі DD.MM.YYYY
    """
    if len(args) < 2:
        return Colorize.warning("Вкажіть поле та значення для пошуку. Наприклад: search phone 1234567890")

    field, value, *_ = args
    field = field.lower().strip()
    value = value.strip()

    found_records = []

    for record in book.data.values():
        # Пошук за телефоном
        if field in ("phone", "tel"):
            for phone in record.phones:
                if phone.value == value:
                    found_records.append(str(record))
                    break

        # Пошук за email
        elif field in ("email", "mail"):
            email_obj = getattr(record, "emails", None)
            if email_obj:
                for e in email_obj:
                    if getattr(e, "value", None) == value:
                        found_records.append(str(record))
                        break

        # Пошук за днем народження (формат DD.MM.YYYY)
        elif field in ("birthday", "bday", "bd"):
            if record.birthday:
                bday_obj = getattr(record.birthday, "value", record.birthday)
                try:
                    bday_str = bday_obj.strftime("%d.%m.%Y")
                except AttributeError:
                    bday_str = str(record.birthday)
                if bday_str == value:
                    found_records.append(str(record))
        else:
            return Colorize.error("Невідоме поле для пошуку. Доступні: phone, email, birthday.")

    if not found_records:
        return Colorize.error("Контакти за заданими критеріями не знайдені.")

    return "Знайдені контакти:\n" + "\n".join(found_records)


# ============================
# 📝 Нотатки
# ============================
@input_error
def add_note(notes: Notes) -> str:
    title = input(Colorize.highlight("Enter note title: "))
    text = input(Colorize.highlight("Enter note text: "))
    tags = input(Colorize.highlight("Enter note tags (comma separated): "))
    try:
        notes.add_note(title, text, tags)
        return Colorize.success(f"Note with title '{title}' added successfully.")
    except ValueError as e:
        return Colorize.error(str(e))


@input_error
def find_note_by_title(notes: Notes) -> str:
    title = input(Colorize.highlight("Enter note title to find: "))
    note = notes.find_note_by_title(title)
    if note:
        return str(note)
    else:
        return Colorize.error(f"Note with title '{title}' not found.")


@input_error
def delete_note(notes: Notes) -> str:
    title = input(Colorize.highlight("Enter note title to delete: "))
    result = notes.delete_note(title)
    return result


@input_error
def change_note(notes: Notes) -> str:
    title = input(Colorize.highlight("Enter note title to edit: "))
    new_content = input(Colorize.highlight("Enter new content: "))
    new_tags = input(Colorize.highlight("Enter new tags (comma separated): "))
    result = notes.change_note(
        title, new_content if new_content else None, new_tags if new_tags else None
    )
    return result


@input_error
def find_note_by_tag(notes: Notes) -> str:
    tag = input(Colorize.highlight("Enter tag to find note: "))
    matched_notes = notes.find_note_by_tag(tag)
    divider = "-"*40
    if matched_notes:
        return "\n".join(f"{divider}\n{str(note)}\n{divider}" for note in matched_notes)
    else:
        return Colorize.error(f"No notes found with tag '{tag}'.")


@input_error
def show_all_notes(notes: Notes) -> str:
    return notes.show_all_notes()


# ============================
# ❓ HELP
# ============================
@input_error
def show_help(*args, **kwargs) -> str:
    """
    Повертає список доступних команд.
    """
    return (
        "Доступні команди:\n"
        "  add <name> <phone>                – додати контакт або телефон до існуючого\n"
        "  change <name> <old> <new>         – змінити номер телефону\n"
        "  delete <name>                     – видалити контакт\n"
        "  phone <name>                      – показати телефони контакту\n"
        "  email <name>                      – показати email-и контакту\n"
        "  birthday <name>                   – показати день народження контакту\n"
        "  contact <name>                    – показати всі дані контакту\n"
        "  all                               – показати всі контакти\n"
        "  add-address <name> <address>      – додати/оновити адресу контакта\n"
        "  add-email <name> <email>          – додати email контакту\n"
        "  change-email <name> <old> <new>   – змінити email контакту\n"
        "  delete-email <name> <email>       – видалити email контакту\n"
        "  add-birthday <name> <DD.MM.YYYY>  – додати день народження\n"
        "  birthdays [days]                  – дні народження впродовж N днів (7 за замовчуванням)\n"
        "  search <field> <value>            – пошук за phone / email / birthday\n"
        "  add-note                          – додати нотатку\n"
        "  change-note                       – змінити нотатку\n"
        "  delete-note                       – видалити нотатку\n"
        "  find-note-by-title                – знайти нотатку за заголовком\n"
        "  find-note-by-tag                  – знайти нотатку за тегом\n"
        "  all-notes                         – показати всі нотатки\n"
        "  help                              – показати цю довідку\n"
        "  exit | close                      – вийти з помічника\n"
    )
