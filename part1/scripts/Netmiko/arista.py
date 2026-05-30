from netmiko import ConnectHandler
import json

def get_version_arista(conn):

    output = conn.send_command("show version | json")

    data = json.loads(output)

    return data["version"]

def get_lldp_arista(conn):
    
    output = conn.send_command("show lldp neighbors | json")

    data = json.loads(output)

    neighbors = []

    for n in data["lldpNeighbors"]:
        neighbors.append({
            "interface": n["port"],
            "host": n["neighborDevice"],
            "port": n["neighborPort"]
        })

    return neighbors


import json

def get_interfaces_arista(conn):
    status_output = conn.send_command("show interfaces status | json")
    ip_output = conn.send_command("show ip interface brief | json")

    status_data = json.loads(status_output)
    ip_data = json.loads(ip_output)

    interfaces = []
    ip_interfaces = ip_data.get("interfaces", {})

    for name, info in status_data["interfaceStatuses"].items():
        ip = ""
        mask = ""

        if name in ip_interfaces and ip_interfaces[name]:
            ip_info = ip_interfaces[name]

            if "interfaceAddress" in ip_info and "ipAddr" in ip_info["interfaceAddress"]:
                ip = ip_info["interfaceAddress"]["ipAddr"].get("address", "")
                mask = ip_info["interfaceAddress"]["ipAddr"].get("maskLen", "")

        interfaces.append({
            "interface": name,
            "status": info.get("linkStatus", ""),
            "ip": ip,
            "mask": mask
        })

    return interfaces

def get_config_arista(conn):
    return conn.send_command("show running-config")