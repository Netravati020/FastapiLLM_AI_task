from fastapi import APIRouter, HTTPException,Security,Depends
from app.api.models import TextRequest, TextResponse
from app.api.services import process_text
from app.core.config import config    # Import config for API keys
from app.database.history import history_storage
from fastapi.security.api_key import APIKeyHeader

router = APIRouter()
# Define API key security
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

def validate_api_key(api_key: str = Security(api_key_header)):
    """Validate API Key"""
    if api_key != config.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# input as Text
@router.post("/process", response_model=TextResponse, dependencies=[Depends(validate_api_key)])
def process_text_api(request: TextRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    result = process_text(text)
    history_storage.append(result)   # Save history
    return result

@router.get("/history",dependencies=[Depends(validate_api_key)])
def get_history():
    """Retrieve all processed history"""
    if not history_storage:
        raise HTTPException(status_code=404, detail="No history found")
    return {"history": history_storage}

@router.get("/history/{index}",dependencies=[Depends(validate_api_key)])
def get_history_entry(index: int):
    """Retrieve a specific history entry"""
    if 0 <= index < len(history_storage):
        return history_storage[index]
    raise HTTPException(status_code=404, detail="Entry not found")

@router.delete("/history",dependencies=[Depends(validate_api_key)])
def delete_history():
    """delete all processed history"""
    history_storage.clear()
    return {"message": "History cleared"}

@router.delete("/history/{index}",dependencies=[Depends(validate_api_key)])
def delete_specific_history(index: int):
    """Delete a specific history entry by index"""
    if 0 <= index < len(history_storage):
        deleted_entry = history_storage.pop(index)  # Remove the entry at index
        return {"message": "Entry deleted successfully", "deleted_entry": deleted_entry}

    raise HTTPException(status_code=404, detail="Entry not found")