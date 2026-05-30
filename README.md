[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/AiAZ2rSd)
# AAR - Administração Automatizada de Redes

Final project for the Network Automation course (AAR) at ISEL-DEETC.

## Quick Start

### Option 1: GitHub Codespaces (recommended)

Click the button below to launch a fully configured environment in the cloud:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/isel-aar/aar-project-template?quickstart=1)

The environment will automatically:
- Install ContainerLab, gNMIc, Ansible and all required tools
- Pull the router images (Arista cEOS, Nokia SR Linux, Mikrotik CHR)
- Create a Python virtual environment with all dependencies

After the setup completes, activate the virtual environment and deploy the lab:

```bash
source .venv/bin/activate
sudo containerlab deploy -t topology/aar-lab.yml
```

> **Important:** Stop your Codespace when you're not using it to conserve hours.
> The idle timeout is set to 30 minutes, but it's good practice to stop it manually
> via the Codespaces dashboard.

### Option 2: Local VM

Follow the instructions in the project specification document to set up a local
Ubuntu Server VM with ContainerLab.

## Topology

The lab consists of 4 routers and 4 hosts:

| Device | Kind | Location | OSPF Area |
|--------|------|----------|-----------|
| r1     | Arista cEOS | Lisboa | 1 |
| r2     | Arista cEOS | Porto  | 2 |
| r3     | Nokia SR Linux | Faro | 3 |
| r4     | Mikrotik CHR | Braga | 4 |

## Repository Structure

```
├── .devcontainer/          # Codespaces / devcontainer configuration
├── topology/               # ContainerLab topology files (prod + twin)
├── part1/                  # Python scripts (Netmiko, NAPALM)
│   ├── scripts/
│   └── templates/
├── ansible/                # Ansible automation (Part 2)
│   ├── inventory/
│   ├── playbooks/
│   ├── roles/
│   └── group_vars/
├── telemetry/              # Streaming telemetry stack (Part 3)
├── scripts/                # Shared utility scripts
├── tests/                  # Validation scripts
├── data/                   # devices.csv, shared variables
├── .github/workflows/      # CI/CD pipeline (Part 4)
├── requirements.txt
└── .yamllint
```

## Useful Commands

```bash
# Deploy the lab
sudo containerlab deploy -t topology/aar-lab.yml

# Check lab status
sudo containerlab inspect -t topology/aar-lab.yml

# Destroy the lab
sudo containerlab destroy -t topology/aar-lab.yml

# SSH to a router
ssh admin@clab-aar-lab-r1    # Arista cEOS
ssh admin@clab-aar-lab-r3    # Nokia SR Linux
ssh admin@clab-aar-lab-r4    # Mikrotik CHR
```
