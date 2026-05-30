from addressing import (
    wildcardFromPrefix,
    getLoopbackPrefix,
    getLoopbackIp,
    getLanGateway,
    getLanNetwork,
    getP2pNetwork,
    getP2pIp,
)


def buildAristaInterfaces(routerNumber):
    interfaces = []

    if routerNumber == 1:
        interfaces.append({"name": "Ethernet1", "desc": "to r2", "ip": getP2pIp(1, 2)})
        interfaces.append({"name": "Ethernet2", "desc": "to h1", "ip": getLanGateway(1)})
        interfaces.append({"name": "Ethernet3", "desc": "to r3", "ip": getP2pIp(1, 3)})
        interfaces.append({"name": "Ethernet4", "desc": "to r4", "ip": getP2pIp(1, 4)})

    elif routerNumber == 2:
        interfaces.append({"name": "Ethernet1", "desc": "to r1", "ip": getP2pIp(2, 1)})
        interfaces.append({"name": "Ethernet2", "desc": "to h2", "ip": getLanGateway(2)})
        interfaces.append({"name": "Ethernet3", "desc": "to r3", "ip": getP2pIp(2, 3)})
        interfaces.append({"name": "Ethernet4", "desc": "to r4", "ip": getP2pIp(2, 4)})

    return interfaces


def buildAristaOspfNetworks(routerNumber):
    networks = []

    networks.append({
        "network": getLoopbackIp(routerNumber),
        "wildcard": "0.0.0.0",
        "area": routerNumber
    })

    networks.append({
        "network": getLanNetwork(routerNumber).split("/")[0],
        "wildcard": wildcardFromPrefix(getLanNetwork(routerNumber)),
        "area": routerNumber
    })

    if routerNumber == 1:
        p2pLinks = [(1, 2), (1, 3), (1, 4)]
    elif routerNumber == 2:
        p2pLinks = [(1, 2), (2, 3), (2, 4)]
    else:
        p2pLinks = []

    for a, b in p2pLinks:
        prefix = getP2pNetwork(a, b)
        networks.append({
            "network": prefix.split("/")[0],
            "wildcard": wildcardFromPrefix(prefix),
            "area": 0
        })

    return networks


def buildAristaRouterData(routerNumber):
    return {
        "hostname": f"r{routerNumber}",
        "loopback": getLoopbackPrefix(routerNumber),
        "interfaces": buildAristaInterfaces(routerNumber),
        "ospf": {
            "processId": 1,
            "routerId": getLoopbackIp(routerNumber),
            "networks": buildAristaOspfNetworks(routerNumber),
        },
    }