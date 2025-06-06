from pathlib import Path

import requests

from app.config.setting import setting
from app.repository.store import get_store

root_path = Path(__file__).parent.parent.parent.resolve()

REFRESH_TOKEN_KEY = 'strava-refresh-token'


def get_access_token() -> str | None:
    """Obtém um access token válido, seja do refresh token ou solicitando autorização inicial."""
    client_id = setting.STRAVA_CLIENT_ID
    client_secret = setting.STRAVA_CLIENT_SECRET
    redirect_uri = setting.STRAVA_REDIRECT_URI
    scope = setting.STRAVA_SCOPE

    if not client_id or not client_secret:
        print("Por favor, configure seu 'STRAVA_CLIENT_ID' e 'STRAVA_CLIENT_SECRET' no .env")
        return None

    stored_refresh_token = _load_refresh_token()

    if stored_refresh_token:
        try:
            token_data = _refresh_access_token(client_id, client_secret, stored_refresh_token)
            _save_refresh_token(token_data.get('refresh_token', stored_refresh_token))
            print("Novo access token obtido usando o refresh token.")
            return token_data['access_token']
        except requests.exceptions.HTTPError as e:
            print(f"Erro ao obter novo access token usando o refresh token: {e}")
            print("Será necessário realizar a autorização inicial novamente.")

            # Remove o refresh token inválido para forçar a nova autorização
            store = get_store()
            store.add(REFRESH_TOKEN_KEY, None)

    else:
        print("Nenhum refresh token encontrado. Iniciando o fluxo de autorização.")
        authorization_url = _get_authorization_url(client_id, redirect_uri, scope)
        print(f"Abra este URL no seu navegador para autorizar o acesso:\n{authorization_url}")
        print("Após autorizar, você será redirecionado para uma URL com o parâmetro 'code'.")
        authorization_code = input("Cole aqui o valor do parâmetro 'code' da URL de redirecionamento: ").strip()

        if authorization_code:
            try:
                token_data = _exchange_code_for_token(client_id, client_secret, authorization_code, redirect_uri)
                _save_refresh_token(token_data['refresh_token'])
                print("Access token obtido com sucesso.")
                return token_data['access_token']
            except requests.exceptions.HTTPError as e:
                print(f"Erro ao trocar o código de autorização pelo token: {e}")
        else:
            print("Nenhum código de autorização fornecido.")

    return None


def _load_refresh_token() -> str | None:
    """Carrega o refresh token da base"""
    store = get_store()
    value = store.get(REFRESH_TOKEN_KEY)
    return value


def _refresh_access_token(client_id, client_secret, refresh_token) -> dict:
    """Obtém um novo access token usando o refresh token."""
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post('https://www.strava.com/oauth/token', data=data)
    response.raise_for_status()
    return response.json()


def _save_refresh_token(refresh_token: str):
    """Salva o refresh token na base"""
    store = get_store()
    store.add(REFRESH_TOKEN_KEY, refresh_token)


def _get_authorization_url(client_id, redirect_uri, scope):
    """Gera a URL de autorização do Strava."""
    return f"https://www.strava.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"


def _exchange_code_for_token(client_id, client_secret, authorization_code, redirect_uri) -> dict:
    """Troca o código de autorização pelo access token e refresh token."""
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }
    response = requests.post('https://www.strava.com/oauth/token', data=data)
    response.raise_for_status()
    return response.json()
