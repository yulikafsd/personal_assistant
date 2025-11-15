from enum import Enum


class Command_Use(Enum):

    # ---------------- General ----------------
    HELLO = "hello"
    CLOSE = "close"
    EXIT = "exit"

    # ---------------- Phone ----------------
    ADD = "add [name] [phone]"
    CHANGE = "change [name] [old_phone] [new_phone]"
    DELETE = "delete [name]"

    # ---------------- Emails ----------------
    ADD_EMAIL = "add-email [name] [email]"
    CHANGE_EMAIL = "change-email [name] [old_email] [new_email]"
    DELETE_EMAIL = "delete-email [name] [email]"

    # ---------------- Birthdays ----------------
    ADD_BIRTHDAY = "add-birthday [name] [birthday]"
    BIRTHDAYS = "birthdays( [days_from_today])"

    # ---------------- Address ----------------
    ADD_ADDRESS = "add-address [name] [address]"

    # ---------------- Show Contact's Info ----------------
    PHONE = "phone [name]"
    BIRTHDAY = "birthday [name]"
    EMAIL = "email [name]"
    CONTACT = "contact [name]"
    ALL = "all"

    # ---------------- Notes ----------------
    ADD_NOTE = "add-note"
    FIND_NOTE_BY_TITLE = "find-note-by-title"
    DELETE_NOTE = "delete-note"
    CHANGE_NOTE = "change-note"
    FIND_NOTE_BY_TAG = "find-note-by-tag"
    ALL_NOTES = "all-notes"
