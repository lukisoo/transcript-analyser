from transformers import pipeline

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
    
    # Iterate through each line to split into corresponding speaker:text pairs
    for line in lines:
        if ":" in line:
            speaker, text = line.split(":", 1)
            data.append({
                "speaker": speaker.strip(),
                "text": text.strip(),
                "sentiment": detect_sentiment(text)
            })
    
    return data
