import json
import os
from pathlib import Path

import requests

root_path = Path(__file__).parent.parent.parent.resolve()

# Nome do arquivo de configuração principal
CONFIG_FILE = root_path / 'config.json'
# Nome do arquivo para armazenar o refresh token
REFRESH_TOKEN_FILE = root_path / 'refresh_token.txt'


def get_access_token() -> str | None:
    """Obtém um access token válido, seja do refresh token ou solicitando autorização inicial."""
    config = _load_config()
    if not config:
        return None

    client_id = config.get('client_id')
    client_secret = config.get('client_secret')
    redirect_uri = config.get('redirect_uri', 'http://localhost')  # Valor padrão se não estiver no config
    scope = config.get('scope', 'activity:read_all,profile:read_all')  # Escopo padrão

    if not client_id or not client_secret:
        print(f"Por favor, configure seu 'client_id' e 'client_secret' no arquivo '{CONFIG_FILE}'.")
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
            if os.path.exists(REFRESH_TOKEN_FILE):
                os.remove(REFRESH_TOKEN_FILE)
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


def _load_config() -> dict | None:
    """Carrega as configurações do arquivo config.json."""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            f"Arquivo de configuração '{CONFIG_FILE}' não encontrado. Crie este arquivo com suas credenciais, como no 'config.example.json'")
        return None
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo de configuração '{CONFIG_FILE}'. Verifique o formato JSON.")
        return None


def _load_refresh_token() -> str | None:
    """Carrega o refresh token do arquivo refresh_token.txt"""
    try:
        with open(REFRESH_TOKEN_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except IOError:
        print(f"Erro ao ler o refresh token do arquivo '{REFRESH_TOKEN_FILE}'.")
        return None


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


def _save_refresh_token(refresh_token):
    """Salva o refresh token no arquivo refresh_token.txt."""
    try:
        with open(REFRESH_TOKEN_FILE, 'w') as f:
            f.write(refresh_token)
        print(f"Refresh token salvo com sucesso em '{REFRESH_TOKEN_FILE}'.")
    except IOError:
        print(f"Erro ao salvar o refresh token no arquivo '{REFRESH_TOKEN_FILE}'.")


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
