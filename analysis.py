# Parse the transcript, print to test
def parse_transcript(path="transcript.txt"):
    with open(path, "r") as f:
        lines = f.readlines()
    data = []
    
    # Iterate through each line to split the list into corresponding speaker:text pairs
    for line in lines:
        if ":" in line:
            speaker, text = line.split(":", 1)
            data.append({
                "speaker": speaker.strip(),
                "text": text.strip()
            })
    
    return data
