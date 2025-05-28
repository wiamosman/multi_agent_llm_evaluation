import os

emoji_to_label = {
    "😃": "Joyful",
    "🤔": "Thoughtful",
    "😔": "Sad",
    "😒": "Annoyed",
    "😐": "Neutral",
    "🙄": "Annoyed",
    "😏": "Smug",
    "🙅‍♀️": "Dismissive",
    "😜": "Playful",
    "🌊": "Powerful",
    "😂": "Laughing",
    "🎉": "Celebration",
    "😋": "Delighted",
    "🙃": "Playful",
    "😎": "Cool",
    "😍": "Loving",
    "😕": "Confused",
    "📚": "Studious",
    "🙅‍♂️": "Dismissive",
    "😆": "Happy",
    "😠": "Angry",
    "😡": "Angry",
    "🍹": "Fun",
    "👋": "Goodbye",
    "😉": "Winking",
    "🎭": "Drama",
    "🙂": "Friendly",
    "😨": "Fearful",
    "🤷‍♀️": "Shrug",
    "🤯": "Shocked",
    "😊": "Happy",
    "😴": "Tired",
    "😅": "Nervous",
    "💡": "Thoughtful",
    "👀": "Curious",
    "😲": "Surprised"
}

def replace_emoji_with_label(line, emoji_map):
    replaced_any = False
    for emoji, label in emoji_map.items():
        if emoji in line:
            line = line.replace(emoji, f" @{label}$")
            replaced_any = True
    return line, replaced_any

def process_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if not filename.endswith(".txt"):
            continue

        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        print(f"\nProcessing file: {filename}")
        with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
            for line_number, line in enumerate(infile, 1):
                new_line, changed = replace_emoji_with_label(line.strip(), emoji_to_label)
                if changed:
                    print(f"Line {line_number}: replaced -> {new_line}")
                outfile.write(new_line + "\n")

    print("\nAll files processed successfully.")

# Example usage:
input_folder = "predictions/llama2"  # your input folder with original files
output_folder = "predictions-altered-manually-for-evaluation/llama2"  # output folder for processed files

process_folder(input_folder, output_folder)
