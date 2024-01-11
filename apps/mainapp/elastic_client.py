import os
import json
import requests 
from dotenv import load_dotenv

load_dotenv()

def getLast30Coincidence(index='qainar-coincidence'):

    username_elastic=str(os.getenv('ELASTIC_USERNAME')),
    password_elastic=str(os.getenv('ELASTIC_PASSWORD')),
    cert_file=str(os.getenv('ELASTIC_CERT_FILE'))

    url = "https://elastic:9200/"
    search_endpoint = f"{url}{index}/_search"
    query = {   
        "query": {
            "match_all": {}  
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "desc"
                }
            }
        ],
        "size": 30
        }

    try: 
        response = requests.post(search_endpoint, json=query, auth=(username_elastic, password_elastic), verify=cert_file)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            hits = response_json.get("hits", {}).get("hits", [])
            err = None
    except requests.exceptions.RequestException as e: 
        hits = None
        err = (f"Error: {e}") 
    except Exception as e:
        hits = None
        err = (f"Unexpected error: {e}") 
    
    return hits, err




def getSignalsFromCoincidenceHits(hits, index='qainar_signals'):

    username_elastic=str(os.getenv('ELASTIC_USERNAME')),
    password_elastic=str(os.getenv('ELASTIC_PASSWORD')),
    cert_file=str(os.getenv('ELASTIC_CERT_FILE'))

    url = "https://elastic:9200/"
    search_endpoint = f"{url}{index}/_search"
    signal_ids = []

    for hit in hits:
        if "_source" in hit and "signal_id" in hit["_source"]:
            signal_ids.extend(hit["_source"]["signal_id"])

    query = {
        "_source": ["@timestamp", "event.timestamp", "event.ip_src","event.ip_dst", "identifiers.uid","identifiers.user"],
        "query": {
            "terms": {
                "_id": signal_ids
            }
        }, 
        "size" : len(signal_ids)
    }

    try: 
        response = requests.post(search_endpoint, json=query, auth=(username_elastic, password_elastic), verify=cert_file)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            signalHits = response_json.get("hits", {}).get("hits", [])
            err = None
    except requests.exceptions.RequestException as e: 
        signalHits = None
        err = (f"Error: {e}") 
    except Exception as e:
        signalHits = None
        err = (f"Unexpected error: {e}") 
    return signalHits, err