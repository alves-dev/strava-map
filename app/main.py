from app.map import geojson
from app.strava import client as strava
from app.strava import token as token_service


def init():
    token = token_service.get_access_token()
    if token is None:
        return
    activities = strava.get_activities(token)
    geojson.create_geojson(activities)


if __name__ == "__main__":
    init()
