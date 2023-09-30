import json
import os.path
import shutil

SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive']


def clear_downloads():
    downloads_dir = get_downloads_dir()
    if os.path.exists(downloads_dir):
        shutil.rmtree(downloads_dir)


def take_action(func):
    print(f'{__file__}')
    clear_downloads()
    os.mkdir(get_downloads_dir())

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
    return r"C:/Users/MagicBook/Documents/GitHub/CloudStorageConnector"


def get_downloads_dir():
    return r"C:/Users/MagicBook/Documents/GitHub/CloudStorageConnector/Downloads"


def get_yandex_drive_access_token():
    with open(f"{get_proj_dir()}/secrets/auth_token.json") as token:
        return json.load(token)["token"]


def get_token():
    with open(os.path.join(get_proj_dir(), 'token.json')) as f:
        return json.load(f)["token"]
