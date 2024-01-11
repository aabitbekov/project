import json
import requests

# Укажите путь к вашему JSON-файлу
json_file_path = "test.json"
# Открываем файл на чтение
with open(json_file_path, "r") as file:
    data = json.load(file)
    
hits = data.get("hits", {}).get("hits", [])
signal_ids = []

for hit in hits:
    if "_source" in hit and "signal_id" in hit["_source"]:
        signal_ids.extend(hit["_source"]["signal_id"])
for signal in signal_ids:
    print(f'"{signal}"', end=",")
print(len(signal_ids))