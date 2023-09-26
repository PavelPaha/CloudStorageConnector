import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive']


def tryaction(func):
    def wrapper(*args):
        try:
            func(*args)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    return wrapper


def get_dropbox_access_token():
    with open(f'{get_proj_dir()}/secrets/dropbox_access_token.json') as file:
        json_data = json.load(file)
        return json_data['token']


def get_proj_dir():
    return r"C:\Users\MagicBook\Documents\GitHub\CloudStorageConnector"


def get_downloads_dir():
    return r"C:/Users/MagicBook/Documents/GitHub/CloudStorageConnector/Downloads"


def get_yandex_drive_access_token():
    with open(f"{get_proj_dir()}/secrets/auth_token.json") as token:
        return json.load(token)["token"]


def get_token():
    with open(os.path.join(get_proj_dir(), 'token.json')) as f:
        return json.load(f)["token"]


def configure_service():
    creds = None
    proj_dir = get_proj_dir()
    token_name = os.path.join(proj_dir, 'secrets/token.json')
    creds_name = os.path.join(proj_dir, 'secrets/credentials.json')
    if os.path.exists(token_name):
        creds = Credentials.from_authorized_user_file(token_name, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_name, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_name, 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service
