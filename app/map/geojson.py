import json

import polyline

from app.github.commit import Commit
from app.strava import client as strava


def create_geojson(activities: dict, token: str):
    features = []

    for activity in activities:
        id = activity.get('id')
        activity_by_id = strava.get_activities_by_id(token, id)

        poly = activity_by_id.get('map', {}).get('polyline')

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

    commit = Commit()

    formated_json = json.dumps(geojson, indent=4, ensure_ascii=False)
    commit.write_file('strava_all.json', formated_json)

    commit.commit_and_push('strava-activities')
