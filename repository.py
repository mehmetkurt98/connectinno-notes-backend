from firebase_config import db
from schemas import NoteCreate, NoteUpdate, NoteResponse
from typing import List, Optional
from datetime import datetime
import uuid
from google.cloud import firestore

class NotesRepository:
    def __init__(self):
        self.collection = db.collection('notes')
    
    async def create_note(self, note_data: NoteCreate, owner_uid: str) -> NoteResponse:
        """Create a new note"""
        # Frontend'den gelen ID'yi kullan, yoksa yeni oluştur
        note_id = getattr(note_data, 'id', None) or str(uuid.uuid4())
        now = datetime.utcnow()
        
        note_doc = {
            "id": note_id,
            "title": note_data.title,
            "content": note_data.content,
            "owner_uid": owner_uid,
            "created_at": now,
            "updated_at": now,
            "dirty": False,
            "deleted": False,
            "hasTodos": False,
            "todos": []
        }
        
        # Direct Firestore operation - much faster
        self.collection.document(note_id).set(note_doc)
        
        return NoteResponse(**note_doc)
    
    async def get_notes_by_owner(self, owner_uid: str) -> List[NoteResponse]:
        """Get all notes for a specific owner"""
        notes = []
        try:
            # Simplified query without order_by to avoid index requirement
            docs = (self.collection
                    .where("owner_uid", "==", owner_uid)
                    .where("deleted", "==", False)
                    .limit(100)
                    .stream())
            
            for doc in docs:
                note_data = doc.to_dict()
                notes.append(NoteResponse(**note_data))
            
            # Sort in Python instead of Firestore
            notes.sort(key=lambda x: x.updatedAt, reverse=True)
            
        except Exception as e:
            print(f"Firestore query error: {e}")
            # Fallback: get all notes and filter in Python
            docs = self.collection.limit(100).stream()
            for doc in docs:
                note_data = doc.to_dict()
                if (note_data.get("owner_uid") == owner_uid and 
                    note_data.get("deleted", False) == False):
                    notes.append(NoteResponse(**note_data))
            notes.sort(key=lambda x: x.updatedAt, reverse=True)
        
        return notes
    
    async def get_note_by_id(self, note_id: str, owner_uid: str) -> Optional[NoteResponse]:
        """Get a specific note by ID"""
        doc = self.collection.document(note_id).get()
        
        if not doc.exists:
            return None
        
        note_data = doc.to_dict()
        
        # Check if the note belongs to the owner
        if note_data.get("owner_uid") != owner_uid:
            return None
        
        return NoteResponse(**note_data)
    
    async def update_note(self, note_id: str, note_data: NoteUpdate, owner_uid: str) -> Optional[NoteResponse]:
        """Update a note"""
        doc_ref = self.collection.document(note_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return None
        
        existing_note = doc.to_dict()
        
        # Check if the note belongs to the owner
        if existing_note.get("owner_uid") != owner_uid:
            return None
        
        # Update only provided fields
        update_data = {"updated_at": datetime.utcnow()}
        
        if note_data.title is not None:
            update_data["title"] = note_data.title
        
        if note_data.content is not None:
            update_data["content"] = note_data.content
        
        doc_ref.update(update_data)
        
        # Get updated document
        updated_doc = doc_ref.get()
        return NoteResponse(**updated_doc.to_dict())
    
    async def delete_note(self, note_id: str, owner_uid: str) -> bool:
        """Soft delete a note"""
        doc_ref = self.collection.document(note_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return False
        
        note_data = doc.to_dict()
        
        # Check if the note belongs to the owner
        if note_data.get("owner_uid") != owner_uid:
            return False
        
        # Soft delete - direct operation
        doc_ref.update({
            "deleted": True,
            "updated_at": datetime.utcnow()
        })
        
        return True
    
    async def hard_delete_note(self, note_id: str, owner_uid: str) -> bool:
        """Permanently delete a note"""
        doc_ref = self.collection.document(note_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return False
        
        note_data = doc.to_dict()
        
        # Check if the note belongs to the owner
        if note_data.get("owner_uid") != owner_uid:
            return False
        
        doc_ref.delete()
        return True
    
    async def update_note_todos(self, note_id: str, todos: list, owner_uid: str) -> NoteResponse:
        """Update note with extracted todos"""
        doc_ref = self.collection.document(note_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise Exception("Note not found")
        
        note_data = doc.to_dict()
        
        # Check if the note belongs to the owner
        if note_data.get("owner_uid") != owner_uid:
            raise Exception("Unauthorized")
        
        # Update todos
        update_data = {
            "updated_at": datetime.utcnow(),
            "hasTodos": True,
            "todos": todos
        }
        
        doc_ref.update(update_data)
        
        # Get updated document
        updated_doc = doc_ref.get()
        return NoteResponse(**updated_doc.to_dict())
