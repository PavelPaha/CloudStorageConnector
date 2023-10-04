import os
import unittest

import service
from yandex.yandex_drive_client import YandexDriveClient


class YandexDriveTest(unittest.TestCase):

    @service.take_action
    def download(self, resource_path):
        access_token = service.get_yandex_drive_access_token()
        client = YandexDriveClient(access_token)
        path = client.download_file(resource_path)
        print(path)
        self.assertEqual(os.path.exists(path), True)

    @service.take_action
    def upload(self, path, path_on_ya_drive):
        access_token = service.get_yandex_drive_access_token()
        client = YandexDriveClient(access_token)
        if not os.path.exists(path):
            path = os.path.join(service.get_proj_dir(), path)
        if os.path.isfile(path):
            client.upload_file(path, path_on_ya_drive)
        else:
            client.upload_folder(path, path_on_ya_drive)

    def test_file_downloading(self):
        self.download("me.jpg")

    def test_dir_downloading(self):
        self.download("testDirectory")

    def test_dir_uploading(self):
        path = os.path.join('testDirectory', 'audio')
        self.upload(path, "audio")

    def test_file_uploading(self):
        path = os.path.join('testDirectory', 'баран', 'баран.jpg')
        self.upload(path, "баран.jpg")

    def test_get_all_items(self):
        client = YandexDriveClient(service.get_yandex_drive_access_token())
        try:
            items = client.get_list_files_and_folders()
            print(items)
        except Exception as e:
            self.fail(e)
