# Amazon Web Services (AWS) Lambda Images for Python

[![Docker Build and Push](https://github.com/degagne/docker-aws-lambda/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/degagne/docker-aws-lambda/actions/workflows/docker-ci.yml)

[![Dependency Vulnerabilities](https://img.shields.io/endpoint?url=https%3A%2F%2Fapi-hooks.soos.io%2Fapi%2Fshieldsio-badges%3FbadgeType%3DDependencyVulnerabilities%26pid%3D8y87rihef%26)](https://app.soos.io/research/repositories/github/degagne/docker-aws-lambda?attributionFormat=soosissues) [![Out Of Date Dependencies](https://img.shields.io/endpoint?url=https%3A%2F%2Fapi-hooks.soos.io%2Fapi%2Fshieldsio-badges%3FbadgeType%3DOutOfDateDependencies%26pid%3D8y87rihef%26)](https://app.soos.io/research/repositories/github/degagne/docker-aws-lambda?attributionFormat=soosissues)

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

### Variants

The base images are built on Alpine Linux and support multiple Python versions. Additionally, by default, these
images include third-party libraries for database connectivity.

The following libraries are included:

- `PyMySQL` for MySQL
- `psycopg2-binary` for PostgreSQL
- `oracledb` for Oracle

Moreover, there are 'slim' variants available for each Python version, which are optimized for smaller image sizes
and do not include these third-party libraries. These slim images are suitable for applications that do not require
database connectivity.

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
docker compose --project-directory 3.13 --env-file base.env --no-cache build
```

## Generating the AWS Lambda Image

To generate an AWS Lambda image, you can create a Dockerfile in the desired directory. For example, to create an 
image for Python 3.13 on Alpine 3.22, you can use the following `Dockerfile`:

```dockerfile
FROM python-alpine AS final-image

# Set build arguments for Lambda user, group, and task root
ARG LAMBDA_USER
ARG LAMBDA_GROUP
ARG LAMBDA_TASK_ROOT

# Change to a non-root user for security
USER ${LAMBDA_USER}

# Create the Lambda task root directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the function code and requirements file for Python dependencies
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install Python dependencies
RUN pip install --target ${LAMBDA_TASK_ROOT} --requirement requirements.txt --upgrade

# Set the entrypoint for the Lambda function
ENTRYPOINT ["/var/task/lambda-entrypoint.sh"]

# Set the command to run the Lambda function handler
CMD ["lambda_function.lambda_handler"]
```

For issues with custom ca certificates, you can add the following lines to your Dockerfile prior to the final-image stage:

```dockerfile
# ------------------- Stage 1: Build Stage -------------------
FROM ddegagne/aws-lambda:3.13-alpine3.22 AS python-alpine

# Switch to root user to install certificates
USER root

# Download CA certificate and add it to the trusted certificates
ADD https://artifactory.example.com/artifactory/dcs-container-release-local/CA-Certs/ca-certificate.crt \
    /usr/local/share/ca-certificates/ca-certificates.crt

# Update the CA certificates
RUN update-ca-certificates
```

### Building the Image

To build the Docker image, use the following command:

```bash
docker build \
  --build-arg LAMBDA_TASK_ROOT=/var/task \
  --build-arg LAMBDA_USER=lambda-user \
  --build-arg LAMBDA_GROUP=lambda-group \
  -f Dockerfile \
  -t aws_docker_test/python3.13:local .
```

### Running the Image

To run the built Docker image, use the following command:

```bash
docker run -p 9000:8080 aws_docker_test/python3.13:local
```

### Testing the Lambda Function

You can test the Lambda function locally using the AWS Lambda Runtime Interface Emulator. Send a POST request to the endpoint:

```powershell
Invoke-WebRequest -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Method Post -ContentType "application/json" -Body '{}'
```

This should return a response from your Lambda function, indicating that it is working correctly.

```powershell
# Example response
StatusCode        : 200
StatusDescription : OK
Content           : {"statusCode": 200, "body": "Hello from Lambda! nice_shtern"}
RawContent        : HTTP/1.1 200 OK
                    Content-Length: 61
                    Content-Type: text/plain; charset=utf-8
                    Date: Thu, 21 Aug 2025 14:28:06 GMT

                    {"statusCode": 200, "body": "Hello from Lambda! nice_shtern"}
Forms             : {}
Headers           : {[Content-Length, 61], [Content-Type, text/plain; charset=utf-8], [Date, Thu, 21 Aug 2025 14:28:06 GMT]}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 61
```
