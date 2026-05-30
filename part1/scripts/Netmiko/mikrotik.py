
def get_version_mikrotik(conn):

    output = conn.send_command("/system resource print")

    for line in output.splitlines():
        if "version:" in line:
            version = line.split(":")[1].strip()
            return version

    return "unknown"

def get_version_mikrotik(conn):
    output = conn.send_command("/system resource print")

    for line in output.splitlines():
        if "version:" in line:
            return line.split(":", 1)[1].strip()

    return "unknown"


def get_lldp_mikrotik(conn):
    output = conn.send_command("/ip neighbor print detail")

    neighbors = []
    current = {}

    for line in output.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("0 ") or line.startswith("1 ") or line.startswith("2 ") or line.startswith("3 "):
            if current:
                if "interface" in current and "host" in current and "port" in current:
                    neighbors.append(current)
            current = {}

        if "interface=" in line:
            parts = line.split()
            for part in parts:
                if part.startswith("interface="):
                    current["interface"] = part.split("=", 1)[1]

                elif part.startswith("identity="):
                    current["host"] = part.split("=", 1)[1]

                elif part.startswith("interface-name="):
                    current["port"] = part.split("=", 1)[1]

        else:
            parts = line.split()
            for part in parts:
                if part.startswith("interface="):
                    current["interface"] = part.split("=", 1)[1]

                elif part.startswith("identity="):
                    current["host"] = part.split("=", 1)[1]

                elif part.startswith("interface-name="):
                    current["port"] = part.split("=", 1)[1]

    if current:
        if "interface" in current and "host" in current and "port" in current:
            neighbors.append(current)

    return neighbors

def get_interfaces_mikrotik(conn):

    interfaces = []

    int_output = conn.send_command("/interface print")
    ip_output = conn.send_command("/ip address print")

    # mapa interface -> ip
    ip_map = {}

    for line in ip_output.splitlines():
        parts = line.split()
        if len(parts) >= 3 and "/" in parts[1]:
            ip, mask = parts[1].split("/")
            iface = parts[-1]
            ip_map[iface] = (ip, mask)

    for line in int_output.splitlines():
        parts = line.split()

        if len(parts) >= 3 and parts[0].isdigit():
            flags = parts[1]
            name = parts[2]

            status = "up" if "R" in flags else "down"
            ip, mask = ip_map.get(name, ("", ""))

            interfaces.append({
                "interface": name,
                "status": status,
                "ip": ip,
                "mask": mask
            })

    return interfaces

def get_config_mikrotik(conn):
    return conn.send_command("/export")