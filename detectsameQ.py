import json

# Path to your JSONL file
file_path = "/Python311/DLLs/a_cleaned.jsonl"

# Dictionary to track occurrences of each question along with line numbers
question_lines = {}

# Read file line by line
with open(file_path, "r") as f:
    for line_num, line in enumerate(f, start=1):
        try:
            entry = json.loads(line)
            question = entry.get("instruction", "").strip()
            if question:
                question_lines.setdefault(question, []).append(line_num)
        except json.JSONDecodeError:
            print(f"Error decoding JSON on line {line_num}")

# Identify repeated questions
repeated = {q: nums for q, nums in question_lines.items() if len(nums) > 1}

# Print repeated questions with their line numbers
for question, lines in repeated.items():
    print(f"Question: {question}\nRepeated on lines: {lines}\n")

