from transformers import pipeline
import re

# List of words considered 'filler words'
FILLER_WORDS = {"um", "uh", "like", "you know", "i mean", "so"}

# Load the model for sentiment analysis
# Using https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest for three class output (positive, neutral, negative)
sentiment_analyser = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

# Count filler words and total words for each line
def compute_filler_ratio(text, filler_data, speaker):
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Get the filler ratio per line
    word_count = len(words)
    filler_count = sum(1 for word in words if word in FILLER_WORDS)
    line_filler_ratio = round(filler_count / word_count, 3) if word_count else 0.0
    
    # Update filler counts for speaker A, speaker B, and in total
    if speaker == "A":
        filler_data["a_filler"] += filler_count
        filler_data["a_words"] += word_count
    else:
        filler_data["b_filler"] += filler_count
        filler_data["b_words"] += word_count
        
    filler_data["total_filler"] += filler_count
    filler_data["total_words"] += word_count

    return line_filler_ratio, filler_data

def compute_sentiment(text):
    result = sentiment_analyser(text)[0]['label']
    return label_map.get(result, result)

# Parse the transcript, print to test
def parse_transcript(path="transcript.txt"):
    with open(path, "r") as f:
        lines = f.readlines()
    data = []
    # Keep track of per-speaker filler data and running totals for later reporting
    filler_data = {"a_filler": 0, "a_words":0, "b_filler": 0, "b_words":0, "total_filler": 0, "total_words": 0}
    
    # Iterate through each line to split and analyse
    for line in lines:
        if ":" in line:
            speaker, text = line.split(":", 1)
            speaker = speaker.strip()[-1]
            text = text.strip()

			# Compute sentiment and filler ratio
            sentiment = compute_sentiment(text)
            line_filler_ratio, filler_data = compute_filler_ratio(text, filler_data, speaker)

            data.append({
                "speaker": speaker,
                "text": text,
                "sentiment": sentiment,
                "filler_ratio": line_filler_ratio
            })

    overall_filler_ratio = round(filler_data["total_filler"] / filler_data["total_words"], 3) if filler_data["total_words"] else 0.0

    return {
        "transcript": data,
        "overall_filler_ratio": overall_filler_ratio,
        "filler_stats" : filler_data
    }