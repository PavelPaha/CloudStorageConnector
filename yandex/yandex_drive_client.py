import os.path

import requests

import service
from client import Client


class YandexDriveClient(Client):
    def __init__(self, token):
        self.URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.access_token = token
        self.default_headers = {'Content-Type': 'application/json',
                                'Accept': 'application/json',
                                'Authorization': f'OAuth {self.access_token}'}

    def upload_file(self, file_path, savefile=None):
        if savefile is None:
            savefile = os.path.basename(file_path)
        """Загрузка файла.
        savefile: Путь к файлу на Диске
        folder_path: Путь к загружаемому файлу
        replace: true or false Замена файла на Диске"""

        res = requests.get(f'{self.URL}/upload?folder_path={savefile}&overwrite=True',
                           headers=self.default_headers).json()

        with open(file_path, 'rb') as f:
            try:
                requests.put(res['href'], files={'file': f})
            except Exception as e:
                print(res, e)

    def download_file(self, save_path, path=service.get_downloads_dir()):
        get_name_request = requests.get(
            f'https://cloud-api.yandex.net/v1/disk/resources?path={save_path}&fields=name,type,_embedded',
            headers=self.default_headers).json()

        path_to_save = f'{path}/{get_name_request["name"]}'
        print(path_to_save)
        resource_type = get_name_request["type"]
        if resource_type == 'dir':
            if not os.path.exists(path_to_save):
                os.mkdir(path_to_save)
            embedded = get_name_request['_embedded']

            items = embedded["items"]
            for item in items:
                self.download_file(item['path'], path_to_save)
        else:
            response = requests.get(f'{self.URL}/download?path={save_path}', headers=self.default_headers)
            response.raise_for_status()
            response_json = response.json()

            response_json = requests.get(response_json['href'], headers=self.default_headers)
            with open(path_to_save, 'wb+') as f:
                f.write(response_json.content)
        return path

    def download_folder(self, folder_path, download_path=service.get_downloads_dir()):
        return self.download_file(folder_path, download_path)

    def create_folder(self, folder_path):
        response = requests.put(f'{self.URL}?folder_path={folder_path}', headers=self.default_headers).json()
        if response.__contains__('error'):
            print('Warning', response['description'])
            return
        requests.put(response['href'])

    def upload_folder(self, folder_path, destination_path=None):
        items = os.listdir(folder_path)
        if destination_path is not None:
            self.create_folder(destination_path)
        for item in items:
            new_destination = item if destination_path is None else f"{destination_path}/{item}"
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                self.upload_file(item_path, new_destination)
            elif os.path.isdir(item_path):
                self.upload_folder(item_path, new_destination)

    def get_list_files_and_folders(self, path='/'):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = {
            "Authorization": f"OAuth {self.access_token}"
        }

        params = {
            "path": path
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        result = response.json()
        entries = result["_embedded"]["items"]

        items = []
        for entry in entries:
            items += [f'Name: {entry["name"]}, path: {entry["path"].replace("disk:/", "")}']
        return '\n'.join(items)
