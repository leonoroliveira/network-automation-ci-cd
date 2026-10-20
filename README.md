# Network Automation & Orchestration

A multi-vendor network automation project developed as part of the Network Automation course at ISEL – Instituto Superior de Engenharia de Lisboa.

The project combines network configuration automation, infrastructure validation, streaming telemetry and CI/CD practices to simplify the deployment, testing and maintenance of a virtualized network environment.

## Overview

The lab simulates a multi-vendor network using Containerlab, with Arista cEOS, Nokia SR Linux and MikroTik RouterOS devices.

Automation is implemented using Python, Ansible and Jinja2 templates. A digital twin environment is used to validate network changes before applying configurations to the production lab.

The project also includes a CI/CD workflow that performs automated validation, deploys and tests the digital twin, and proceeds to production configuration when the required stages succeed.

## Key Features

- **Multi-vendor network automation** using Ansible, Python and Jinja2 templates.
- **Infrastructure as Code (IaC)** through reusable playbooks, roles, templates and YAML configuration files.
- **Automated validation** using `yamllint`, `ansible-lint` and Jinja2 template validation.
- **CI/CD pipeline** implemented with GitHub Actions.
- **Digital twin validation** to test network configurations before production deployment.
- **Network provisioning and configuration** for OSPF, NTP and DHCP.
- **Network troubleshooting** through automated checks and simulated failures.
- **Streaming telemetry and monitoring** using gNMIc, Prometheus and Grafana.

## Architecture

The virtualized lab contains four routers and four hosts connected through a multi-vendor topology.

| Device | Network OS | Site |
|---|---|---|
| R1 | Arista cEOS | Lisboa |
| R2 | Arista cEOS | Porto |
| R3 | Nokia SR Linux | Faro |
| R4 | MikroTik RouterOS | Braga |

Containerlab provides the virtualized network environment, while Ansible and Python automate configuration and validation tasks.

A separate digital twin topology mirrors the lab environment and supports testing before production deployment.

## CI/CD Workflow

The GitHub Actions workflow is organized into three stages.

### 1. Lint and Validation

- Checks out the repository.
- Validates YAML files using `yamllint`.
- Validates Jinja2 templates.
- Checks Ansible playbooks using `ansible-lint`.

### 2. Staging — Digital Twin

- Deploys the digital twin topology.
- Waits for network devices to initialize.
- Applies OSPF, NTP and DHCP configurations.
- Performs host-route adjustments.
- Executes network validation playbooks.
- Destroys the digital twin environment after the validation stage.

### 3. Production Deployment

After the previous stages succeed, the workflow applies the configuration to the production lab and runs additional validation tasks.

The workflow uses self-hosted GitHub Actions runners configured with the required network lab and dependencies.

## Network Telemetry

The project includes a telemetry stack built with:

- **gNMIc** — collects streaming telemetry from supported network devices.
- **Prometheus** — collects and stores metrics.
- **Grafana** — provides dashboards for network monitoring.

Docker Compose is used to manage the telemetry services.

## Technologies Used

- **Network Automation:** Ansible, Python, Jinja2
- **Networking:** TCP/IP, OSPF, DHCP, NTP, multi-vendor routing
- **Virtualization and Lab:** Containerlab, Docker
- **CI/CD and Version Control:** Git, GitHub, GitHub Actions
- **Validation:** yamllint, ansible-lint, Jinja2 validation
- **Telemetry and Monitoring:** gNMIc, Prometheus, Grafana
- **Network APIs and Libraries:** Netmiko, NAPALM, RESTCONF, gNMI

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── network-ci.yml
├── ansible/
│   ├── inventory/
│   ├── playbooks/
│   └── roles/
├── data/
├── part1/
│   ├── scripts/
│   ├── templates/
│   └── output/
├── scripts/
├── telemetry/
│   ├── docker-compose.yml
│   ├── gnmic.yml
│   ├── prometheus.yml
│   └── grafana/
├── tests/
├── topology/
│   ├── aar-lab.yml
│   └── aar-lab-twin.yml
├── requirements.txt
└── README.md
```

## Running the Lab

The project requires a Linux environment with Docker, Containerlab, Python and the required network device images.

1. Install and configure the required dependencies.
2. Prepare the Arista cEOS, Nokia SR Linux and MikroTik RouterOS images.
3. Create and activate a Python virtual environment.
4. Install the Python dependencies.
5. Deploy the production or digital twin topology using Containerlab.
6. Run the relevant Ansible playbooks to configure and validate the network.

Example:

```bash
sudo containerlab deploy -t topology/aar-lab.yml
```

To deploy the digital twin:

```bash
sudo containerlab deploy -t topology/aar-lab-twin.yml
```

To remove a deployed topology:

```bash
sudo containerlab destroy -t topology/aar-lab.yml
```

**Note:** The CI/CD workflow relies on self-hosted runners with the network lab environment and dependencies configured. It will not run unchanged on a standard GitHub-hosted runner.

## Authors & Contributions

This project was developed collaboratively as part of the Network Automation course at ISEL.

- **Leonor Oliveira** — [GitHub profile](https://github.com/leonoroliveira)
- **Idiane Moreira** — [GitHub profile](https://github.com/IdianeMoreira)

Both contributors collaborated on the project. Individual contributions should be described here according to the work performed by each author.

## Academic Context

Developed as part of the Network Automation course at ISEL – Instituto Superior de Engenharia de Lisboa.

