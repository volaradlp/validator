import os
import json

INPUT_DIR = '/input'
OUTPUT_DIR = '/output'
SEALED_DIR = '/sealed'

expected_words = ["hello", "world"]

# Gramine will auto encrypt/decrypt anything in SEALED_DIR
def process_on_disk(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f).get('data', '')

    sealed_file = os.path.join(SEALED_DIR, f'{os.path.basename(input_file)}_sealed.txt')

    with open(sealed_file, 'w') as sf:
        for word in expected_words:
            if word in data:
                sf.write(f"{word}\n")

    with open(sealed_file, 'r') as sf:
        found_count = sum(1 for _ in sf)

    return {"valid_contribution": found_count == len(expected_words)}

def process_in_memory(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f).get('data', '')

    found_keywords = set()
    found_keywords.update(word for word in expected_words if word in data)

    return {"valid_contribution": len(found_keywords) == len(expected_words)}

def generate_proof():
    use_sealing = os.path.isdir(SEALED_DIR)

    for filename in os.listdir(INPUT_DIR):
        input_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, f"{filename}_result.json")

        if use_sealing:
            result = process_on_disk(input_path)
        else:
            result = process_in_memory(input_path)

        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)


if __name__ == "__main__":
    generate_proof()
    print("Proof generation complete. Check the output directory for results.")