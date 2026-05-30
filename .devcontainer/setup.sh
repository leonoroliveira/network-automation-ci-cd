#!/bin/bash
set -e

echo "=== AAR Lab Environment Setup ==="

# ---------------------------------------------------------------
# 1. Authenticate to the organisation's GitHub Container Registry
#    to pull the proprietary router images (Arista cEOS, Mikrotik CHR).
#    Inside Codespaces, GITHUB_TOKEN is injected automatically and
#    has read:packages scope for the organisation that owns the repo.
# ---------------------------------------------------------------
if [ -n "$GITHUB_TOKEN" ]; then
    echo ">> Authenticating to ghcr.io ..."
    echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USER" --password-stdin 2>/dev/null \
        || echo "$GITHUB_TOKEN" | docker login ghcr.io -u "codespace" --password-stdin 2>/dev/null \
        || echo "WARNING: Could not authenticate to ghcr.io. You may need to pull images manually."
else
    echo "WARNING: GITHUB_TOKEN not found."
    echo "  If running locally, authenticate manually:"
    echo "    echo \$PAT | docker login ghcr.io -u YOUR_USERNAME --password-stdin"
fi

# ---------------------------------------------------------------
# 2. Pull router images
#    Nokia SR Linux is public. Arista cEOS and Mikrotik CHR are
#    private packages in the organisation's ghcr.io registry.
#
#    IMPORTANT: Update the image tags below to match the versions
#    you have pushed to your organisation's registry.
# ---------------------------------------------------------------
echo ">> Pulling router images ..."

# Nokia SR Linux (public)
docker pull ghcr.io/nokia/srlinux:latest
docker tag ghcr.io/nokia/srlinux:latest srlinux:latest

# Arista cEOS (private - from organisation registry)
# TODO: Replace 'isel-aar' with your actual GitHub organisation name
# TODO: Replace the tag with the version you uploaded
if docker pull ghcr.io/isel-aar/ceos:4.35.2F 2>/dev/null; then
    docker tag ghcr.io/isel-aar/ceos:4.35.2F ceos:latest
    echo "  cEOS image pulled successfully."
else
    echo "WARNING: Could not pull cEOS image from ghcr.io/isel-aar/ceos:4.35.2F"
    echo "  Check that the image exists and you have access to the organisation."
fi

# Mikrotik CHR via vrnetlab (private - from organisation registry)
# TODO: Replace the tag with the version you uploaded
if docker pull ghcr.io/isel-aar/mikrotik_ros:7.20.8 2>/dev/null; then
    docker tag ghcr.io/isel-aar/mikrotik_ros:7.20.8 mikrotik_ros:latest
    echo "  Mikrotik image pulled successfully."
else
    echo "WARNING: Could not pull Mikrotik image from ghcr.io/isel-aar/mikrotik_ros:7.20.8"
    echo "  Check that the image exists and you have access to the organisation."
fi

# ---------------------------------------------------------------
# 3. Python virtual environment and dependencies
# ---------------------------------------------------------------
echo ">> Setting up Python environment ..."
cd /clab
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo ""
echo "=== Setup complete ==="
echo ""
echo "To activate the Python virtual environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To deploy the lab topology:"
echo "  sudo containerlab deploy -t topology/aar-lab.yml"
echo ""
echo "To destroy the lab:"
echo "  sudo containerlab destroy -t topology/aar-lab.yml"
echo ""
