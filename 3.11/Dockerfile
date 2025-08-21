ARG DISTRO_VERSION

# ------------------- Stage 1: Pre-build Stage -------------------
FROM public.ecr.aws/docker/library/python:3.11-alpine${DISTRO_VERSION} AS python-alpine

# Include global args for the pre-build stage
ARG CA_CERTIFICATE
ARG LAMBDA_RUNTIME_INTERFACE_EMULATOR

# Download the ca certificate and the runtime interface emulator into the container
ADD ${CA_CERTIFICATE} /usr/local/share/ca-certificates/Custom-CA-Bundle
ADD ${LAMBDA_RUNTIME_INTERFACE_EMULATOR} /usr/local/bin/aws-lambda-rie

# Add Python script to extract certificates into individual files.
COPY extract-certs-bundle.py /usr/local/bin/extract-certs-bundle

# Register the new CA certificates bundle
RUN chmod +x /usr/local/bin/extract-certs-bundle \
    && python3 /usr/local/bin/extract-certs-bundle \
    && rm -f /usr/local/share/ca-certificates/ca-certificates.crt \
    && update-ca-certificates

# Install required packages and dependencies
RUN apk add --no-cache \
        binutils \
        libstdc++

# ------------------- Stage 2: Build Stage -------------------
FROM python-alpine AS build-image

# Install required build tools and dependencies
RUN apk add --no-cache \
      autoconf \
      automake \
      bmake \
      build-base \
      cmake \
      elfutils-dev \
      libcurl \
      libtool

# Include global args for the build stage
ARG LAMBDA_TASK_ROOT
ARG LAMBDA_RUNTIME_INTERFACE

# Download the Python runtime client into the container
ADD ${LAMBDA_RUNTIME_INTERFACE} ${LAMBDA_TASK_ROOT}/awslambdaric.tar.gz

# Create the /var/task directory
RUN mkdir -p ${LAMBDA_TASK_ROOT}

# Create a symlink for bmake to override the default make command (bmake is used in Alpine Linux)
RUN ln -s -f /usr/bin/bmake /usr/bin/make

# Copy the deps directory contents into the /var/task directory
COPY deps/ ${LAMBDA_TASK_ROOT}

# Create a symlink for the pip configuration file for global use
RUN ln -s ${LAMBDA_TASK_ROOT}/pip.conf /etc/pip.conf

# Regenerate the CA certificates to include the custom certificate
RUN update-ca-certificates

# Upgrade and/or install Python dependencies to the /var/task directory
RUN pip install --upgrade pip && \
    pip install --target ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}/awslambdaric.tar.gz && \
    pip install --target ${LAMBDA_TASK_ROOT} --requirement ${LAMBDA_TASK_ROOT}/requirements.txt

# Perform cleanup by removing unnecessary files to reduce the image size
RUN rm -rf ${LAMBDA_TASK_ROOT}/awslambdaric.tar.gz && \
    rm -rf ${LAMBDA_TASK_ROOT}/requirements.txt

# ------------------- Stage 3: Final Stage -------------------
FROM python-alpine

# Set the base image metadata
LABEL "org.opencontainers.image.version"="1.0"
LABEL "org.opencontainers.image.description"="Dockerfile for Amazon Web Services (AWS) on Lambda with Python 3.11"
LABEL "org.opencontainers.image.authors"="Deric Degagne <deric.degagne@gmail.com>"
LABEL "org.opencontainers.image.source"="https://github.com/degagne/docker-aws-lambda"
LABEL "org.opencontainers.image.licenses"="GNU General Public License v3.0"
LABEL "org.opencontainers.image.url"="https://hub.docker.com/r/ddegagne/aws-cli"

# Include global args for the final stage
ARG LAMBDA_USER
ARG LAMBDA_GROUP
ARG LAMBDA_TASK_ROOT

# Change the current working directory to the Lambda task root
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the entrypoint script into the container and /var/task directory
COPY --from=build-image ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}
COPY --from=python-alpine /usr/local/bin/aws-lambda-rie /usr/local/bin/aws-lambda-rie

# Create a symlink for the pip configuration file for global use
RUN ln -s ${LAMBDA_TASK_ROOT}/pip.conf /etc/pip.conf

# Regenerate the CA certificates to include the custom certificate
RUN update-ca-certificates

# Upgrade pip and setuptools, and clean up Python bytecode files
RUN pip install --upgrade pip setuptools && \
    find ${LAMBDA_TASK_ROOT} -type f -name "*.pyc" -delete && \
    find ${LAMBDA_TASK_ROOT} -type d -name "__pycache__" -delete

# Create a non-root user and group
RUN addgroup -S ${LAMBDA_GROUP} && adduser -S -G ${LAMBDA_GROUP} ${LAMBDA_USER}

# Set the ownership and permissions for the required directories and files
RUN chown -R ${LAMBDA_USER}:${LAMBDA_GROUP} ${LAMBDA_TASK_ROOT} && \
    chmod -R 755 ${LAMBDA_TASK_ROOT}/lambda-entrypoint.sh && \
    chmod -R 755 /usr/local/bin/aws-lambda-rie

# Switch to the non-root user
USER ${LAMBDA_USER}

ENTRYPOINT ["/lambda-entrypoint.sh"]

CMD ["lambda_function.lambda_handler"]
