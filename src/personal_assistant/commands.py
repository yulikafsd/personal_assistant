from .utils import input_error
from .addressbook import AddressBook
from .record import Record
from .notes import Notes


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
            f"Contact {name_capitalized} already exists.\n"
            "Add another phone number to the contact? Y/N: "
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
            f"Contact with name {name_capitalized} was not found.\n"
            "Add a new contact? Y/N: "
        )
        if user_input.lower() == "y":
            return add_contact([name_capitalized, new_phone], book)
        else:
            return "Nothing changed"
    return record.edit_phone(old_phone, new_phone)


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        return f"Contact with name {name_capitalized} was not found"
    return (
        f"{name_capitalized}'s phones: {', '.join([p.value for p in record.phones])}"
        if record.phones
        else f"{name_capitalized} has no phone numbers yet."
    )


@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts were found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, new_birthday, *_ = args
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        return f"Contact with name {name_capitalized} was not found."
    return record.add_birthday(new_birthday)


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    name_capitalized = name.capitalize()
    record = book.find(name_capitalized)
    if not record:
        return f"Contact with name {name_capitalized} was not found."
    if not record.birthday:
        return f"Contact {name_capitalized} has no birthday yet"
    return f"{name_capitalized}'s birthday: {record.birthday}"


@input_error
def birthdays(book: AddressBook):
    if not book.data:
        return "No contacts were found."
    upcoming_bds = book.get_upcoming_birthdays()
    if not upcoming_bds:
        return "No birthdays in the next 7 days."
    return ", ".join(
        f"{user['name']}: {user['congratulation_date']}" for user in upcoming_bds
    )


# ============================
# 🔍 Пошук контактів
# ============================
@input_error
def search_contacts(args, book: AddressBook):
    """
    Пошук контактів за номером телефону, email або датою народження.

    Приклади:
        search phone 1234567890
        search email user@example.com
        search birthday 10.04.1995
    """
    if len(args) < 2:
        return (
            "Вкажіть поле та значення для пошуку.\n"
            "Приклад: search phone 1234567890"
        )

    field, value, *rest = args
    field = field.lower()
    value = value.strip()

    found_records = []

    for record in book.data.values():
        # Пошук за телефоном
        if field == "phone":
            if any(p.value == value for p in record.phones):
                found_records.append(str(record))

        # Пошук за email (якщо в запису вже реалізоване поле email)
        elif field == "email":
            email = getattr(record, "email", None)
            if email and getattr(email, "value", None) == value:
                found_records.append(str(record))

# Пошук за днем народження (формат DD.MM.YYYY)
        elif field in ("birthday", "bday", "bd"):
            if record.birthday:
                # birthday.value має бути datetime, але робимо обережно
                bday_obj = getattr(record.birthday, "value", record.birthday)
                try:
                    bday_str = bday_obj.strftime("%d.%m.%Y")
                except AttributeError:
                    bday_str = str(record.birthday)
                if bday_str == value:
                    found_records.append(str(record))
        else:
            return "Невідоме поле для пошуку. Доступні: phone, email, birthday."

    if not found_records:
        return "Контакти за заданими критеріями не знайдені."

    return "Знайдені контакти:\n" + "\n".join(found_records)


# ============================
# 📝 Нотатки
# ============================
@input_error
def add_note(notes: Notes) -> str:
    title = input("Enter note title: ")
    text = input("Enter note text: ")
    tags = input("Enter note tags (comma separated): ")
    notes.add_note(title, text, tags)
    return f"Note with title '{title}' added successfully."


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
    message = notes.delete_note(title)
    return message


@input_error
def change_note(notes: Notes) -> str:
    title = input("Enter note title to edit: ")
    new_content = input("Enter new content: ")
    new_tags = input("Enter new tags (comma separated): ")
    message = notes.change_note(
        title,
        new_content if new_content else None,
        new_tags if new_tags else None,
    )
    return message


@input_error
def find_note_by_tag(notes: Notes) -> str:
    tag = input("Enter tag to find note: ")
    matched_notes = notes.find_note_by_tag(tag)
    if matched_notes:
        return "\n".join(str(note) for note in matched_notes)
    else:
        return f"No notes found with tag '{tag}'."


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
        "  phone <name>                      – показати телефони контакту\n"
        "  all                               – показати всі контакти\n"
        "  add-birthday <name> <DD.MM.YYYY>  – додати день народження\n"
        "  show-birthday <name>              – показати день народження\n"
        "  birthdays                         – дні народження впродовж 7 днів\n"
        "  search <field> <value>            – пошук за phone / email / birthday\n"
        "  add-note                          – додати нотатку\n"
        "  change-note                       – змінити нотатку\n"
        "  delete-note                       – видалити нотатку\n"
        "  find-note-title                   – знайти нотатку за заголовком\n"
        "  find-note-tag                     – знайти нотатку за тегом\n"
        "  show-notes                        – показати всі нотатки\n"
        "  help                              – показати цю довідку\n"
        "  exit | close | good bye           – вийти з помічника\n"
    )