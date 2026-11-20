import json
import sys

path = sys.argv[1]

with open(path, encoding="utf-8") as file:
    sbom = json.load(file)

required_fields = ["bomFormat", "specVersion", "components",]

for field in required_fields:
    if field not in sbom:
        print(f"Отсутствует обязательное поле: {field}")
        sys.exit(1)

print("Формат SBOM:", sbom["bomFormat"])
print("Версия спецификации:", sbom["specVersion"])

components = sbom["components"]

print("Количество компонентов:", len(components))

for component in components:
    print(component.get("name", "Unknown"), component.get("version", "Unknown"),)

if "dependencies" in sbom:
    print("Граф зависимостей присутствует")
else:
    print("Граф зависимостей отсутствует")

print("SBOM проверен")