#!/usr/bin/python3
"""
Small Python script to extract each certificate from a PEM file, and saving them
into individual files.
"""
import logging
import pathlib
import re


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Specify the input ca bundle file and output directory
output_path: pathlib.Path = pathlib.Path("/usr/local/share/ca-certificates")
certs_file: pathlib.Path = output_path.joinpath("ca-certificates.crt")

# Ensure the output directory exists
output_path.mkdir(parents=True, exist_ok=True)

# Compile regex patterns for matching certificates and labels
cert_pattern = re.compile(r'(-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----)', re.DOTALL)
label_pattern = re.compile(r'# Label: "(.*?)"')

if not certs_file.exists():
    logger.info("No ca-certificates.crt file found, skipping extraction.")
    exit(0)

# Read the content of the ca-certificates.crt file
content = certs_file.read_text()

# Find all certificates
certificates = cert_pattern.findall(content)

for index, cert in enumerate(certificates, start=1):
    # Extract the label if available
    label_match = label_pattern.search(content, content.find(cert))
    label = label_match.group(1).replace(" ", "_") if label_match else f"cert-{index}"

    # Create a filename based on the label
    filename = output_path.joinpath(f"{label}.pem")

    # Write the certificate to a file
    with filename.open('w') as cert_file:
        cert_file.write(cert.strip())

    logger.info(f"Extracted certificate {index} to {filename}")

logger.info("All certificates have been extracted successfully.")
