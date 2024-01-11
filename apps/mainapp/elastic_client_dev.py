import os
import json

def getLast30Coincidence(index='qainar-coincidence'):
    # Укажите путь к вашему JSON-файлу
    json_file_path = "test.json"
    # Открываем файл на чтение
    with open(json_file_path, "r") as file:
        data = json.load(file)
    
    hits = data.get("hits", {}).get("hits", [])
    err = None
    return hits, err




def getSignalsFromCoincidenceHits(hits, index='qainar_signals'):
        # Укажите путь к вашему JSON-файлу
    json_file_path = "signals.json"
    # Открываем файл на чтение
    with open(json_file_path, "r") as file:
        data = json.load(file)
    
    signalHits = data.get("hits", {}).get("hits", [])
    err = None
    return signalHits, err