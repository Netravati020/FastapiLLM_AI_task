from pydantic import BaseModel
from typing import List, Dict

# schemas here
class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    original_text: str
    summary: str
    keywords: List[str]
    sentiment: Dict[str, str]
