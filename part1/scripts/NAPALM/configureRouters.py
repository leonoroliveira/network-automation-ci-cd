import os
import time

from config_data import buildRouterData
from config_render import ensureFolderExists, renderRouterConfig, writeConfigToFile
from config_deploy import applyConfigToRouter
from ping_tests import pingFromRouter, printPingTable
import logging
logging.disable(logging.ERROR)


def configureOneRouter(
    routerNumber,
    containerHost,
    routerType,
    templatesPath,
    outputPath,
):
    routerData = buildRouterData(routerNumber, routerType)
    config = renderRouterConfig(routerData, routerType, templatesPath)

    configPath = writeConfigToFile(
        routerData["hostname"],
        config,
        outputPath,
    )
    print(f"\nConfig written to: {configPath}")

    device = applyConfigToRouter(containerHost, routerType, configPath)
    return device


def safeCli(device, commands, label):
    if device is None:
        print(f"\n[{label}] Device unavailable")
        return

    try:
        output = device.cli(commands)
        print(f"\n[{label}]")
        for command, result in output.items():
            print(f"\n> {command}\n{result}")
    except Exception as error:
        print(f"\n[{label}] Error running CLI commands: {error}")


def addPingRow(rows, openDevices, sourceRouter, destRouter, destinationIp):
    sourceDevice = openDevices.get(sourceRouter)

    if sourceDevice is None:
        rows.append(
            {
                "from": f"r{sourceRouter}",
                "to": f"r{destRouter}",
                "destination": destinationIp,
                "status": "SKIPPED",
            }
        )
        return

    try:
        routerType = sourceDevice["type"]
        device = sourceDevice["device"]

        status = pingFromRouter(device, destinationIp, routerType)
    except Exception:
        status = "DOWN"

    rows.append(
        {
            "from": f"r{sourceRouter}",
            "to": f"r{destRouter}",
            "destination": destinationIp,
            "status": status,
        }
    )


def main():
    baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    templatesPath = os.path.join(baseDir, "templates")
    outputPath = os.path.join(baseDir, "output", "configs")

    ensureFolderExists(outputPath)

    routers = [
        {"number": 1, "host": "clab-aar-lab-r1", "type": "arista_eos"},
        {"number": 2, "host": "clab-aar-lab-r2", "type": "arista_eos"},
        {"number": 3, "host": "clab-aar-lab-r3", "type": "nokia_srl"},
        {"number": 4, "host": "clab-aar-lab-r4", "type": "mikrotik_routeros"},
    ]

    openDevices = {}

    try:
        for router in routers:
            routerNumber = router["number"]
            containerHost = router["host"]
            routerType = router["type"]

            try:
                device = configureOneRouter(
                    routerNumber,
                    containerHost,
                    routerType,
                    templatesPath,
                    outputPath,
                )

                openDevices[routerNumber] = {
                    "device": device,
                    "type": routerType,
                    "host": containerHost,
                }

            except Exception as error:
                print(
                    f"\n[WARNING] Skipping router r{routerNumber} "
                    f"({containerHost}) due to error: {error}"
                )
                openDevices[routerNumber] = None
        

        rows = []

        addPingRow(rows, openDevices, 1, 2, "172.16.12.2")
        addPingRow(rows, openDevices, 2, 1, "172.16.12.1")

        addPingRow(rows, openDevices, 1, 2, "172.16.0.2")
        addPingRow(rows, openDevices, 2, 1, "172.16.0.1")

        addPingRow(rows, openDevices, 1, 3, "172.16.0.3")
        addPingRow(rows, openDevices, 2, 3, "172.16.0.3")
        addPingRow(rows, openDevices, 3, 1, "172.16.0.1")
        addPingRow(rows, openDevices, 3, 2, "172.16.0.2")

        addPingRow(rows, openDevices, 1, 4, "172.16.0.4")
        addPingRow(rows, openDevices, 2, 4, "172.16.0.4")
        addPingRow(rows, openDevices, 4, 1, "172.16.0.1")
        addPingRow(rows, openDevices, 4, 2, "172.16.0.2")

        printPingTable(rows)

    finally:
        for routerData in openDevices.values():
            if routerData is not None:
                try:
                    routerData["device"].close()
                except Exception:
                    pass


if __name__ == "__main__":
    main()