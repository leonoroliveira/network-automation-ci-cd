def pingFromRouter(device, destinationIp, routerType=None):

    if routerType == "mikrotik_routeros":
        print("DEBUG entrou no bloco mikrotik")
        try:
            sshTunnel = device._netmiko_open(device_type="mikrotik_routeros")
            print("DEBUG abriu netmiko mikrotik")

            try:
                command = f"/ping address={destinationIp} count=3"
                print(f"DEBUG comando: {command}")

                output = sshTunnel.send_command_timing(
                    command,
                    read_timeout=15,
                ).lower()

                print(f"\n[MikroTik ping output to {destinationIp}]")
                print(output)

            finally:
                device._netmiko_close()

            if (
                "received=3" in output
                or "received=2" in output
                or "ttl=" in output
                or "packet-loss=0" in output
            ):
                return "UP"

            return "DOWN"

        except Exception as error:
            print(f"DEBUG mikrotik ping error: {type(error).__name__}: {error}")
            try:
                device._netmiko_close()
            except Exception:
                pass
            return "DOWN"

    if routerType == "nokia_srl":
        try:
            cliResult = device.cli(
                [f"ping network-instance default {destinationIp} -c 1"]
            )
            output = str(list(cliResult.values())[0]).lower()

            if (
                "1 received" in output
                or "0% packet loss" in output
                or "bytes from" in output
                or "icmp_seq" in output
            ):
                return "UP"

            return "DOWN"

        except Exception:
            return "DOWN"

    if routerType == "arista_eos":
        try:
            cliResult = device.cli([f"ping {destinationIp} repeat 1"])
            output = str(list(cliResult.values())[0]).lower()

            if "1 received" in output or "0% packet loss" in output:
                return "UP"

            return "DOWN"

        except Exception:
            return "DOWN"

    try:
        pingResult = device.ping(destinationIp)

        if "success" in pingResult:
            success = pingResult["success"]
            if success.get("packet_loss", 100) == 0:
                return "UP"

        return "DOWN"

    except Exception:
        return "DOWN"

def printPingTable(rows):
    print("\n===== Ping Status Table =====")
    print(f"{'FROM':<6}{'TO':<6}{'DESTINATION':<18}{'STATUS':<10}")
    print("-" * 40)

    for row in rows:
        print(
            f"{row['from']:<6}"
            f"{row['to']:<6}"
            f"{row['destination']:<18}"
            f"{row['status']:<10}"
        )