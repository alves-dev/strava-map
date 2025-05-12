import requests

from app.config.setting import setting

STRAVA_BASE_API = 'https://www.strava.com/api/v3'
STRAVA_ACTIVITIES_API = f'{STRAVA_BASE_API}/athlete/activities'
STRAVA_ACTIVITIES_ID_API = f'{STRAVA_BASE_API}/activities'

PER_PAGE = 100


def get_activities(token: str) -> dict:
    params = {
        'per_page': PER_PAGE,
        'page': 1,
        'after': setting.STRAVA_ACTIVITIES_AFTER
    }

    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        resp = requests.get(STRAVA_ACTIVITIES_API, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do Strava: {e}")
        return {}


def get_activities_by_id(token: str, id: str) -> dict:
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        resp = requests.get(f'{STRAVA_ACTIVITIES_ID_API}/{id}', headers=headers)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API do Strava: {e}")
        return {}


def get_properties(activity: dict) -> dict:
    distance = f"{round(activity.get('distance') / 1000, 1)} km"

    return {
        "id": activity.get('id'),
        "date": str(activity.get('start_date_local')).replace('T', ' ')[:16],
        "distance": distance,
        "type": activity.get('type'),
        "color": _get_color(activity.get('type'))
    }


def _get_color(type: str) -> int:
    """
    Cada número no grafana é convertido para uma cor
    """
    colors = {
        'Ride': 1,  # dark-yellow
        'Run': 2  # dark-orange
    }
    return colors.get(type, 0)  # red
