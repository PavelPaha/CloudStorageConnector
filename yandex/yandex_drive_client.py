import math
import os.path
import shutil

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

    @service.operation_status("Uploading a file")
    def upload_file(self, file_path, savefile=None, archive=True):
        if savefile is None:
            savefile = os.path.basename(file_path)

        if service.size_limit_exceeded(file_path) and archive:
            file_path = service.archive(file_path)
            extension = os.path.splitext(file_path)[1]
            savefile += extension

            self.upload_file_partially(file_path, savefile)

        res = requests.get(f'{self.URL}/upload?path={savefile}&overwrite=True',
                           headers=self.default_headers).json()

        with open(file_path, 'rb') as f:
            try:
                requests.put(res['href'], files={'file': f})
            except Exception as e:
                print(res, e)

    @service.operation_status("Donwloading a file")
    def download_file(self, save_path, path=service.get_downloads_dir(), partially=False):
        if partially:
            try:
                return self.download_parts(save_path, path)
            except Exception as e:
                print(f"Не нашлось Partially: {e}")
            return None

        get_name_request = requests.get(
            f'https://cloud-api.yandex.net/v1/disk/resources?path={save_path}&fields=name,type,_embedded',
            headers=self.default_headers).json()

        path_to_save = os.path.join(path, get_name_request["name"])
        print(f"File {path_to_save} downloaded")
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
        return os.path.join(path, os.path.basename(save_path))

    @service.operation_status("Downloading a folder")
    def download_folder(self, folder_path, download_path=service.get_downloads_dir(), partially=True):
        return self.download_file(folder_path, download_path, partially=partially)

    @service.operation_status("Creating a folder")
    def create_folder(self, folder_path):
        try:
            response = requests.put(f'{self.URL}?path={folder_path}', headers=self.default_headers)
            # response.raise_for_status()
            response_json = response.json()
            if 'error' in response:
                print('Warning', response_json['description'])
                return
            requests.put(response_json['href'])
        except:
            print(f"Папка {folder_path} уже создана")

    @service.operation_status("Uploading a folder")
    def upload_folder(self, folder_path, destination_path=None):
        if service.size_limit_exceeded(folder_path):
            folder_path = service.archive(folder_path)
            self.upload_file(folder_path, destination_path)
            return

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

    @service.operation_status("Getting folders and files")
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

    def upload_file_partially(self, file_path, upload_path='', part_size=2 * 1024 * 1024):
        parts_count = math.ceil(service.get_size(file_path) / part_size)
        offset = 0
        print(f"The file will be cut into {parts_count} parts")

        recource_name, extension = os.path.splitext(os.path.basename(file_path))
        dir_name = f'{recource_name}_Partially{extension}'
        parent_dir = os.path.dirname(upload_path)
        self.create_folder(f'{parent_dir}/{dir_name}')

        with open(file_path, 'rb') as f:
            for i in range(parts_count):
                file_name, _ = os.path.splitext(os.path.basename(file_path))

                current_file_name = f'{file_name}-Part{i + 1}'
                current_upload_path = f'{parent_dir}/{dir_name}/{os.path.splitext(current_file_name)[0]}'.strip('/')

                bytes = f.read(part_size)
                local_parent_dir = os.path.dirname(file_path)
                part_file_path = os.path.join(local_parent_dir, parent_dir, current_file_name)

                with open(part_file_path, 'wb') as part_file:
                    part_file.write(bytes)

                self.upload_file(part_file_path, current_upload_path, archive=False)
                os.remove(part_file_path)
                offset += part_size

    def download_parts(self, destination_path, save_to=service.get_downloads_dir()):
        resource_name, extension = os.path.splitext(destination_path)
        folder_path = self.download_folder(f'{resource_name}_Partially{extension}', partially=False)
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        files.sort()

        path = os.path.join(save_to, f'{destination_path}_Partially.{extension}')
        with open(path, 'wb') as outfile:
            for filename in files:
                with open(os.path.join(folder_path, filename), 'rb') as infile:
                    outfile.write(infile.read())

        shutil.rmtree(folder_path)
        return path
