from arista_nap import buildAristaRouterData
from nokia_nap import buildSrlinuxRouterData
from mikrotik_nap import buildMikrotikRouterData


def buildRouterData(routerNumber, routerType):
    if routerType == "arista_eos":
        return buildAristaRouterData(routerNumber)

    if routerType == "nokia_srl":
        return buildSrlinuxRouterData(routerNumber)

    if routerType == "mikrotik_routeros":
        return buildMikrotikRouterData(routerNumber)

    raise ValueError(f"Unsupported router type: {routerType}")