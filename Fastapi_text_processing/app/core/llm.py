from transformers import pipeline

class LLMService:
    def __init__(self):
        self.summarizer = pipeline("summarization")
        self.keyword_extractor = pipeline("ner")
        self.sentiment_analyzer = pipeline("sentiment-analysis")

    def summarize(self, text):
        return self.summarizer(text, max_length=200, min_length=10, do_sample=False)[0]["summary_text"]

    def extract_keywords(self, text):
        return list(set([entity["word"] for entity in self.keyword_extractor(text)]))

    def analyze_sentiment(self, text):
        return self.sentiment_analyzer(text)[0]

llm_service = LLMService()

