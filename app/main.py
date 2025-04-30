from app.map import geojson
from app.strava import client as strava


def init():
    activities = strava.get_activities()
    geojson.create_geojson(activities)


if __name__ == "__main__":
    init()
