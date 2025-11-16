import sys
import difflib
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

sys.path.append("src")

# перед здачею проєкту видалити 1–3 рядки та встановити пакет локально:
# pip install -e src/

from personal_assistant import (
    Command_Use,
    load_data,
    save_data,
    parse_input,
    add_contact,
    change_contact,
    delete_contact,
    show_phone,
    show_email,
    show_contact,
    show_all,
    add_address,
    add_email,
    change_email,
    delete_email,
    add_birthday,
    show_birthday,
    birthdays,
    add_note,
    find_note_by_title,
    delete_note,
    change_note,
    find_note_by_tag,
    show_all_notes,
    search_contacts,
    show_help,
)

command_list = [
    "hello",
    "exit",
    "close",
    "help",
    "add",
    "change",
    "delete",
    "phone",
    "email",
    "birthday",
    "contact",
    "all",
    "add-address",
    "add-email",
    "change-email",
    "delete-email",
    "add-birthday",
    "birthdays",
    "search",
    "add-note",
    "find-note-by-title",
    "delete-note",
    "change-note",
    "find-note-by-tag",
    "all-notes",
]

class AutoSuggestFromList(AutoSuggest):
    def __init__(self, options):
        self.options = sorted(options)

    def get_suggestion(self, buffer, document):
        text = document.text_before_cursor.strip()
        
        # Якщо текст порожній - нічого не підказуємо
        if not text:
            return None

        # Шукаємо першу команду, яка починається з введеного тексту
        for option in self.options:
            if option.startswith(text.lower()):
                # Повертаємо ту частину команди, яку користувач ще не ввів
                return Suggestion(option[len(text):])

        return None


def main():
    # завантаження даних контактів та нотаток
    book, notes = load_data()

    print("Welcome to the assistant bot!")

    session = PromptSession(auto_suggest=AutoSuggestFromList(command_list))

    while True:
        try:
            # читаю команду від користувача
            user_input = session.prompt("Enter a command: ")
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

                case "delete":
                    print(delete_contact(args, book))

                case "phone":
                    print(show_phone(args, book))

                case "email":
                    print(show_email(args, book))

                case "birthday":
                    print(show_birthday(args, book))

                case "contact":
                    print(show_contact(args, book))

                case "all":
                    print(show_all(book))

                case "add-address":
                    print(add_address(args, book))

                case "add-email":
                    print(add_email(args, book))

                case "change-email":
                    print(change_email(args, book))

                case "delete-email":
                    (delete_email(args, book))

                case "add-birthday":
                    print(add_birthday(args, book))

                case "birthdays":
                    print(birthdays(args, book))

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
                    # Шукаємо найбільш схожу команду
                    matches = difflib.get_close_matches(command, command_list, n=1, cutoff=0.6)
                    
                    if matches:
                        print(f"Invalid command. Did you mean '{matches[0]}'?")
                    else:
                        print("Invalid command. Type 'help' to see all commands.")

        except KeyboardInterrupt:
            # Дозволяє коректно вийти через Ctrl+C
            print("Good bye!")
            save_data(book, notes)
            break
        except ValueError:
            continue

if __name__ == "__main__":
    main()
