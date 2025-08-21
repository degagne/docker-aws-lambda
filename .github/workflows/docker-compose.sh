#!/usr/bin/env sh
# This script builds the Docker images using docker compose with the specified options.

docker compose --project-directory 3.10 --env-file base.env build --no-cache --provenance true --sbom true --push
docker compose --project-directory 3.11 --env-file base.env build --no-cache --provenance true --sbom true --push
docker compose --project-directory 3.12 --env-file base.env build --no-cache --provenance true --sbom true --push
docker compose --project-directory 3.13 --env-file base.env build --no-cache --provenance true --sbom true --push
