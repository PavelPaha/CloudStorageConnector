import os.path

import requests

import service


class YandexDriveDownloader:
    def __init__(self, token):
        self.access_token = token
        self.default_headers = {'Content-Type': 'application/json',
                                'Accept': 'application/json',
                                'Authorization': f'OAuth {self.access_token}'}

    def upload_file(self, file_path, savefile=None, replace=True):
        if savefile is None:
            savefile = os.path.basename(file_path)
        URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        """Загрузка файла.
        savefile: Путь к файлу на Диске
        resource_path: Путь к загружаемому файлу
        replace: true or false Замена файла на Диске"""

        res = requests.get(f'{URL}/upload?path={savefile}&overwrite={replace}', headers=self.default_headers).json()
        with open(file_path, 'rb') as f:
            try:
                requests.put(res['href'], files={'file': f})
            except:
                print(res)

    def download_file(self, resource_path, path=service.get_downloads_dir()):
        URL = 'https://cloud-api.yandex.net/v1/disk/resources'

        res = requests.get(f'{URL}/download?path={resource_path}', headers=self.default_headers).json()

        get_name_request = requests.get(
            f'https://cloud-api.yandex.net/v1/disk/resources?path={resource_path}&fields=name,type,_embedded',
            headers=self.default_headers).json()

        path_to_save = f'{path}/{get_name_request["name"]}'
        type = get_name_request["type"]
        if type == 'dir':
            if not os.path.exists(path_to_save):
                os.mkdir(path_to_save)
            embedded = get_name_request['_embedded']

            items = embedded["items"]
            for item in items:
                self.download_file(item['path'], path_to_save)
        else:
            answer = requests.get(res['href'], headers=self.default_headers)
            with open(path_to_save, 'wb+') as f:
                f.write(answer.content)
            print(answer)
        return path
