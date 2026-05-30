FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# Add the netdevops repository
RUN echo "deb [trusted=yes] https://netdevops.fury.site/apt/ /" | \
    tee -a /etc/apt/sources.list.d/netdevops.list

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    btop \
    iputils-ping \
    tcpdump \
    iproute2 \
    dnsutils \
    telnet \
    curl \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install ContainerLab
RUN bash -c "$(curl -sL https://get.containerlab.dev)"

# Install gNMIc (needed for telemetry and SR Linux config push)
RUN bash -c "$(curl -sL https://get-gnmic.openconfig.net)"

# Install GitHub CLI
RUN bash -c 'ARCH=$(uname -m | sed "s/x86_64/amd64/" | sed "s/aarch64/arm64/") && \
    VERSION=$(curl -s https://api.github.com/repos/cli/cli/releases/latest | \
    grep -oP "\"tag_name\": \"\K[^\"]+") && \
    CLEAN_VERSION=${VERSION#v} && \
    DOWNLOAD_URL="https://github.com/cli/cli/releases/download/${VERSION}/gh_${CLEAN_VERSION}_linux_${ARCH}.tar.gz" && \
    curl -L "$DOWNLOAD_URL" | tar xz -C /tmp && \
    mv /tmp/gh_${CLEAN_VERSION}_linux_${ARCH}/bin/gh /usr/local/bin/ && \
    chmod +x /usr/local/bin/gh && \
    rm -rf /tmp/gh_${CLEAN_VERSION}_linux_${ARCH}'

# Add empty docker config to avoid clab warnings for root
RUN mkdir -p /root/.docker && echo "{}" > /root/.docker/config.json

# Allow sudo without password for SSH_AUTH_SOCK
RUN mkdir -p /etc/sudoers.d && echo 'Defaults env_keep += "SSH_AUTH_SOCK"' > /etc/sudoers.d/ssh_auth_sock

# Add vscode user to clab_admins group (created by clab installer)
RUN usermod -aG clab_admins vscode

# Switch to vscode user
USER vscode

# Create SSH key for passwordless SSH to lab devices
RUN ssh-keygen -t ecdsa -b 256 -N "" -f ~/.ssh/id_ecdsa

# Add empty docker config for vscode user
RUN mkdir -p /home/vscode/.docker && echo "{}" > /home/vscode/.docker/config.json
