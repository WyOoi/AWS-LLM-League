import re

# Load your text
with open('a.json', 'r', encoding='utf-8') as file:
    data = file.read()

# Replace problematic characters
cleaned = data \
    .replace('‘', "'") \
    .replace('’', "'") \
    .replace('“', '"') \
    .replace('”', '"') \
    .replace('—', '-') \
    .replace('√', '')

# Optional: Remove non-ASCII characters if unsure
cleaned = re.sub(r'[^\x00-\x7F]+', '', cleaned)

# Save the cleaned file
with open('a_cleaned.jsonl', 'w', encoding='utf-8') as file:
    file.write(cleaned)

