import json
import requests 

def getLast30Coincidence(index, username_elastic, password_elastic, cert_file):
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



    

        