from jinja2 import Environment, TemplateSyntaxError
import os
import sys

env = Environment()
errors = 0
found = 0

exclude = [".venv", ".git", "__pycache__"]

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in exclude]

    for f in files:
        if f.endswith(".j2"):
            found += 1
            path = os.path.join(root, f)

            try:
                with open(path, "r", encoding="utf-8") as file:
                    source = file.read()

                env.parse(source)
                print(f"OK: {path}")

            except TemplateSyntaxError as e:
                print(f"ERROR: {path} - {e}")
                errors += 1

if found == 0:
    print("ERROR: no Jinja2 templates found")
    sys.exit(1)

sys.exit(1 if errors else 0)