import requests
import pandas as pd
from datetime import datetime
import os

OUTPUT_FILE = "bixi_realtime.csv"

# --- URLs Bixi ---
url_info = "https://gbfs.velobixi.com/gbfs/2-2/fr/station_information.json"
url_status = "https://gbfs.velobixi.com/gbfs/2-2/fr/station_status.json"

def collect():
    # Récupération des infos et statuts
    info = requests.get(url_info).json()['data']['stations']
    status = requests.get(url_status).json()['data']['stations']

    stations_list = []
    for s in status:
        station_info = next((i for i in info if i['station_id'] == s['station_id']), {})
        num_ebikes = s.get('num_ebikes_available', 0)
        num_bikes_total = s.get('num_bikes_available', 0)
        num_classic = num_bikes_total - num_ebikes
        stations_list.append({
            "timestamp": datetime.now().isoformat(),
            "station_id": s['station_id'],
            "name": station_info.get('name', 'N/A'),
            "lat": station_info.get('lat', None),
            "lon": station_info.get('lon', None),
            "capacity": station_info.get('capacity', None),
            "status": "ouvert" if s.get('is_renting', 0) == 1 else "fermé",
            "num_bikes_available": num_bikes_total,
            "num_bikes_electric": num_ebikes,
            "num_bikes_classic": num_classic,
            "num_docks_available": s.get('num_docks_available', 0)
        })

    df = pd.DataFrame(stations_list)

    # Si le fichier existe, on ajoute sans header ; sinon, on crée avec header
    write_header = not os.path.exists(OUTPUT_FILE)
    df.to_csv(OUTPUT_FILE, mode="a", header=write_header, index=False)

if __name__ == "__main__":
    collect()