import json
from sentence_transformers import SentenceTransformer, util

# Path to your JSONL file
file_path = "/Python311/DLLs/cleanedV2.jsonl"

# Load a pre-trained SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Read the file and extract the "instruction" field along with line numbers
questions = []
line_numbers = []
with open(file_path, 'r') as f:
    for i, line in enumerate(f, start=1):
        try:
            data = json.loads(line)
            instruction = data.get("instruction", "").strip()
            if instruction:
                questions.append(instruction)
                line_numbers.append(i)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line {i}: {e}")

# Compute embeddings for all questions
embeddings = model.encode(questions, convert_to_tensor=True)

# Compute pairwise cosine similarities
cosine_scores = util.cos_sim(embeddings, embeddings)

# Define a threshold for similarity (e.g., 0.8 means 80% similarity)
threshold = 0.92
similar_pairs = []

# Iterate over pairs (avoid duplicate and self-comparison)
num_questions = len(questions)
for i in range(num_questions):
    for j in range(i + 1, num_questions):
        if cosine_scores[i][j] >= threshold:
            similar_pairs.append((line_numbers[i], line_numbers[j], float(cosine_scores[i][j])))

# Print the similar question pairs with their line numbers and similarity scores
for pair in similar_pairs:
    print(f"Line {pair[0]} and Line {pair[1]} have similarity score: {pair[2]:.4f}")

