# Amazon Web Services (AWS) Lambda Images for Python

This project provides Docker images for running Python-based AWS Lambda functions. It includes Dockerfiles
and a docker-compose.yaml configuration to build and manage containerized environments for AWS Lambda using
Python 3.10+. The project supports both standard and slim versions of the images, based on Alpine Linux, to 
ensure lightweight and efficient containers.

## Key Features:
- **Python 3.10+ Runtime**: The images are tailored for AWS Lambda functions using Python 3.10+.
- **Alpine Linux Base**: Utilizes Alpine Linux for minimal image size and security.
- **Custom CA Certificates**: Supports adding custom CA certificates for secure communication.
- **Lambda Runtime Interface Emulator**: Includes the AWS Lambda Runtime Interface Emulator for local testing.
- **Multi-Stage Builds**: Uses multi-stage Docker builds to optimize image size and dependencies.
- **Non-Root User**: Runs the container as a non-root user for enhanced security.
- **Docker Compose Support**: Provides a docker-compose.yaml file for easy setup and management of services.

## Tagging

The Docker images are tagged with the following format:

```
<image_name>-<python_version>alpine<distro_version>-<variant>
```

**Where**:
- `<image_name>`: The name of the image (e.g., `aws-lambda`).
- `<python_version>`: The version of Python (e.g., `3.10`, `3.11`).
- `<distro_version>`: The version of the Alpine Linux distribution (e.g., `3.22`, `3.23`).
- `<variant>`: The variant of the image (e.g., `slim`, `standard`).

**Examples**:

- `aws-lambda-3.10-alpine3.22-slim`
- `aws-lambda-3.11-alpine3.22`
- `aws-lambda-3.13-alpine3.21`

### Supported Tags and `Dockerfile` Links

- Python Runtime: 3.13
  - [`3.13-alpine3.20`](3.13/Dockerfile)
  - [`3.13-alpine3.20-slim`](3.13/Dockerfile.slim)
  - [`3.13-alpine3.21`](3.13/Dockerfile)
  - [`3.13-alpine3.21-slim`](3.13/Dockerfile.slim)
  - [`3.13-alpine3.22`](3.13/Dockerfile)
  - [`3.13-alpine3.22-slim`](3.13/Dockerfile.slim)
- Python Runtime: 3.12
  - [`3.12-alpine3.20`](3.12/Dockerfile)
  - [`3.12-alpine3.20-slim`](3.12/Dockerfile.slim)
  - [`3.12-alpine3.21`](3.12/Dockerfile)
  - [`3.12-alpine3.21-slim`](3.12/Dockerfile.slim)
  - [`3.12-alpine3.22`](3.12/Dockerfile)
  - [`3.12-alpine3.22-slim`](3.12/Dockerfile.slim) 
- Python Runtime: 3.11
  - [`3.11-alpine3.20`](3.11/Dockerfile)
  - [`3.11-alpine3.20-slim`](3.11/Dockerfile.slim)
  - [`3.11-alpine3.21`](3.11/Dockerfile)
  - [`3.11-alpine3.21-slim`](3.11/Dockerfile.slim)
  - [`3.11-alpine3.22`](3.11/Dockerfile)
  - [`3.11-alpine3.22-slim`](3.11/Dockerfile.slim)
- Python Runtime: 3.10
  - [`3.10-alpine3.20`](3.10/Dockerfile)
  - [`3.10-alpine3.20-slim`](3.10/Dockerfile.slim)
  - [`3.10-alpine3.21`](3.10/Dockerfile)
  - [`3.10-alpine3.21-slim`](3.10/Dockerfile.slim)
  - [`3.10-alpine3.22`](3.10/Dockerfile)
  - [`3.10-alpine3.22-slim`](3.10/Dockerfile.slim)

## Usage

To use these Docker images, you can build them using the provided Dockerfiles or pull them from a Docker
registry if available.

### Building the Images

To build the images, navigate to the directory containing the Dockerfile and run:

```bash
docker build -t <image_name>:<tag> .
```

Docker compose can also be used to build all images at once. Ensure you have the `docker-compose.yaml` file in
the root directory, then run:

```bash 
docker compose --project-directory 3.13 --env_file base.env --no-cache build
```

### Running the Images

To run the images, you can use Docker Compose with the provided `docker-compose.yaml` file. First, ensure you have Docker Compose installed, then run:

```bash
docker-compose up
```

## Deployment of AWS Lambda Functions
