# Vana Satya Proof of Contribution Python Template

This repository serves as a template for creating proof tasks using Python and Gramine for secure computation.

## Overview

This template provides a basic structure for building proof tasks that:

1. Read input files from the `/input` directory
2. Process the data securely
3. Write proof results to the `/output` directory
4. Use the `/sealed` directory for secure storage (when available)

The project is designed to work with Gramine, a lightweight library OS that enables running unmodified applications in secure enclaves, such as Intel SGX (Software Guard Extensions). This allows the code to run in a trusted execution environment, ensuring confidentiality and integrity of the computation.

## Project Structure

- `my_proof/`: Contains the main proof logic
  - `proof.py`: Implements the proof generation logic
  - `__main__.py`: Entry point for the proof execution
- `demo/`: Contains sample input and output for testing
- `.github/workflows/`: CI/CD pipeline for building and releasing
- `Dockerfile`: Defines the container image for the proof task
- `python.manifest.template`: Gramine manifest template for secure execution
- `config.yaml`: Configuration file for Gramine Shielded Containers (GSC)

## Getting Started

To use this template:

1. Fork this repository
2. Modify the `my_proof/proof.py` file to implement your specific proof logic
3. Update the `python.manifest.template` if you need to add any additional files or change the configuration
4. Commit your changes and push to your repository

## Customizing the Proof Logic

The main proof logic is implemented in `my_proof/proof.py`. To customize it:

1. Modify the `expected_words` list to include the keywords you're looking for
2. Adjust the `process_on_disk` and `process_in_memory` functions to implement your specific proof generation logic
3. Update the `generate_proof` function if you need to change how input files are processed or results are written

## Local Development

To run the proof locally, without Gramine, you can use Docker:

```
docker build -t my-proof .
docker run \
--rm \
--volume $(pwd)/demo/sealed:/sealed \
--volume $(pwd)/demo/input:/input \
--volume $(pwd)/demo/output:/output \
my-proof
```

## Generating the Gramine Signing Key

Before building and signing your graminized Docker image, you need to generate a signing key. Gramine provides a tool called `gramine-sgx-gen-private-key` for this purpose. Here's how to use it:

1. If you have Gramine installed on your system, you can use the following command:

   ```
   gramine-sgx-gen-private-key enclave-key.pem
   ```

   This will generate a new RSA 3072 key suitable for signing SGX enclaves and save it as `enclave-key.pem` in the current directory.

2. If you don't have Gramine installed, you can use OpenSSL to generate a compatible key:

   ```
   openssl genrsa -3 -out enclave-key.pem 3072
   ```

   This generates an RSA 3072-bit key with the public exponent set to 3, which is required for SGX enclaves.

Make sure to keep this key secure, as it will be used to sign your enclaves. You'll use this key in the `gsc sign-image` step of the GSC workflow.

## Building and Releasing

This template includes a GitHub Actions workflow that automatically:

1. Builds a Docker image with your code
2. Creates a Gramine-shielded container (GSC) image
3. Publishes the GSC image as a GitHub release

To use this workflow, you need to:

1. Set up a signing key, as described above, and add it as a GitHub secret named `SIGNING_KEY`
2. Push your changes to the `main` branch or create a pull request

## Running with SGX

Intel SGX (Software Guard Extensions) is a set of security-related instruction codes built into modern Intel CPUs. It allows parts of a program to be executed in a secure enclave, isolated from the rest of the system.

To load a released image with docker, copy the URL from the release and run:

```
curl -L https://address/of/gsc-my-proof.tar.gz | docker load
```

To run the image:

```
docker run \
--rm \
--volume /gsc-my-proof/input:/input \
--volume /gsc-my-proof/output:/output \
--device /dev/sgx_enclave:/dev/sgx_enclave \
--volume /var/run/aesmd:/var/run/aesmd \
--volume /mnt/gsc-my-proof/sealed:/sealed \
gsc-my-proof
```

Remember to populate the `/input` directory with the files you want to process.

## Security Features

This template leverages several security features:

1. **Secure Enclaves**: The proof runs inside an SGX enclave, isolating it from the rest of the system.
2. **Encrypted Storage**: The `/sealed` directory is automatically encrypted/decrypted by Gramine, providing secure storage for sensitive data.
3. **Input/Output Isolation**: Input and output directories are mounted separately, ensuring clear data flow boundaries.
4. **Minimal Attack Surface**: The Gramine manifest limits the files and resources accessible to the enclave, reducing potential vulnerabilities.

## Customization

Feel free to modify any part of this template to fit your specific needs. The goal is to provide a starting point that can be easily adapted to various proof tasks.

## Contributing

If you have suggestions for improving this template, please open an issue or submit a pull request.

## License

[MIT License](LICENSE)