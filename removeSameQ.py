import json

# Specify your input and output file paths
input_file = "/Python311/DLLs/a_cleaned.jsonl"
output_file = "/Python311/DLLs/cleaned.jsonl"

# Dictionary to store the best (longest) record for each unique instruction
# The key is the instruction, the value is a dict with the record and its line length.
records = {}

# Open and read the input file line by line
with open(input_file, "r") as f:
    for line in f:
        try:
            record = json.loads(line)
            instruction = record.get("instruction", "").strip()
            line_length = len(line)
            # If the instruction already exists, compare the line lengths.
            if instruction in records:
                if line_length > records[instruction]["line_length"]:
                    records[instruction] = {"record": record, "line_length": line_length}
            else:
                records[instruction] = {"record": record, "line_length": line_length}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

# Write the deduplicated records to a new output file
with open(output_file, "w") as fout:
    for item in records.values():
        json.dump(item["record"], fout)
        fout.write("\n")

print("Deduplication complete. Cleaned data written to:", output_file)

