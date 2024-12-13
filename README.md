# Volara Satya Proof of Contribution

This repository provides proof of contribution using Satya validators for the Volara dataset on the Vana network.

## Overview

This template provides a basic structure for building proof tasks that:

1. Read input files from the `/input` directory.
2. Process the data securely, running any necessary validations to prove the data authentic, unique, high quality, etc.
3. Write proof results to the `/output/results.json` file in the following format:

```json
{
  "dlp_id": 19, // DLP ID is found in the Root Network contract after the DLP is registered
  "valid": false, // A single boolean to summarize if the file is considered valid in this DLP
  "score": 0.7614457831325301, // A score between 0 and 1 for the file, used to determine how valuable the file is. This can be an aggregation of the individual scores below.
  "authenticity": 1.0, // A score between 0 and 1 to rate if the file has been tampered with
  "ownership": 1.0, // A score between 0 and 1 to verify the ownership of the file
  "quality": 0.6024096385542169, // A score between 0 and 1 to show the quality of the file
  "uniqueness": 0, // A score between 0 and 1 to show unique the file is, compared to others in the DLP
  "attributes": {
    // Custom attributes that can be added to the proof to provide extra context about the encrypted file
    "total_score": 0.5,
    "score_threshold": 0.83,
    "email_verified": true
  }
}
```

The project is designed to work with Intel TDX (Trust Domain Extensions), providing hardware-level isolation and security guarantees for confidential computing workloads.

## Project Structure

- `my_proof/`: Contains the main proof logic
  - `proof.py`: Implements the proof generation logic
  - `__main__.py`: Entry point for the proof execution
  - `models/`: Data models for the proof system
- `demo/`: Contains sample input and output for testing
- `Dockerfile`: Defines the container image for the proof task
- `requirements.txt`: Python package dependencies

## Getting Started

To use this template:

1. Fork this repository
2. Modify the `my_proof/proof.py` file to implement your specific proof logic
3. Update the project dependencies in `requirements.txt` if needed
4. Commit your changes and push to your repository

## Customizing the Proof Logic

The main proof logic is implemented in `my_proof/proof.py`. To customize it, update the `Proof.generate()` function to change how input files are processed.

The proof can be configured using environment variables:

- `USER_EMAIL`: The email address of the data contributor, to verify data ownership

If you want to use a language other than Python, you can modify the Dockerfile to install the necessary dependencies and build the proof task in the desired language.

## Local Development

To run the proof locally for testing, you can use Docker:

```bash
docker build -t my-proof .
docker run \
  --rm \
  --volume $(pwd)/input:/input \
  --volume $(pwd)/output:/output \
  --env USER_EMAIL=user123@gmail.com \
  my-proof
```

## Running with Intel TDX

Intel TDX (Trust Domain Extensions) provides hardware-based memory encryption and integrity protection for virtual machines. To run this container in a TDX-enabled environment, follow your infrastructure provider's specific instructions for deploying confidential containers.

Common volume mounts and environment variables:

```bash
docker run \
  --rm \
  --volume /path/to/input:/input \
  --volume /path/to/output:/output \
  --env USER_EMAIL=user123@gmail.com \
  my-proof
```

Remember to populate the `/input` directory with the files you want to process.

## Security Features

This template leverages several security features:

1. **Hardware-based Isolation**: The proof runs inside a TDX-protected environment, isolating it from the rest of the system
2. **Input/Output Isolation**: Input and output directories are mounted separately, ensuring clear data flow boundaries
3. **Minimal Container**: Uses a minimal Python base image to reduce attack surface

## Customization

Feel free to modify any part of this template to fit your specific needs. The goal is to provide a starting point that can be easily adapted to various proof tasks.

## Contributing

If you have suggestions for improving this template, please open an issue or submit a pull request.
my suggestion and contribution


## License

[MIT License](LICENSE)

