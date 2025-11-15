def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            match func.__name__:
                case "add_contact":
                    return "Wrong format. Usage: add [contact_name] [phone_number]"
                case "change_contact":
                    return "Wrong format. Usage: change [contact_name] [old_phone_number] [new_phone_number]"
                case "add_birthday":
                    return "Wrong format. Usage: add-birthday [contact_name] [birthday]"
                case "show_birthday":
                    return "Wrong format. Usage: show-birthday [contact_name]"
                case "add_email":
                    return (
                        "Wrong format. Usage: add-email [contact_name] [email_address]"
                    )
                case "change_email":
                    return "Wrong format. Usage: change-email [contact_name] [old_email] [new_email]"
                case "show_email":
                    return "Wrong format. Usage: show-email [contact_name]"
                case "add_address":
                    return "Wrong format. Usage: add-address [contact_name] [address]"
                case "birthdays":
                    return "Wrong format. Usage: birthdays [dates_from_today] - must be an integer"
                case "add_note" | "find_note_by_title" | "delete_note" | "change_note" | "find_note_by_tag":
                    return e
                case _:
                    return "ValueError"
        except KeyError:
            return "KeyError"
        except IndexError:
            match func.__name__:
                case "show_phone":
                    return "Wrong format. Usage: phone [contact_name]"
                case "add_contact":
                    return "Wrong format. Usage: add [contact_name] [phone_number]"
                case "change_contact":
                    return "Wrong format. Usage: change [contact_name] [old_phone_number] [new_phone_number]"
                case "add_birthday":
                    return "Wrong format. Usage: add-birthday [contact_name] [birthday]"
                case "show_birthday":
                    return "Wrong format. Usage: show-birthday [contact_name]"
                case "add_email":
                    return (
                        "Wrong format. Usage: add-email [contact_name] [email_address]"
                    )
                case "change_email":
                    return "Wrong format. Usage: change-email [contact_name] [old_email] [new_email]"
                case "show_email":
                    return "Wrong format. Usage: show-email [contact_name]"
                case "add_address":
                    return "Wrong format. Usage: add-address [contact_name] [address]"
                case _:
                    return "IndexError"

    return inner
