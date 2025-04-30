import json
from pathlib import Path

import polyline

from app.strava import client as strava


def create_geojson(activities: dict):
    features = []

    for activity in activities:
        poly = activity.get('map', {}).get('summary_polyline')
        if not poly:
            continue

        try:
            coordinates = polyline.decode(poly)
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[lon, lat] for lat, lon in coordinates]
                },
                "properties": strava.get_properties(activity)
            }
            features.append(feature)
        except Exception as e:
            print(f"Erro ao decodificar polyline: {e}")
            continue

    save_geojson(features)


def save_geojson(features: list):
    # FeatureCollection
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    root_path = Path(__file__).parent.parent.parent.resolve()
    geojson_path = root_path / 'geojson'

    # today = str(datetime.now().strftime("%Y-%m-%d"))

    with open(f'{geojson_path}/strava_all.json', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=4)

    # with open(f'{geojson_path}/strava_{today}.json', 'w', encoding='utf-8') as f:
    #     json.dump(geojson, f, ensure_ascii=False, indent=4)
