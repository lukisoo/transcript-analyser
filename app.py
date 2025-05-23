import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from analysis import parse_transcript

# Analyse the transcript, and create the graphs to display metrics
def analyse_transcript():
    results = parse_transcript("transcript.txt")
    df = pd.DataFrame(results["transcript"])
    stats = results["filler_stats"]

    # Plot 1: The filler ratio per line
    fig1, ax1 = plt.subplots(figsize=(8, 3))
    ax1.bar(df.index + 1, df["filler_ratio"], color="salmon")
    ax1.set_title("Filler Ratio per Turn")
    ax1.set_xlabel("Turn")
    ax1.set_ylabel("Filler Ratio")
    ax1.set_xticks(df.index + 1)
    plt.tight_layout()
    plt.close(fig1)

    # Plot 2: The sentiment distribution across positive, negative, neutral
    sentiment_counts = df["sentiment"].value_counts()
    total_turns = sentiment_counts.sum()
    sentiment_props = (sentiment_counts / total_turns * 100).round(1)

    fig2, ax2 = plt.subplots(figsize=(4, 3))
    sentiment_counts.plot(kind="bar", ax=ax2, color="skyblue")
    ax2.set_title("Sentiment Distribution")
    ax2.set_ylabel("Count")
    plt.tight_layout()
    plt.close(fig2)

    # Plot 3: The average filler ratio per speaker
    avg_ratios = {
        "Speaker A": stats["a_filler"] / stats["a_words"] if stats["a_words"] else 0,
        "Speaker B": stats["b_filler"] / stats["b_words"] if stats["b_words"] else 0
    }

    fig3, ax3 = plt.subplots(figsize=(4, 3))
    pd.Series(avg_ratios).plot(kind="bar", color="lightgreen", ax=ax3)
    ax3.set_title("Average Filler Ratio per Speaker")
    ax3.set_ylabel("Filler Ratio")
    plt.tight_layout()
    plt.close(fig3)

    # Plot 4: The total filler words per speaker
    total_filler_words = {
        "Speaker A": stats["a_filler"],
        "Speaker B": stats["b_filler"]
    }

    fig4, ax4 = plt.subplots(figsize=(4, 3))
    pd.Series(total_filler_words).plot(kind="bar", color="orange", ax=ax4)
    ax4.set_title("Total Filler Words per Speaker")
    ax4.set_ylabel("Filler Word Count")
    plt.tight_layout()
    plt.close(fig4)

    # Summary for filler words, with a comparison between both speakers
    a_filler = stats["a_filler"]
    b_filler = stats["b_filler"]
    winner = "Speaker A" if a_filler > b_filler else "Speaker B"
    diff = abs(a_filler - b_filler)

    # Sentiment summary
    most_common = sentiment_counts[sentiment_counts == sentiment_counts.max()].index.tolist()
    most_common_str = " & ".join(most_common).capitalize()
    sentiment_summary = " | ".join([f"{k.capitalize()}: {v:.1f}%" for k, v in sentiment_props.items()])

    # Word totals
    total_words = stats["total_words"]
    total_filler = stats["total_filler"]

    summary = (
        f"Overall Filler Ratio: {results['overall_filler_ratio'] * 100:.2f}%\n"
        f"Total Words: {total_words} | Filler Words: {total_filler}\n"
        f"{winner} used more filler words - by {diff} words.\n\n"
        f"Sentiment Summary\n"
        f"{sentiment_summary}\n"
        f"Most common sentiment(s): {most_common_str}"
    )

    return df, fig1, fig2, fig3, fig4, summary


# Use Gradio blocks layout to get rows and columns for visualisations and summary
with gr.Blocks(title="Transcript Sentiment + Filler Word Dashboard") as iface:
    gr.Markdown("## Transcript Sentiment + Filler Word Dashboard")

    df_output = gr.Dataframe(label="Per-Turn Transcript Analysis")
    summary_output = gr.Textbox(label="Summary", lines=8)
    fig1_output = gr.Plot(label="Filler Ratio per Turn")
    fig2_output = gr.Plot(label="Sentiment Distribution")

    with gr.Row():
        fig3_output = gr.Plot(label="Avg Filler Ratio per Speaker", scale=1)
        fig4_output = gr.Plot(label="Total Filler Words per Speaker", scale=1)

    gr.Button("Load or Refresh Analysis").click(
        analyse_transcript,
        inputs=[],
        outputs=[df_output, fig1_output, fig2_output, fig3_output, fig4_output, summary_output]
    )

if __name__ == "__main__":
    iface.launch()
