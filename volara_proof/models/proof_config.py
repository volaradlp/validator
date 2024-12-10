from dataclasses import dataclass


@dataclass
class ProofConfig:
    input_dir: str
    cookies: str
    dlp_id: int
    volara_api_key: str
    file_id: str
    miner_address: str
