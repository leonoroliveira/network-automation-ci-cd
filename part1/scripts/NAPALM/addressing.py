from ipaddress import ip_network


def wildcardFromPrefix(prefix):
    network = ip_network(prefix, strict=False)
    netmaskOctets = [int(octet) for octet in str(network.netmask).split(".")]
    wildcardOctets = [str(255 - octet) for octet in netmaskOctets]
    return ".".join(wildcardOctets)


def getLoopbackPrefix(routerNumber):
    return f"172.16.0.{routerNumber}/32"


def getLoopbackIp(routerNumber):
    return f"172.16.0.{routerNumber}"


def getLanGateway(routerNumber):
    return f"192.168.{routerNumber}.254/24"


def getLanNetwork(routerNumber):
    return f"192.168.{routerNumber}.0/24"


def getP2pNetwork(routerA, routerB):
    low = min(routerA, routerB)
    high = max(routerA, routerB)
    return f"172.16.{low}{high}.0/24"


def getP2pIp(localRouter, remoteRouter):
    low = min(localRouter, remoteRouter)
    high = max(localRouter, remoteRouter)
    return f"172.16.{low}{high}.{localRouter}/24"