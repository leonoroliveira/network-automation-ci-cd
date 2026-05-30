from addressing import (
    getLoopbackPrefix,
    getLoopbackIp,
    getLanGateway,
    getLanNetwork,
    getP2pIp,
    getP2pNetwork,
)


def buildMikrotikInterfaces(routerNumber):
    interfaces = []

    if routerNumber == 4:
        interfaces.append({"name": "ether2", "desc": "to h4", "ip": getLanGateway(4)})
        interfaces.append({"name": "ether3", "desc": "to r2", "ip": getP2pIp(4, 2)})
        interfaces.append({"name": "ether4", "desc": "to r1", "ip": getP2pIp(4, 1)})

    return interfaces


def buildMikrotikOspfNetworks(routerNumber):
    networks = []

    networks.append({
        "network": getLoopbackPrefix(routerNumber),
        "area_name": f"area{routerNumber}",
    })

    networks.append({
        "network": getLanNetwork(routerNumber),
        "area_name": f"area{routerNumber}",
    })

    networks.append({
        "network": getP2pNetwork(1, 4),
        "area_name": "backbone",
    })

    networks.append({
        "network": getP2pNetwork(2, 4),
        "area_name": "backbone",
    })

    return networks


def buildMikrotikRouterData(routerNumber):
    return {
        "hostname": f"r{routerNumber}",
        "loopback": getLoopbackPrefix(routerNumber),
        "interfaces": buildMikrotikInterfaces(routerNumber),
        "ospf": {
            "router_id": getLoopbackIp(routerNumber),
            "local_area": routerNumber,
            "networks": buildMikrotikOspfNetworks(routerNumber),
        },
    }