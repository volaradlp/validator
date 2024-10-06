import logging
import os
from typing import Dict, Any


from volara_proof.proofs.proof import proof
from volara_proof.models.proof_response import ProofResponse
from volara_proof.models.proof_config import ProofConfig


class Proof:
    def __init__(self, config: Dict[str, Any]):
        self.config = ProofConfig(**config)
        self.proof_response = ProofResponse(dlp_id=config["dlp_id"])

    def generate(self) -> ProofResponse:
        """Generate proofs for all input files."""
        logging.info("Starting proof generation")

        for input_filename in os.listdir(self.config.input_dir):
            input_file = os.path.join(self.config.input_dir, input_filename)
            break

        output_message = proof(input_file, self.proof_response, self.config)

        return output_message
