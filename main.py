import sys

sys.path.append("src")

# перед здачею проєкту видалити 1-3 строки та встановлюти пакет локально командою:
# pip install -e src/

from personal_assistant import AddressBook, Record
from enum import Enum
from personal_assistant import (
    load_data,
    save_data,
    parse_input,
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_address,
    add_email,
    change_email,
    show_email,
    add_birthday,
    show_birthday,
    birthdays,
    add_note,
    find_note_by_title,
    delete_note,
    change_note,
    find_note_by_tag,
    show_all_notes,
)


class Command_Use(Enum):
    ADD = "add [name] [phone]"
    CHANGE = "change [name] [old_phone] [new_phone]"
    PHONE = "phone [name]"
    ALL = "all"
    ADD_ADDRESS = "add-address [name] [address]"

    # ---------------- Emails ----------------
    ADD_EMAIL = "add-email [name] [email]"
    CHANGE_EMAIL = "change-email [name] [old_email] [new_email]"
    SHOW_EMAIL = "show-email [name]"

    # ---------------- Birthdays ----------------
    ADD_BIRTHDAY = "add-birthday [name] [birthday]"
    SHOW_BIRTHDAY = "show-birthday [name]"
    BIRTHDAYS = "birthdays"

    # ---------------- Notes ----------------
    ADD_NOTE = "add-note"
    FIND_NOTE_BY_TITLE = "find-note-by-title"
    DELETE_NOTE = "delete-note"
    CHANGE_NOTE = "change-note"
    FIND_NOTE_BY_TAG = "find-note-by-tag"
    ALL_NOTES = "all-notes"

    # ---------------- General ----------------
    HELLO = "hello"
    CLOSE = "close"
    EXIT = "exit"


def main():
    book, notes = load_data()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if not command:
            continue

        match command:
            case "close" | "exit":
                print("Good bye!")
                save_data(book, notes)
                break

            case "hello":
                print("How can I help you?")

            case "add":
                print(add_contact(args, book))

            case "change":
                print(change_contact(args, book))

            case "phone":
                print(show_phone(args, book))

            case "all":
                print(show_all(book))

            case "add-address":
                print(add_address(args, book))

            case "add-email":
                print(add_email(args, book))

            case "change-email":
                print(change_email(args, book))

            case "show-email":
                print(show_email(args, book))

            case "add-birthday":
                print(add_birthday(args, book))

            case "show-birthday":
                print(show_birthday(args, book))

            case "birthdays":
                print(birthdays(book))

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
