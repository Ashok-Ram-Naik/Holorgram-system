import matplotlib.pyplot as plt
import numpy as np
import os

# --- GESTURE DATA ---
gesture_labels = ['None', 'Thumb Up', 'Index Point', 'Open Palm', 'Closed Fist']
gesture_precision = [0.96, 1.00, 0.96, 0.85, 0.80]
gesture_recall = [0.82, 1.00, 0.95, 0.98, 0.82]
gesture_f1 = [0.88, 1.00, 0.95, 0.91, 0.81]

# --- VOICE DATA ---
voice_labels = ['Next', 'Previous', 'Rotate', 'Stop', 'Background']
voice_precision = [1.00, 1.00, 1.00, 0.97, 0.85]
voice_recall = [0.97, 0.97, 0.85, 0.99, 1.00]
voice_f1 = [0.99, 0.98, 0.92, 0.98, 0.92]

def plot_bar_chart(labels, precision, recall, f1, title, filename, color_map):
    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plotting the bars
    rects1 = ax.bar(x - width, precision, width, label='Precision', color=color_map[0])
    rects2 = ax.bar(x, recall, width, label='Recall', color=color_map[1])
    rects3 = ax.bar(x + width, f1, width, label='F1-Score', color=color_map[2])

    # Adding text and labels
    ax.set_ylabel('Scores', fontsize=12)
    ax.set_title(title, fontsize=16)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.legend(loc='lower right')

    # Adding grid for readability
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='gray', linestyle='dashed', alpha=0.3)

    # Function to attach a text label above each bar
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    fig.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Saved: {os.path.abspath(filename)}")
    plt.close()

if __name__ == '__main__':
    print("Generating Bar Graphs...")
    
    # Colors: Blues for Gesture, Oranges for Voice
    plot_bar_chart(
        gesture_labels, gesture_precision, gesture_recall, gesture_f1,
        'Gesture Model Performance by Class',
        'gesture_bar_graph.png',
        ['#93c5fd', '#3b82f6', '#1e3a8a']
    )
    
    plot_bar_chart(
        voice_labels, voice_precision, voice_recall, voice_f1,
        'Voice Model Performance by Class',
        'voice_bar_graph.png',
        ['#fdba74', '#f97316', '#9a3412']
    )
    
    print("Done!")
