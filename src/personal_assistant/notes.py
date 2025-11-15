from .fields import Title, Content, Tags

class Note:
    def __init__(self, title, content=None, tags=None):
        self.title = Title(title)
        self.content = Content(content)
        self.tags = Tags(tags) if tags else ""
    
    def __str__(self) -> str:
        title_str = f"Title: {self.title.value}"
        content_str = f"Content: {self.content}" if self.content else ""
        tag_str = f"Tags: {self.tags}" if self.tags else ""
        return "\n".join(filter(None, [title_str, content_str, tag_str]))
    

class Notes:
    def __init__(self):
        self.notes = []

    # HELPER METHOD (Private) Returns the note tags as a simple string
    def _get_tags_text(self, note) -> str:
        if hasattr(note, 'tags'):
            t = note.tags
            if hasattr(t, 'value'):
                return str(t.value)
            return str(t)
        return ""

    def add_note(self, title, text=None, tags=None) -> str:
        if self.find_note_by_title(title):
            raise ValueError(f"Note with title '{title}' already exists")
        note = Note(title, text, tags)
        self.notes.append(note)
        return f"Note with title '{title}' added successfully."
    
    def find_note_by_title(self, title):
        if not title:
            raise ValueError("Title is required")
        for note in self.notes:
            if note.title.value == title:
                return note
        return None
    
    def delete_note(self, title) -> str:
        note = self.find_note_by_title(title)
        if note:
            self.notes.remove(note)
            return f"Note with title '{title}' deleted successfully."
        else:
            return f"Note with title '{title}' not found"
        
    def change_note(self, title, new_content, new_tags) -> str:
        note = self.find_note_by_title(title)
        if note:
            note.content = Content(new_content) if new_content else note.content
            note.tags = Tags(new_tags) if new_tags else note.tags
            return f"Note with title '{title}' updated successfully."
        else:
            return f"Note with title '{title}' not found"
        
    def find_note_by_tag(self, tag: str) -> list:
        if not tag:
            raise ValueError("Tag is required")
        matched_notes = []
        tag = tag.strip().lower()
        for note in self.notes:
            tags_text = self._get_tags_text(note).lower()

            actual_tags = [t.strip() for t in tags_text.split(',')]
            if tag in actual_tags:
                matched_notes.append(note)

        matched_notes.sort(key=lambda x: self._get_tags_text(x).lower())  
        return matched_notes
    
    def show_all_notes(self) -> str:
        if not self.notes:
            return "No notes available."
        divider = "-" * 40
        notes_str = "\n".join(f"{divider}\n{str(note)}\n{divider}" for note in self.notes)
        return notes_str
    