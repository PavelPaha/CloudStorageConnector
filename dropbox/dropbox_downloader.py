import json

import requests

import service


class DropboxDownloader:
    URL = 'https://api.dropboxapi.com/2/auth/token/revoke'

    create_folder_url = 'https://api.dropboxapi.com/2/files/create_folder_v2'
    upload_file_url = 'https://content.dropboxapi.com/2/files/upload'
    download_file_url = 'https://content.dropboxapi.com/2/files/download'

    def __init__(self, access_token):
        self.access_token = access_token
        self.default_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def create_folder(self, path, autorename=False):
        data = {
            "autorename": autorename,
            "path": path
        }
        json_data = json.dumps(data)
        try:
            response = requests.post(self.create_folder_url,
                                     headers=self.default_headers, data=json_data).json()
            return response
        except Exception as e:
            raise Exception(f"Произошла ошибка создания папки (path = {path}): {e}")

    def upload_file(self, upload_path, file_path, author_name=False):
        with open(file_path, "rb") as file:
            file_content = file.read()

        api_args = {
            "autorename": author_name,
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
                                     headers=headers, data=file_path)
            # TODO: пофиксить Dropbox-API-Arg в header'ах
            return response
        except Exception as e:
            raise Exception(f"Произошла ошибка загрузки файла на Dropbox (upload_path = {upload_path}): {e}")

    def download_file(self, download_path, file_name, save_path=service.get_downloads_dir()):
        api_args = {
            "path": download_path,
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Dropbox-API-Arg": json.dumps(api_args)
        }
        try:
            response = requests.post(self.download_file_url,
                                     headers=headers)
            # TODO: пофиксить Dropbox-API-Arg в header'ах
            with open(f"{save_path}/{file_name}", 'wb') as file:
                file.write(response.content)
            return f"{save_path}/{file_name}"
        except Exception as e:
            raise Exception(f"Произошла ошибка загрузки файла на Dropbox (upload_path = {download_path}): {e}")
