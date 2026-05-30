import sys
import os

scriptsDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if scriptsDir not in sys.path:
    sys.path.insert(0, scriptsDir)

from napalm import get_network_driver
import tempfile
import json
from netmiko import ConnectHandler
import logging
logging.disable(logging.ERROR)

def connectToRouter(containerHost, routerType):
    if routerType == "arista_eos":
        driver = get_network_driver("eos")
        optionalArgs = {"transport": "https"}

    elif routerType == "nokia_srl":
        driver = get_network_driver("srl")
        optionalArgs = {
            "gnmi_port": 57400,
            "jsonrpc_port": 443,
            "target_name": containerHost,
            "tls_ca": "/home/xlcvlym/topology/clab-aar-lab/.tls/ca/ca.pem",
            "encoding": "JSON_IETF",
    }
    elif routerType == "mikrotik_routeros":
        driver = get_network_driver("ros")
        optionalArgs = {}

    else:
        raise ValueError(f"Unsupported router type: {routerType}")

    device = driver(
        hostname=containerHost,
        username="admin",
        password="admin",
        timeout=60,
        optional_args=optionalArgs,
    )

    device.open()
    return device


def applyConfigToRouter(containerHost, routerType, configPath):
    device = connectToRouter(containerHost, routerType)

    try:
        print(f"Connected to {containerHost}")
        
        if routerType == "nokia_srl":
            with open(configPath, "r", encoding="utf-8") as file:
                config = file.read()

            device.load_merge_candidate(config=config)

            try:
                device.commit_config()
            except Exception as error:
                print(f"[{containerHost}] commit_config timeout, mas continuo: {type(error).__name__}: {error}")

        elif routerType == "mikrotik_routeros":
            with open(configPath, "r", encoding="utf-8") as file:
                commands = [
                    line.strip()
                    for line in file
                    if line.strip() and not line.strip().startswith("#")
                ]

            sshTunnel = device._netmiko_open(device_type="mikrotik_routeros")

            try:
                for command in commands:
                    sshTunnel.send_command_timing(command, read_timeout=15)
            finally:
                device._netmiko_close()

        else:
            device.load_merge_candidate(filename=configPath)

            diffs = device.compare_config()

            if diffs:
                device.commit_config()
            else:
                device.discard_config()

        return device

    except Exception as error:
        import traceback
        traceback.print_exc()
        print(f"Erro completo: {type(error).__name__}: {error}")
        device.close()
        raise