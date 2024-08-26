import os
import json
import requests
import logging
from typing import Dict, Any, List, Callable

INPUT_DIR, OUTPUT_DIR, SEALED_DIR = '/input', '/output', '/sealed'

logging.basicConfig(level=logging.INFO, format='%(message)s')

def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    config = {
        'expected_words': os.environ.get('MY_PROOF_EXPECTED_WORDS', 'hello,world').split(','),
        'random_threshold': float(os.environ.get('MY_PROOF_RANDOM_THRESHOLD', '0.5'))
    }
    logging.info(f"Config: expected words = {config['expected_words']}, threshold = {config['random_threshold']}")
    return config

def fetch_random_number() -> float:
    """Demonstrate HTTP requests by fetching a random number from random.org."""
    try:
        response = requests.get('https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new')
        return float(response.text.strip())
    except requests.RequestException as e:
        logging.warning(f"Error fetching random number: {e}. Using local random.")
        return __import__('random').random()

def find_words_with_sealing(data: str, target_words: List[str], sealed_file: str) -> int:
    """Find target words in data, writing results to a sealed file."""
    with open(sealed_file, 'w') as sf:
        for word in target_words:
            if word in data:
                sf.write(f"{word}\n")

    with open(sealed_file, 'r') as sf:
        return sum(1 for _ in sf)

def find_words_in_memory(data: str, target_words: List[str]) -> int:
    """Find target words in data, keeping results in memory."""
    return sum(word in data for word in target_words)

def process_input(input_file: str, config: Dict[str, Any], find_words: Callable) -> Dict[str, Any]:
    """Process a single input file and generate the proof result."""
    with open(input_file, 'r') as f:
        input_data = json.load(f).get('data', '')

    found_count = find_words(input_data, config['expected_words'])
    random_value = fetch_random_number()
    is_valid = (found_count == len(config['expected_words']) and
                random_value >= config['random_threshold'])

    logging.info(f"File: {os.path.basename(input_file)}")
    logging.info(f"  Words found: {found_count}/{len(config['expected_words'])}")
    logging.info(f"  Random value: {random_value:.2f} (threshold: {config['random_threshold']})")
    logging.info(f"  Valid contribution: {'Yes' if is_valid else 'No'}")

    return {
        "valid_contribution": is_valid,
        "random_value": random_value,
        "found_keywords": found_count,
        "threshold": config['random_threshold']
    }

def generate_proof() -> None:
    """Generate proofs for all input files."""
    logging.info("Starting proof generation")
    config = load_config()
    use_sealing = os.path.isdir(SEALED_DIR)
    logging.info(f"Using sealed storage: {'Yes' if use_sealing else 'No'}")

    for input_filename in os.listdir(INPUT_DIR):
        input_path = os.path.join(INPUT_DIR, input_filename)
        output_path = os.path.join(OUTPUT_DIR, f"{input_filename}_result.json")

        if use_sealing:
            sealed_file = os.path.join(SEALED_DIR, f'{input_filename}_sealed.txt')
            find_words = lambda data, target_words: find_words_with_sealing(data, target_words, sealed_file)
        else:
            find_words = find_words_in_memory

        result = process_input(input_path, config, find_words)

        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)

    logging.info(f"Proof generation complete. Results in {OUTPUT_DIR}")

if __name__ == "__main__":
    generate_proof()