import os.path
import requests
import service


class YandexDriveDownloader:
    def __init__(self, token):
        self.URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.access_token = token
        self.default_headers = {'Content-Type': 'application/json',
                                'Accept': 'application/json',
                                'Authorization': f'OAuth {self.access_token}'}

    def upload_file(self, file_path, savefile=None, replace=True):
        if savefile is None:
            savefile = os.path.basename(file_path)
        """Загрузка файла.
        savefile: Путь к файлу на Диске
        resource_path: Путь к загружаемому файлу
        replace: true or false Замена файла на Диске"""

        res = requests.get(f'{self.URL}/upload?path={savefile}&overwrite={replace}',
                           headers=self.default_headers).json()

        with open(file_path, 'rb') as f:
            try:
                requests.put(res['href'], files={'file': f})
            except Exception as e:
                print(res, e)

    def download_file(self, resource_path, path=service.get_downloads_dir()):
        res = requests.get(f'{self.URL}/download?path={resource_path}', headers=self.default_headers).json()

        get_name_request = requests.get(
            f'https://cloud-api.yandex.net/v1/disk/resources?path={resource_path}&fields=name,type,_embedded',
            headers=self.default_headers).json()

        path_to_save = f'{path}/{get_name_request["name"]}'
        resource_type = get_name_request["type"]
        if resource_type == 'dir':
            if not os.path.exists(path_to_save):
                os.mkdir(path_to_save)
            embedded = get_name_request['_embedded']

            items = embedded["items"]
            for item in items:
                self.download_file(item['path'], path_to_save)
        else:
            response = requests.get(res['href'], headers=self.default_headers)
            with open(path_to_save, 'wb+') as f:
                f.write(response.content)
        return path

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

    def create_folder(self, folder_path):
        response = requests.put(f'{self.URL}?path={folder_path}', headers=self.default_headers).json()
        if response.__contains__('error'):
            print('Warning', response['description'])
            return
        requests.put(response['href'])
