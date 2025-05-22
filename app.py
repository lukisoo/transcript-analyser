from analysis import parse_transcript

if __name__ == "__main__":
    # Print out the transcript
    results = parse_transcript("transcript.txt")

    print("Transcript with Metrics:\n")
    for entry in results["transcript"]:
        print(f"{entry['speaker']}: {entry['text']} → Sentiment: {entry['sentiment']}, Filler Ratio: {entry['filler_ratio']}")

    print("\nOverall Filler Word Ratio:")
    print(f"{results['overall_filler_ratio']}")