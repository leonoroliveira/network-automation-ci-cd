import json

def get_version_nokia(conn):

    output = conn.send_command("show version | as json")
    data = json.loads(output)

    version = data["basic system info"]["Software Version"]
    return version


import json

def get_version_nokia(conn):
    output = conn.send_command("show version | as json")
    data = json.loads(output)

    version = data["basic system info"]["Software Version"]
    return version


def get_lldp_nokia(conn):
    output = conn.send_command("show system lldp neighbor | as json")

    start = output.find("{")
    end = output.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(f"Output LLDP inválido do Nokia:\n{output}")
    
    clean_output = output[start:end+1]
    data = json.loads(clean_output)

    neighbors = []

    for n in data["LLDP-Interface"]:
        neighbors.append({
            "interface": n["Name"],
            "host": n["Neighbor System Name"],
            "port": n["Neighbor Port"]
        })

    return neighbors


def get_interfaces_nokia(conn):
    output = conn.send_command_timing("show interface | as json")

    start = output.find("{")
    end = output.rfind("}")

    clean_output = output[start:end+1]
    data = json.loads(clean_output)

    interfaces = []

    for iface in data["interfaces"]:
        name = iface["name"]
        status = iface["oper-state"]
        ip = ""
        mask = ""

        if name == "mgmt0":
            addresses = iface["subinterfaces"][0]["address"]

            for addr in addresses:
                if addr["type"] == "IPv4":
                    ip, mask = addr["prefix"].split("/")
                    break

        interfaces.append({
            "interface": name,
            "status": status,
            "ip": ip,
            "mask": mask
        })

    return interfaces

def get_config_nokia(conn):
    return conn.send_command("info")