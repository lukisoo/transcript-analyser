from analysis import parse_transcript

# Test the data parsing
def show_transcript():
    data = parse_transcript("transcript.txt")
    return data

if __name__ == "__main__":
    print(show_transcript())
