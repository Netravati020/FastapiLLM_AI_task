from app.core.llm import llm_service

def process_text(text: str):
    summary = llm_service.summarize(text)
    keywords = llm_service.extract_keywords(text)
    sentiment = llm_service.analyze_sentiment(text)

    return {
        "original_text": text,
        "summary": summary,
        "keywords": keywords,
        "sentiment": sentiment
    }
