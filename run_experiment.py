from openai import OpenAI

# import os
# from together import Together

#client = Together(api_key="key")

#Initialize client for Ollama local server
# client = OpenAI(
#     base_url="http://localhost:11434/",
#     api_key="ollama"
# )

# Local models on a local server (you must have them installed)

client = OpenAI(
    api_key="KEY",
    base_url="LOCAL"
)

MODEL = "gpt-4-turbo"
EXAMPLES = ["01", "11", "21"]


def predict(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an assistant that fills in missing annotations in dialogues."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.2,
    )
    return response.choices[0].message.content
#together llama
# def predict(prompt):
#     # Use client.chat.completions.create for chat models
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": "You are an assistant that fills in missing annotations in dialogues."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=1500,
#         temperature=0.2,
#     )
#     print("Raw response:", response)
#     return response.choices[0].message.content

# ----for local Ollama server----
# import requests

# BASE_URL = "http://localhost:11434"

# def predict(prompt):
#     url = f"{BASE_URL}/v1/chat/completions"
#     headers = {"Content-Type": "application/json"}
#     payload = {
#         "model": "llama2:latest",
#         "messages": [
#             {"role": "system", "content": "You are an assistant that fills in missing annotations in dialogues."},
#             {"role": "user", "content": prompt}
#         ],
#         "max_tokens": 1500,
#         "temperature": 0.2,
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     response.raise_for_status()
#     data = response.json()
#     print("Raw response:", data)
#     return data["choices"][0]["message"]["content"]



def process(prompt, dialogue_number):
    dialogue_path = f"dialogues-with-blanks/dialogue{dialogue_number}.txt"
    with open(dialogue_path, "r") as f:
        dialogue = f.read().rstrip()

    prompt_filled = prompt.replace("{dialogue_with_blanks}", dialogue)
    prediction = predict(prompt_filled)

    prediction_path = f"predictions/{MODEL}/prediction{dialogue_number}.txt"
    with open(prediction_path, "w") as f:
        f.write(prediction)

def main():
    print(f"Model: {MODEL}")
    print(f"Dialogues used for training: {EXAMPLES}")
    print("Processing...")

    with open("prompt.txt", "r") as f:
        prompt = f.read().rstrip()

    examples = []
    for ex_num in EXAMPLES:
        with open(f"dialogues/dialogue{ex_num}.txt", "r") as f:
            examples.append(f.read().rstrip())

    # Insert examples into prompt template
    prompt = prompt.replace("{example_dialogue_1}", examples[0])
    prompt = prompt.replace("{example_dialogue_2}", examples[1])
    prompt = prompt.replace("{example_dialogue_3}", examples[2])

    for i in range(1, 36):
        dialogue_number = f"{i:02d}"
        if dialogue_number in EXAMPLES:
            print(f"{dialogue_number}/35 (In training examples, skipping)")
            continue
        print(f"{dialogue_number}/35")
        process(prompt, dialogue_number)

    print("Done.")

if __name__ == "__main__":
    main()
