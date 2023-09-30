import json
import os

import requests

import service
from client import Client


class DropboxClient(Client):
    main_url = 'https://api.dropboxapi.com/2/auth/token/revoke'

    create_folder_url = 'https://api.dropboxapi.com/2/files/create_folder_v2'
    upload_file_url = 'https://content.dropboxapi.com/2/files/upload'
    download_file_url = 'https://content.dropboxapi.com/2/files/download'
    list_folders_url = 'https://api.dropboxapi.com/2/sharing/list_folders'

    def __init__(self, access_token):
        self.access_token = access_token
        self.default_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def upload_file(self, file_path, upload_path='/'):
        with open(file_path, "rb") as file:
            file_content = file.read()

        api_args = {
            "autorename": False,
            "path": upload_path,
            "mode": "add",
            "mute": False,
            "strict_conflict": False
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": json.dumps(api_args)
        }
        try:
            response = requests.post(self.upload_file_url,
                                     headers=headers, data=file_content)
            response.raise_for_status()
            return
        except Exception as e:
            raise Exception(f"Произошла ошибка загрузки файла на Dropbox (upload_path = {upload_path}): {e}")

    def download_file(self, save_path, path=service.get_downloads_dir()):
        # if not save_path.startswith('/'):
        #     save_path = f'/{save_path}'
        api_args = {
            "path": save_path,
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Dropbox-API-Arg": json.dumps(api_args)
        }

        try:
            response = requests.post(self.download_file_url,
                                     headers=headers)
            response.raise_for_status()
            path = f"{path}/{os.path.basename(save_path)}"

            with open(path, 'wb') as file:
                file.write(response.content)
            return path
        except Exception as e:
            raise Exception(f"Произошла ошибка загрузки файла на Dropbox (upload_path = {save_path}): {e}")

    def download_folder(self, folder_path, download_path=None):
        # if not folder_path.startswith('/'):
        #     folder_path = f'/{folder_path}'
        if download_path is None:
            download_path = f'{service.get_downloads_dir()}/{os.path.basename(folder_path)}.zip'
        else:
            download_path = f'{service.get_downloads_dir()}/{download_path}'

        url = "https://content.dropboxapi.com/2/files/download_zip"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Dropbox-API-Arg": f'{{"path": "{folder_path}"}}'
        }

        response = requests.post(url, headers=headers, stream=True)
        response.raise_for_status()

        with open(download_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        return download_path

    def create_folder(self, folder_path):
        data = {
            "autorename": False,
            "path": folder_path
        }
        json_data = json.dumps(data)
        try:
            response = requests.post(self.create_folder_url,
                                     headers=self.default_headers, data=json_data).json()
            return response
        except Exception as e:
            raise Exception(f"Произошла ошибка создания папки (path = {folder_path}): {e}")

    def upload_folder(self, folder_path, destination_path):
        # if not destination_path.startswith('/'):
        #     destination_path = f'/{destination_path}'

        for file_name in os.listdir(folder_path):
            current_path = f'{folder_path}/{file_name}'
            if os.path.isfile(current_path):
                self.upload_file(current_path, f'{destination_path}/{file_name}')
            else:
                self.upload_folder(current_path, f'{destination_path}/{file_name}')

        print(f"Папка {folder_path} успешно загружена на диск (путь на диске - {destination_path})")

    def get_list_files_and_folders(self, path=""):
        url = "https://api.dropboxapi.com/2/files/list_folder"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "path": path,
            "recursive": False,
            "include_media_info": False,
            "include_deleted": False,
            "include_has_explicit_shared_members": False,
            "include_mounted_folders": True,
            "include_non_downloadable_files": True
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        entries = result["entries"]

        items = []
        for entry in entries:
            items += [f'Name: {entry["name"]}, path: {entry["path_lower"]}']
        return '\n'.join(items)
