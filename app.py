from analysis import parse_transcript

# Test the data parsing
def show_transcript():
    data = parse_transcript("transcript.txt")
    return data

if __name__ == "__main__":
    # Print out the transcript with sentiment
    for entry in show_transcript():
        print(f"{entry['speaker']}: {entry['text']} -> Sentiment: {entry.get('sentiment', 'N/A')}")
