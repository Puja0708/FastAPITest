from transformers import pipeline

summarizer = pipeline("summarization")

def summarize_conversation(text: str) -> str:
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']
