import os
from jinja2 import Environment, FileSystemLoader


def ensureFolderExists(folderPath):
    os.makedirs(folderPath, exist_ok=True)


def getTemplateName(routerType):
    if routerType == "arista_eos":
        return "arista.j2"
    if routerType == "nokia_srl":
        return "nokia.j2"
    if routerType == "mikrotik_routeros":
        return "mikrotik.j2"

    raise ValueError(f"Unsupported router type: {routerType}")


def renderRouterConfig(routerData, routerType, templatesPath):
    env = Environment(
        loader=FileSystemLoader(templatesPath),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(getTemplateName(routerType))
    return template.render(**routerData)


def writeConfigToFile(hostname, config, outputPath):
    ensureFolderExists(outputPath)
    configPath = os.path.join(outputPath, f"{hostname}.cfg")

    with open(configPath, "w", encoding="utf-8") as configFile:
        configFile.write(config)

    return configPath