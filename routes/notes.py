from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas import NoteCreate, NoteUpdate, NoteResponse, NoteSummaryRequest, NoteSummaryResponse, TodoExtractionRequest, TodoExtractionResponse
from repository import NotesRepository
from auth import get_current_user
from ai_service import AIService
import asyncio
from config import REQUEST_TIMEOUT

router = APIRouter(prefix="/api/notes", tags=["notes"])
notes_repo = NotesRepository()
ai_service = None  # Lazy loading

@router.post("", response_model=NoteResponse)
async def create_note(
    note_data: NoteCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new note with automatic AI todo extraction"""
    try:
        # Önce normal notu oluştur
        note = await notes_repo.create_note(note_data, current_user["uid"])
        
        # AI ile otomatik todo extraction yap (sadece yeterli içerik varsa)
        if len(note_data.content.strip()) >= 5:
            try:
                global ai_service
                if ai_service is None:
                    try:
                        ai_service = AIService()
                    except ValueError as e:
                        print(f"AI servisi başlatılamadı: {str(e)}")
                        return note
                
                result = await asyncio.wait_for(
                    ai_service.extract_todos(note_data.content),
                    timeout=35.0
                )
                
                if result["hasTodos"] and result["todos"]:
                    # Todo'lar bulundu, notu güncelle
                    updated_note = await notes_repo.update_note_todos(
                        note.id, 
                        result["todos"], 
                        current_user["uid"]
                    )
                    return updated_note
                    
            except asyncio.TimeoutError:
                print("AI todo extraction timeout")
            except Exception as e:
                print(f"AI todo extraction error: {e}")
        
        return note
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create note: {str(e)}"
        )

@router.get("", response_model=List[NoteResponse])
async def get_notes(current_user: dict = Depends(get_current_user)):
    """Get all notes for the current user"""
    try:
        notes = await notes_repo.get_notes_by_owner(current_user["uid"])
        return notes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch notes: {str(e)}"
        )

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific note by ID"""
    try:
        note = await notes_repo.get_note_by_id(note_id, current_user["uid"])
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return note
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch note: {str(e)}"
        )

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    note_data: NoteUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a note"""
    try:
        note = await notes_repo.update_note(note_id, note_data, current_user["uid"])
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return note
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update note: {str(e)}"
        )

@router.delete("/{note_id}")
async def delete_note(
    note_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a note (soft delete)"""
    try:
        success = await asyncio.wait_for(
            notes_repo.delete_note(note_id, current_user["uid"]),
            timeout=REQUEST_TIMEOUT
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return {"message": "Note deleted successfully"}
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="Request timeout - please try again"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete note: {str(e)}"
        )

@router.delete("/{note_id}/permanent")
async def permanent_delete_note(
    note_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Permanently delete a note"""
    try:
        success = await notes_repo.hard_delete_note(note_id, current_user["uid"])
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return {"message": "Note permanently deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to permanently delete note: {str(e)}"
        )

@router.post("/summarize", response_model=NoteSummaryResponse)
async def summarize_note(
    request: NoteSummaryRequest,
    # current_user: dict = Depends(get_current_user)  # Test için geçici olarak kaldırıldı
):
    """AI ile not içeriğini özetle"""
    try:
        # İçerik uzunluğunu kontrol et
        if len(request.content.strip()) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="İçerik çok kısa, özetleme için en az 5 karakter gerekli"
            )
        
        # AI servisini lazy loading ile initialize et
        global ai_service
        if ai_service is None:
            try:
                ai_service = AIService()
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"AI servisi başlatılamadı: {str(e)}"
                )
        
        # AI servisi ile özetleme yap (timeout ile)
        try:
            result = await asyncio.wait_for(
                ai_service.summarize_note(request.content),
                timeout=35.0  # 35 saniye timeout
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="AI özetleme işlemi zaman aşımına uğradı"
            )
        
        return NoteSummaryResponse(
            summary=result["summary"],
            keyPoints=result["keyPoints"],
            wordCount=result["wordCount"],
            originalWordCount=result["originalWordCount"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Özetleme işlemi başarısız: {str(e)}"
        )

@router.post("/extract-todos", response_model=TodoExtractionResponse)
async def extract_todos(
    request: TodoExtractionRequest,
    # current_user: dict = Depends(get_current_user)  # Test için geçici olarak kaldırıldı
):
    """AI ile not içeriğinden yapılacak işleri çıkar"""
    try:
        # İçerik uzunluğunu kontrol et
        if len(request.content.strip()) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="İçerik çok kısa, yapılacak iş algılama için en az 5 karakter gerekli"
            )
        
        # AI servisini lazy loading ile initialize et
        global ai_service
        if ai_service is None:
            try:
                ai_service = AIService()
            except ValueError as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"AI servisi başlatılamadı: {str(e)}"
                )
        
        # AI servisi ile yapılacak işleri çıkar (timeout ile)
        try:
            result = await asyncio.wait_for(
                ai_service.extract_todos(request.content),
                timeout=35.0  # 35 saniye timeout
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
                detail="AI yapılacak iş algılama işlemi zaman aşımına uğradı"
            )
        
        return TodoExtractionResponse(
            hasTodos=result["hasTodos"],
            todos=result["todos"],
            originalContent=result["originalContent"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Yapılacak iş algılama işlemi başarısız: {str(e)}"
        )
