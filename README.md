# Volara Satya Proof of Contribution

This repository provides proof of contribution using Satya validators for the Volara dataset on the Vana network.

## Overview

This template provides a basic structure for building proof tasks that:

1. Read input files from the `/input` directory.
2. Process the data securely, running any necessary validations to prove the data authentic, unique, high quality, etc.
3. Write proof results to the `/output/results.json` file in the following format:

```json
{
  "dlp_id": 19,
  "valid": true,
  "score": 0.85,
  "authenticity": 1.0,
  "ownership": 1.0,
  "quality": 0.9,
  "uniqueness": 0.8,
  "attributes": {
    "email_verified": true,
    "total_score": 0.75,
    "score_threshold": 0.83
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

##Getting Started
To begin using this project:
1. Fork the repository:
Make a copy of this repository in your GitHub account.
2. Clone the repository:

``git clone https://github.com/volaradlp/validator.git
cd validator``
3. Build the Docker image:

``docker build -t volara-validator .``
4. Run the proof task:

```docker run --rm \
  --volume $(pwd)/input:/input \
  --volume $(pwd)/output:/output \
  --env USER_EMAIL=user@example.com \
  volara-validator```
## Customizing the Proof Logic

The main proof logic is implemented in `my_proof/proof.py`. To customize it, update the `Proof.generate()` function to change how input files are processed.

The proof can be configured using environment variables:

- `USER_EMAIL`: The email address of the data contributor, to verify data ownership

If you want to use a language other than Python, you can modify the Dockerfile to install the necessary dependencies and build the proof task in the desired language.

## Running with Intel TDX

Intel TDX (Trust Domain Extensions) provides hardware-based memory encryption and integrity protection for virtual machines. To run this container in a TDX-enabled environment, follow your infrastructure provider's specific instructions for deploying confidential containers.

Common volume mounts and environment variables:

```docker run --rm \
  --volume /path/to/input:/input \
  --volume /path/to/output:/output \
  --env USER_EMAIL=user@example.com \
  volara-validator
```

Remember to populate the `/input` directory with the files you want to process.

## Security Features

This template leverages several security features:

1. **Hardware-based Isolation**: The proof runs inside a TDX-protected environment, isolating it from the rest of the system
2. **Input/Output Isolation**: Input and output directories are mounted separately, ensuring clear data flow boundaries
3. **Minimal Container**: Uses a minimal Python base image to reduce attack surface

## Development and testinng
Local Testing: Run proof logic locally for development:

```python -m unittest discover```
2. Linting and Code Style: Use tools like flake8 or black to ensure code consistency:

```pip install flake8 black
black my_proof/```
## Contributing

If you have suggestions for improving this template, please open an issue or submit a pull request.
my suggestion and contribution


## License

[MIT License](LICENSE)

