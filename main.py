import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os

# Initialize FastAPI app
app = FastAPI(title="Text Processing API (OpenAI)", version="1.0")

# Store processed history
history: List[Dict] = []

# Set OpenAI API Key (Replace with actual API key)
openai.api_key = ""

class TextRequest(BaseModel):
    text: str

def openai_request(prompt: str, max_tokens: int = 100):
    """Helper function to call OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=max_tokens
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")


@app.post("/process", tags=["Processing"])
def process_text(request: TextRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    # OpenAI LLM Processing
    summary = openai_request(f"Summarize the following text:\n{text}", max_tokens=50)
    keywords = openai_request(f"Extract important keywords from the text:\n{text}", max_tokens=30)
    sentiment = openai_request(f"Analyze the sentiment of the text:\n{text}", max_tokens=10)

    result = {
        "original_text": text,
        "summary": summary,
        "keywords": keywords.split(", "),  # Convert response to list
        "sentiment": sentiment
    }

    history.append(result)  # Save to history
    return result

@app.get("/history", tags=["History"])
def get_history():
    """Retrieve all processed history"""
    if not history:
        raise HTTPException(status_code=404, detail="No history found")
    return {"history": history}


@app.get("/history/{index}", tags=["History"])
def get_history_entry(index: int):
    """Retrieve a specific history entry"""
    if 0 <= index < len(history):
        return history[index]
    raise HTTPException(status_code=404, detail="Entry not found")


@app.delete("/history", tags=["History"])
def clear_history():
    """Clear all stored history"""
    history.clear()
    return {"message": "History cleared successfully"}
