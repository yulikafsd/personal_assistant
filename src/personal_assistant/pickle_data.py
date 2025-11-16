import os
import pickle
from .addressbook import AddressBook
from .notes import Notes

DEFAULT_DIR = os.path.join(os.path.expanduser("~"), ".assistant")
DEFAULT_FILE = os.path.join(DEFAULT_DIR, "addressbook.pkl")


# Creates directory ~/.assistant if it doesn't exist.
def ensure_data_dir():
    if not os.path.exists(DEFAULT_DIR):
        os.makedirs(DEFAULT_DIR)


# Loads data from ~/.assistant/addressbook.pkl or creates new.
def load_data(filepath=DEFAULT_FILE):
    ensure_data_dir()

    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, "rb") as file:
            data = pickle.load(file)
            return data.get("addressbook", AddressBook()), data.get("notes", Notes())
    else:
        return AddressBook(), Notes()


# Saves data to ~/.assistant/addressbook.pkl.
def save_data(addressbook, notes, filepath=DEFAULT_FILE):
    ensure_data_dir()

    data = {"addressbook": addressbook, "notes": notes}
    with open(filepath, "wb") as file:
        pickle.dump(data, file)
