import os
import csv
from datetime import datetime
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

from arista import get_version_arista, get_lldp_arista, get_interfaces_arista, get_config_arista
from nokia import get_version_nokia, get_lldp_nokia, get_interfaces_nokia, get_config_nokia
from mikrotik import get_version_mikrotik, get_lldp_mikrotik, get_interfaces_mikrotik, get_config_mikrotik

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
CSV_FILE = os.path.join(BASE_DIR, "scripts", "Netmiko", "routers.csv")

def read_csv(file):
    routers = []

    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            routers.append(row)

    return routers


def connect_router(router):
    device = {
        "host": router["host"],
        "port": int(router["port"]),
        "username": router["user"],
        "password": router["password"],
        "secret": router["enable_password"],
        "device_type": router["type"],
    }

    return ConnectHandler(**device)


def show_menu():
    print("\nEscolhe o que queres obter:")
    print("1 - Versions")
    print("2 - Neighbours")
    print("3 - Interfaces")
    print("4 - Configuration")
    print("5 - Tudo")

    option = input("Opção: ")
    return option


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    routers = read_csv(CSV_FILE)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    option = show_menu()

    version_file = None
    if option in ["1", "5"]:
        version_file = open(os.path.join(OUTPUT_DIR, f"versions_{now}.txt"), "w")
        version_file.write("host,sw_version\n")

    for router in routers:
        host = router["host"]
        rtype = router["type"]

        try:
            print(f"A ligar a {host}...")
            conn = connect_router(router)

            if rtype == "arista_eos":
                conn.enable()

                if option in ["1", "5"]:
                    version = get_version_arista(conn)
                    version_file.write(f"{host},{version}\n")

                if option in ["2", "5"]:
                    neighbours = get_lldp_arista(conn)
                    save_neighbours(host, neighbours, now)

                if option in ["3", "5"]:
                    interfaces = get_interfaces_arista(conn)
                    save_interfaces(host, interfaces, now)
                
                if option in ["4", "5"]:
                    config = get_config_arista(conn)
                    save_config(host, config, now)

            elif rtype == "nokia_srl":
                if option in ["1", "5"]:
                    version = get_version_nokia(conn)
                    version_file.write(f"{host},{version}\n")

                if option in ["2", "5"]:
                    neighbours = get_lldp_nokia(conn)
                    save_neighbours(host, neighbours, now)

                if option in ["3", "5"]:
                    interfaces = get_interfaces_nokia(conn)
                    save_interfaces(host, interfaces, now)

                if option in ["4", "5"]:
                    config = get_config_nokia(conn)
                    save_config(host, config, now)

            elif rtype == "mikrotik_routeros":
                if option in ["1", "5"]:
                    version = get_version_mikrotik(conn)
                    version_file.write(f"{host},{version}\n")

                if option in ["2", "5"]:
                    neighbours = get_lldp_mikrotik(conn)
                    save_neighbours(host, neighbours, now)

                if option in ["3", "5"]:
                    interfaces = get_interfaces_mikrotik(conn)
                    save_interfaces(host, interfaces, now)

                if option in ["4", "5"]:
                    config = get_config_mikrotik(conn)
                    save_config(host, config, now)

            else:
                print(f"A ignorar {host} ({rtype})")

            conn.disconnect()

        except NetmikoTimeoutException:
            print(f"[ERRO] Timeout ao ligar a {host}")
        except NetmikoAuthenticationException:
            print(f"[ERRO] Credenciais inválidas em {host}")
        except Exception as e:
            print(f"[ERRO] {host}: {e}")

    if version_file:
        version_file.close()


def save_neighbours(host, neighbors, now):
    with open(os.path.join(OUTPUT_DIR, f"neighbours_{host}_{now}.txt"), "w") as f:
        f.write("interface,neighbour_hostname,neighbour_interface\n")
        for n in neighbors:
            f.write(f"{n['interface']},{n['host']},{n['port']}\n")


def save_interfaces(host, interfaces, now):
    with open(os.path.join(OUTPUT_DIR, f"interfaces_{host}_{now}.txt"), "w") as f:
        f.write("interface,status,ip,mask\n")
        for i in interfaces:
            f.write(f"{i['interface']},{i['status']},{i['ip']},{i['mask']}\n")


def save_config(host, config, now):
    with open(os.path.join(OUTPUT_DIR, f"conf_{host}_{now}.txt"), "w") as f:
        f.write(config)

if __name__ == "__main__":
    main()