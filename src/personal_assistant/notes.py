from .errors import ValidationError
from .fields import Title, Content, Tags

class Note:
    def __init__(self, title, content=None, tags=None):
        if not title:
            raise ValidationError("Title is required")
        self.title = Title(title)
        self.content = Content(content)
        self.tags = tags if tags else []
    
    def __str__(self) -> str:
        title_str = f"Title: {self.title.value}"
        content_str = f"Content: {self.content}" if self.content else ""
        return "\n".join(filter(None, [title_str, content_str]))
    
    def add_tags(self, note, new_tags):
        if not new_tags:
            return
        note.tags = [str(tag).strip() for tag in new_tags.split(",")]
        for tag in new_tags.split(","):
            if tag not in note.tags:
                note.tags.append(tag)
        return f"Tags added to note with title: '{note.title.value}'."
    

class Notes:
    def __init__(self):
        self.notes = []

    def add_note(self, title, text=None, tags=None):
        if self.find_note_by_title(title):
            raise ValidationError(f"Note with title '{title}' already exists")
        note = Note(title, text, tags)
        self.notes.append(note)
        return f"Note with title '{title}' added successfully."
    
    def find_note_by_title(self, title):
        if not title:
            raise ValidationError("Title is required to find a note")
        for note in self.notes:
            if note.title.value == title:
                return note
        return None
    
    def delete_note(self, title):
        note = self.find_note_by_title(title)
        if note:
            self.notes.remove(note)
            return f"Note with title '{title}' deleted successfully."
        else:
            raise ValidationError(f"Note with title '{title}' not found")
        
    def change_note(self, title, new_content, new_tags):
        note = self.find_note_by_title(title)
        if note:
            note.content = Content(new_content) if new_content else note.content
            note.tags = Tags(new_tags) if new_tags else note.tags
            return f"Note with title '{title}' updated successfully."
        else:
            raise ValidationError(f"Note with title '{title}' not found")
        
    def find_note_by_tag(self, tag):
        if not tag:
            raise ValidationError("Tag is required to find notes")
        matched_notes = [note for note in self.notes if tag in note.tags]
        return matched_notes if matched_notes else []
    
    def show_all_notes(self):
        if not self.notes:
            return "No notes available."
        notes_str = "\n\n".join(str(note) for note in self.notes)
        return notes_str