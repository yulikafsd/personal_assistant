from .utils import input_error
from .addressbook import AddressBook
from .record import Record
from .notes import Notes
from typing import Any, Callable


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
            f"Contact {name_capitalized} already exists.\nAdd another phone number to the contact? Y/N: "
        )
        if user_input.lower() == "n":
            return "Nothing changed"
    return record.add_phone(phone)


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        user_input = input(
            f"Contact with name {name_capitalized} was not found.\nAdd a new contact? Y/N: "
        )
        if user_input.lower() == "y":
            return add_contact([name_capitalized, new_phone], book)
        else:
            return "Nothing changed"
    return record.edit_phone(old_phone, new_phone)


@input_error
def delete_contact(args, book: AddressBook):
    if not args:
        raise IndexError
    name = args[0].capitalize()
    record = book.find(name)
    if not record:
        return f"Contact with name {name} was not found."
    book.delete(name)
    return f"Contact {name} was deleted successfully."


# ----------------------- Хелпери для відображення -----------------------
def _show_generic(
    record: Any,
    field_name: str,
    display_func: Callable[[Any], str] = str,
    plural_name: str | None = None,
) -> str:
    """Універсальний хелпер для show_* полів.

    Args:
        record: Record об'єкт.
        field_name: назва атрибуту Record ('phones', 'emails', 'birthday', 'address').
        display_func: функція для перетворення значення в рядок.
        plural_name: як називати поле в рядку (для мн. числа, напр. 'phone(s)').
    """
    value = getattr(record, field_name)

    if not value:
        return f"{record.name.value} has no {plural_name or field_name} yet."

    if isinstance(value, list):
        return f"{record.name.value}'s {plural_name or field_name}: {', '.join(display_func(v) for v in value)}"

    return f"{record.name.value}'s {plural_name or field_name}: {display_func(value)}"


def _show_field(args, book, show_func):
    """Універсальна обгортка для show_* команд."""
    name = args[0].capitalize()
    record = book.find(name)
    if not record:
        return f"Contact with name {name} was not found."
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
        return f"Contact with name {name} was not found."

    fields = [
        ("Phones", lambda r: _show_generic(r, "phones", lambda p: p.value, "phone(s)")),
        ("Emails", lambda r: _show_generic(r, "emails", lambda e: e.value, "email(s)")),
        ("Birthday", lambda r: _show_generic(r, "birthday", lambda b: str(b))),
        ("Address", lambda r: _show_generic(r, "address", lambda a: a.value)),
    ]

    results = []
    for label, func in fields:
        info = func(record)
        # Пропускаємо поля, що повертають 'has no ...'
        if "has no" not in info:
            results.append(info)

    if not results:
        return f"{record.name.value} has no info yet."

    # Додаємо роздільники між полями
    return "---\n" + "\n".join(results) + "\n---"


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts were found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        return "You must provide name and address."

    name, *address_parts = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)

    if not record:
        return f"Contact with name {name_capitalized} was not found."

    address = " ".join(address_parts)
    return record.add_address(address)


@input_error
def add_email(args, book: AddressBook):
    name, email, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)

    if not record:
        user_input = input(
            f"Contact with name {name_capitalized} was not found.\nAdd a new contact? Y/N: "
        )
        if user_input.lower() == "y":
            record = Record(name_capitalized)
            book.add_record(record)
        else:
            return "Nothing changed"

    return record.add_email(email)


@input_error
def change_email(args, book: AddressBook):
    name, old_email, new_email, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)

    if not record:
        user_input = input(
            f"Contact with name {name_capitalized} was not found.\nAdd a new contact? Y/N: "
        )
        if user_input.lower() == "y":
            record = Record(name_capitalized)
            record.add_email(new_email)
            book.add_record(record)
            return f"Contact {name_capitalized} created with email {new_email}"
        else:
            return "Nothing changed"

    return record.edit_email(old_email, new_email)


@input_error
def delete_email(args, book: AddressBook):
    name, email, *_ = args
    name_capitalized = name.capitalize()

    record = book.find(name_capitalized)
    if not record:
        return f"Contact {name_capitalized} was not found."

    result = record.remove_email(email)
    return result


@input_error
def add_birthday(args, book: AddressBook):
    name, new_birthday, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        return f"Contact with name {name_capitalized} was not found."
    return record.add_birthday(new_birthday)


@input_error
def birthdays(args, book: AddressBook):
    if not book.data:
        return "No contacts were found."

    days_from_today = 7 if not args else int(args[0])
    upcoming_bds = book.get_upcoming_birthdays(days_from_today)
    if not upcoming_bds:
        return f"No birthdays in the next {days_from_today} days."
    return ", ".join(
        f"{user['name']}: {user['congratulation_date']}" for user in upcoming_bds
    )


@input_error
def add_note(notes: Notes) -> str:
    title = input("Enter note title: ")
    text = input("Enter note text: ")
    tags = input("Enter note tags (comma separated): ")
    try:
        notes.add_note(title, text, tags)
        return f"Note with title '{title}' added successfully."
    except ValueError as e:
        return str(e)


@input_error
def find_note_by_title(notes: Notes) -> str:
    title = input("Enter note title to find: ")
    note = notes.find_note_by_title(title)
    if note:
        return str(note)
    else:
        return f"Note with title '{title}' not found."


@input_error
def delete_note(notes: Notes) -> str:
    title = input("Enter note title to delete: ")
    result = notes.delete_note(title)
    return result


@input_error
def change_note(notes: Notes) -> str:
    title = input("Enter note title to edit: ")
    new_content = input("Enter new content: ")
    new_tags = input("Enter new tags (comma separated): ")
    result = notes.change_note(
        title, new_content if new_content else None, new_tags if new_tags else None
    )
    return result


@input_error
def find_note_by_tag(notes: Notes) -> str:
    tag = input("Enter tag to find note: ")
    matched_notes = notes.find_note_by_tag(tag)
    if matched_notes:
        return "\n\n".join(str(note) for note in matched_notes)
    else:
        return f"No notes found with tag '{tag}'."


@input_error
def show_all_notes(notes: Notes) -> str:
    return notes.show_all_notes()
