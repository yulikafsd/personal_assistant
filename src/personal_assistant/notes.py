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
        
    def find_note_by_tag(self, tag) -> list:
        if not tag:
            raise ValueError("Tag is required")
        matched_notes = []
        for note in self.notes: # Check if note.tags has a 'value' attribute (is it a Tags object)
            if hasattr(note.tags, 'value'):
                tags_text = note.tags.value 
            else:
                tags_text = str(note.tags) # If not, assume it's just a string
            
            if tag in tags_text:
                matched_notes.append(note)   
        return matched_notes
    
    def show_all_notes(self) -> str:
        if not self.notes:
            return "No notes available."
        notes_str = "\n\n".join(str(note) for note in self.notes)
        return notes_str
    