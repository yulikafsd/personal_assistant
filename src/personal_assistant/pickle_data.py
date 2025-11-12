from .addressbook import AddressBook
from .notes import Notes
import pickle


def save_data(book, notes, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        data = {"address_book": book, "notes": notes}
        pickle.dump(data, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            data = pickle.load(f)
            return data.get("address_book", AddressBook()), data.get("notes", Notes())
    except FileNotFoundError:
        return AddressBook(), Notes()