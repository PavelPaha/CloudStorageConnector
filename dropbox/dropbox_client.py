import json
import os
import time

import requests

import service
from client import Client


class DropboxClient(Client):
    main_url = 'https://api.dropboxapi.com/2/auth/token/revoke'

    create_folder_url = 'https://api.dropboxapi.com/2/files/create_folder_v2'
    upload_file_url = 'https://content.dropboxapi.com/2/files/upload'
    download_file_url = 'https://content.dropboxapi.com/2/files/download'
    list_folders_url = 'https://api.dropboxapi.com/2/sharing/list_folders'

    session_data_file = 'upload_session.json'

    def __init__(self, access_token):
        self.access_token = access_token
        self.default_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    @service.operation_status("Uploading a file")
    def upload_file(self, file_path, upload_path='/'):
        if service.size_limit_exceeded(file_path):
            file_path = service.archive(file_path)
            self.upload_large_file(file_path, upload_path)
            return

        with open(file_path, "rb") as file:
            file_content = file.read()

        api_args = {
            "autorename": True,
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

    @service.operation_status("Donwloading a file")
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

            path = os.path.join(path, os.path.basename(save_path))

            with open(path, 'wb') as file:
                file.write(response.content)
            return path
        except Exception as e:
            raise Exception(f"Произошла ошибка загрузки файла на Dropbox (upload_path = {save_path}): {e}")

    @service.operation_status("Downloading a folder")
    def download_folder(self, folder_path, download_path=None):
        if download_path is None:
            download_path = os.path.join(service.get_downloads_dir(), f'{os.path.basename(folder_path)}.zip')
        else:
            download_path = os.path.join(service.get_downloads_dir(), download_path)

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

    @service.operation_status("Creating a folder")
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

    @service.operation_status("Uploading a folder")
    def upload_folder(self, folder_path, destination_path):
        if service.size_limit_exceeded(folder_path):
            folder_path = service.archive(folder_path)
            self.upload_file(folder_path, destination_path)
            return
        # if not destination_path.startswith('/'):
        #     destination_path = f'/{destination_path}'

        for file_name in os.listdir(folder_path):
            current_path = os.path.join(folder_path, file_name)
            if os.path.isfile(current_path):
                self.upload_file(current_path, f'{destination_path}/{file_name}')
            else:
                self.upload_folder(current_path, f'{destination_path}/{file_name}')

        print(f"Папка {folder_path} успешно загружена на диск (путь на диске - {destination_path})")

    @service.operation_status("Getting folders and files")
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

    def upload_large_file(self, file_path, upload_path):
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/octet-stream'
        }

        session_id = None
        offset = 0
        try:
            with open(self.session_data_file, 'r') as f:
                session_data = json.load(f)
                session_id = session_data['session_id']
                offset = session_data['offset']
        except FileNotFoundError:
            pass

        if not session_id:
            url = 'https://content.dropboxapi.com/2/files/upload_session/start'
            r = self.upload_with_retry(url, headers, None)
            res = r.json()
            session_id = res['session_id']

        with open(file_path, 'rb') as f:
            f.seek(offset)
            data = f.read(1024 * 1024)
            while data:
                print(f'session_id = {session_id}, offset = {offset}')

                url = 'https://content.dropboxapi.com/2/files/upload_session/append_v2'
                headers['Dropbox-API-Arg'] = '{"cursor": {"session_id": "' + session_id + \
                                             '", "offset": ' + str(offset) + '}, "close": false}'
                self.upload_with_retry(url, headers, data)
                offset += len(data)
                with open(self.session_data_file, 'w') as restored:
                    json.dump({'session_id': session_id, 'offset': offset}, restored)
                data = f.read(1024 * 1024)

        commit_path = (upload_path + '/' + os.path.basename(file_path)).replace('//', '/')
        url = 'https://content.dropboxapi.com/2/files/upload_session/finish'
        headers['Dropbox-API-Arg'] = '{"cursor": {"session_id": "' + session_id + \
                                     '", "offset": ' + str(
            offset) + '}, "commit": {"path": "' + commit_path + '", "mode": "overwrite"}}'
        r = requests.post(url, headers=headers, data=None)
        r.raise_for_status()
        os.remove(self.session_data_file)

    def upload_with_retry(self, url, headers, data, max_retries=3, delay=5):
        for i in range(max_retries):
            try:
                r = requests.post(url, headers=headers, data=data)
                r.raise_for_status()
                return r
            except requests.exceptions.RequestException as e:
                if e.response.status_code == 409:
                    error_text_in_json = json.loads(e.response.text)
                    if 'correct_offset' in error_text_in_json['error']:
                        correct_offset = error_text_in_json['error']['correct_offset']

                        with open(self.session_data_file, 'r') as f:
                            session_data = json.load(f)
                            session_id = session_data['session_id']

                        with open(self.session_data_file, 'w') as f:
                            json.dump({'session_id': session_id, 'offset': correct_offset}, f)

                if i < max_retries - 1:
                    time.sleep(delay)
                    continue
                else:
                    raise
