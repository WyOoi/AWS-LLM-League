import json
from sentence_transformers import SentenceTransformer, util

# File paths
input_file = "/Python311/DLLs/cleanedV2.jsonl"
output_file = "/Python311/DLLs/cleanedV3.jsonl"

# Similarity threshold (e.g., 0.8 means 80% similarity)
threshold = 0.85

# Load a pre-trained SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Read the file and store records along with metadata
records = []  # each element: { "line_num": int, "instruction": str, "line": str }
with open(input_file, 'r') as f:
    for i, line in enumerate(f, start=1):
        try:
            data = json.loads(line)
            instruction = data.get("instruction", "").strip()
            if instruction:
                records.append({
                    "line_num": i,
                    "instruction": instruction,
                    "line": line,  # raw line text
                    "length": len(line)
                })
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line {i}: {e}")

# Create list of instructions and their corresponding lengths
instructions = [rec["instruction"] for rec in records]
lengths = [rec["length"] for rec in records]
line_nums = [rec["line_num"] for rec in records]

# Compute embeddings for all instructions
embeddings = model.encode(instructions, convert_to_tensor=True)

# Keep a set of indices to delete
indices_to_delete = set()

# Iterate over pairs of records (only unique pairs)
num_records = len(records)
for i in range(num_records):
    # Skip if already marked for deletion
    if i in indices_to_delete:
        continue
    for j in range(i + 1, num_records):
        if j in indices_to_delete:
            continue
        similarity = util.cos_sim(embeddings[i], embeddings[j]).item()
        if similarity >= threshold:
            # Determine which record has less length and mark it for deletion
            if lengths[i] < lengths[j]:
                indices_to_delete.add(i)
                break  # Once i is marked, no need to compare with others
            else:
                indices_to_delete.add(j)

print(f"Total records to delete: {len(indices_to_delete)}")

# Write out only the records that are not marked for deletion
with open(output_file, "w") as fout:
    for idx, rec in enumerate(records):
        if idx not in indices_to_delete:
            fout.write(rec["line"])

print("Deduplication complete. Cleaned data written to:", output_file)

