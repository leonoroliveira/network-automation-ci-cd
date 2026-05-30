from addressing import getLoopbackPrefix, getLoopbackIp, getLanGateway, getP2pIp


def buildSrlinuxRouterData(routerNumber):
    return {
        "hostname": f"r{routerNumber}",
        "loopback": {
            "name": "lo0",
            "admin_state": "enable",
            "subinterface": {
                "index": 0,
                "admin_state": "enable",
                "ipv4_admin_state": "enable",
                "ip_prefix": getLoopbackPrefix(routerNumber),
            },
        },
        "interfaces": buildSrlinuxInterfaces(routerNumber),
        "network_instance": {
            "name": "default",
            "interfaces": [
                "lo0.0",
                "ethernet-1/1.0",
                "ethernet-1/2.0",
                "ethernet-1/3.0",
            ],
        },
        "ospf": {
            "name": "default",
            "admin_state": "enable",
            "router_id": getLoopbackIp(routerNumber),
            "version": "srl_nokia-ospf-types:ospf-v2",
            "area_id": "0.0.0.0",
            "interfaces": [
                {
                    "interface_name": "ethernet-1/1.0",
                    "admin_state": "enable",
                    "interface_type": "broadcast",
                    "advertise_subnet": True,
                },
                {
                    "interface_name": "ethernet-1/2.0",
                    "admin_state": "enable",
                    "interface_type": "broadcast",
                    "advertise_subnet": True,
                },
                {
                    "interface_name": "lo0.0",
                    "admin_state": "enable",
                    "advertise_subnet": True,
                    "passive": True,
                },
            ],
        },
    }


def buildSrlinuxInterfaces(routerNumber):
    interfaces = []

    if routerNumber == 3:
        interfaces.append(
            {
                "name": "ethernet-1/1",
                "admin_state": "enable",
                "subinterface": {
                    "index": 0,
                    "type": "srl_nokia-interfaces:routed",
                    "admin_state": "enable",
                    "ipv4_admin_state": "enable",
                    "ip_prefix": getP2pIp(3, 1),
                },
            }
        )
        interfaces.append(
            {
                "name": "ethernet-1/2",
                "admin_state": "enable",
                "subinterface": {
                    "index": 0,
                    "type": "srl_nokia-interfaces:routed",
                    "admin_state": "enable",
                    "ipv4_admin_state": "enable",
                    "ip_prefix": getP2pIp(3, 2),
                },
            }
        )
        interfaces.append(
            {
                "name": "ethernet-1/3",
                "admin_state": "enable",
                "subinterface": {
                    "index": 0,
                    "type": "srl_nokia-interfaces:routed",
                    "admin_state": "enable",
                    "ipv4_admin_state": "enable",
                    "ip_prefix": getLanGateway(3),
                },
            }
        )

    return interfaces