from transformers import pipeline
import re

FILLER_WORDS = {"um", "uh", "like", "you know", "i mean", "so"}

def compute_filler_ratio(text):
    words = re.findall(r'\b\w+\b', text.lower())
    filler_count = sum(1 for word in words if word in FILLER_WORDS)
    return filler_count, len(words)

# Load the model for sentiment analysis
# Using https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest for three class output (positive, neutral, negative)
sentiment_analyser = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

def detect_sentiment(text):
    result = sentiment_analyser(text)[0]['label']
    return label_map.get(result, result)

# Parse the transcript, print to test
def parse_transcript(path="transcript.txt"):
    with open(path, "r") as f:
        lines = f.readlines()
    data = []
    total_filler = 0
    total_words = 0
    
    # Iterate through each line to split and analyse
    for line in lines:
        if ":" in line:
            speaker, text = line.split(":", 1)
            speaker = speaker.strip()
            text = text.strip()

            sentiment = detect_sentiment(text)
            filler_count, word_count = compute_filler_ratio(text)
            print(filler_count, word_count)
            filler_ratio = round(filler_count / word_count, 3) if word_count else 0.0

            total_filler += filler_count
            total_words += word_count

            data.append({
                "speaker": speaker,
                "text": text,
                "sentiment": sentiment,
                "filler_ratio": filler_ratio
            })

    overall_filler_ratio = round(total_filler / total_words, 3) if total_words else 0.0

    return {
        "transcript": data,
        "overall_filler_ratio": overall_filler_ratio
    }