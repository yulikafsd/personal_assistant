import sys

sys.path.append("src")

# перед здачею проєкту видалити 1–3 рядки та встановити пакет локально:
# pip install -e src/

from enum import Enum

from personal_assistant import (
    AddressBook,
    Record,
    load_data,
    save_data,
    parse_input,
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    add_note,
    find_note_by_title,
    delete_note,
    change_note,
    find_note_by_tag,
    show_all_notes,
    add_address,        # команда для роботи з адресами
    search_contacts,    # команда пошуку (phone/email/birthday)
    show_help,          # команда виводу довідки
)


class Command_Use(Enum):
    ADD = "add [name] [phone]"
    CHANGE = "change [name] [old_phone] [new_phone]"
    PHONE = "phone [name]"
    ALL = "all"
    ADD_ADDRESS = "add-address [name] [address]"
    ADD_BIRTHDAY = "add-birthday [name] [birthday]"
    SHOW_BIRTHDAY = "show-birthday [name]"
    BIRTHDAYS = "birthdays"
    ADD_NOTE = "add-note"
    FIND_NOTE_BY_TITLE = "find-note-by-title"
    DELETE_NOTE = "delete-note"
    CHANGE_NOTE = "change-note"
    FIND_NOTE_BY_TAG = "find-note-by-tag"
    ALL_NOTES = "all-notes"
    SEARCH = "search [field] [value]"   # команда пошуку
    HELP = "help"                       # команда для виводу довідки
    HELLO = "hello"
    CLOSE = "close"
    EXIT = "exit"


def main():
    # завантаження даних контактів та нотаток
    book, notes = load_data()

    print("Welcome to the assistant bot!")

    while True:
        # читаю команду від користувача
        user_input = input("Enter a command: ")
        # розбираю команду та аргументи
        command, args = parse_input(user_input)

        if not command:
            continue

        match command:

            case "close" | "exit":
                print("Good bye!")
                save_data(book, notes)
                break

            case "hello":
                print("How can I help you?")

            case "help":
                # виведення довідки по доступним командам
                print(show_help())

            case "add":
                print(add_contact(args, book))

            case "change":
                print(change_contact(args, book))

            case "phone":
                print(show_phone(args, book))

            case "all":
                print(show_all(book))

            case "add-address":
                # додавання або оновлення адреси
                print(add_address(args, book))

            case "add-birthday":
                print(add_birthday(args, book))

            case "show-birthday":
                print(show_birthday(args, book))

            case "birthdays":
                print(birthdays(book))

            case "search":
                # пошук по телефону / email / даті народження
                print(search_contacts(args, book))

            case "add-note":
                print(add_note(notes))

            case "find-note-by-title":
                print(find_note_by_title(notes))

            case "delete-note":
                print(delete_note(notes))

            case "change-note":
                print(change_note(notes))

            case "find-note-by-tag":
                print(find_note_by_tag(notes))

            case "all-notes":
                print(show_all_notes(notes))

            case _:
                print("Invalid command. The following commands are available:")
                for cmd in Command_Use:
                    print(f" - {cmd.value}")


if __name__ == "__main__":
    main()



