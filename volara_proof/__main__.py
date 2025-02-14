import json
import logging
import os
import sys
import traceback
from typing import Dict, Any

from volara_proof.proof import Proof
from volara_proof.constants import VOLARA_DLP_OWNER_ADDRESS, VOLARA_DLP_OWNER_PUBLIC_KEY_HEX

INPUT_DIR, OUTPUT_DIR = "/input", "/output"

logging.basicConfig(level=logging.INFO, format="%(message)s")


def load_config() -> Dict[str, Any]:
    """Load proof configuration from environment variables."""
    config = {
        "dlp_id": 6,
        "input_dir": INPUT_DIR,
        "cookies": os.environ.get("COOKIES", None),
        "volara_api_key": os.environ.get("VOLARA_API_KEY", None),
        "file_id": os.environ.get("FILE_ID", None),
        "miner_address": os.environ.get("MINER_ADDRESS", None),
    }
    return config

def assess_validity(validated_permissions) -> bool:
    """Assess the validity of a validated permission."""
    for permission in validated_permissions:
        if permission["address"] == VOLARA_DLP_OWNER_ADDRESS and permission["public_key"] == VOLARA_DLP_OWNER_PUBLIC_KEY_HEX:
            return True
    return False


def run() -> None:
    """Generate proofs for all input files."""
    config = load_config()
    input_files_exist = os.path.isdir(INPUT_DIR) and bool(os.listdir(INPUT_DIR))
    validated_permissions_str = os.environ.get("VALIDATED_PERMISSIONS", None)
    if validated_permissions_str is None:
        raise ValueError("VALIDATED_PERMISSIONS environment variable is not set")

    validated_permissions = json.loads(validated_permissions_str)
    if not assess_validity(validated_permissions):
        raise ValueError("Permissions failed to validate")

    if not input_files_exist:
        raise FileNotFoundError(f"No input files found in {INPUT_DIR}")

    proof = Proof(config)
    proof_response = proof.generate()

    output_path = os.path.join(OUTPUT_DIR, "results.json")
    with open(output_path, "w") as f:
        json.dump(proof_response.dict(), f, indent=2)
    logging.info(f"Proof generation complete: {proof_response}")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logging.error(f"Error during proof generation: {e}")
        traceback.print_exc()
        sys.exit(1)
