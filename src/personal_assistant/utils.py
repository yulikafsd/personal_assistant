from .command_use import Command_Use  # твій Enum
from .errors import ValidationError


def input_error(func):
    usage_messages = {
        # General
        "HELLO": f"Usage: {Command_Use.HELLO.value}",
        "CLOSE": f"Usage: {Command_Use.CLOSE.value}",
        "EXIT": f"Usage: {Command_Use.EXIT.value}",
        # Phone
        "add_contact": f"Usage: {Command_Use.ADD.value}",
        "change_contact": f"Usage: {Command_Use.CHANGE.value}",
        "delete_contact": f"Usage: {Command_Use.DELETE.value}",
        "show_phone": f"Usage: {Command_Use.PHONE.value}",
        # Emails
        "add_email": f"Usage: {Command_Use.ADD_EMAIL.value}",
        "change_email": f"Usage: {Command_Use.CHANGE_EMAIL.value}",
        "delete_email": f"Usage: {Command_Use.DELETE_EMAIL.value}",
        "show_email": f"Usage: {Command_Use.EMAIL.value}",
        # Birthdays
        "add_birthday": f"Usage: {Command_Use.ADD_BIRTHDAY.value}",
        "birthdays": f"Usage: {Command_Use.BIRTHDAYS.value}",
        "show_birthday": f"Usage: {Command_Use.BIRTHDAY.value}",
        # Address
        "add_address": f"Usage: {Command_Use.ADD_ADDRESS.value}",
        # Show Contact
        "show_contact": f"Usage: {Command_Use.CONTACT.value}",
        "show_all": f"Usage: {Command_Use.ALL.value}",
        # Notes
        "add_note": f"Usage: {Command_Use.ADD_NOTE.value}",
        "find_note_by_title": f"Usage: {Command_Use.FIND_NOTE_BY_TITLE.value}",
        "delete_note": f"Usage: {Command_Use.DELETE_NOTE.value}",
        "change_note": f"Usage: {Command_Use.CHANGE_NOTE.value}",
        "find_note_by_tag": f"Usage: {Command_Use.FIND_NOTE_BY_TAG.value}",
        "show_all_notes": f"Usage: {Command_Use.ALL_NOTES.value}",
    }

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValidationError as e:
            return f"Validation Error: {e.message}"

        except IndexError:
            return usage_messages.get(func.__name__, "Error: missing arguments")

        except ValueError:
            return usage_messages.get(func.__name__, "Error: invalid value")

        except Exception as e:
            return f"Unexpected Error: {str(e)}"

    return inner
