import os
import shutil
import unittest

import service
from yandex_drive_downloader import YandexDriveDownloader


def clear_downloads():
    downloads_dir = service.get_downloads_dir()
    if os.path.exists(downloads_dir):
        shutil.rmtree(downloads_dir)


class YandexDriveTests(unittest.TestCase):

    def download(self, resource_path):
        clear_downloads()
        os.mkdir(service.get_downloads_dir())
        access_token = service.get_yandex_drive_access_token()
        downloader = YandexDriveDownloader(access_token)
        try:
            path = downloader.download_file(resource_path)
        except Exception as e:
            self.fail(f"Ошибка: {e}")

        self.assertEqual(os.path.exists(path), True)

    def upload(self, path, path_on_ya_drive):
        access_token = service.get_yandex_drive_access_token()
        downloader = YandexDriveDownloader(access_token)
        if not os.path.exists(path):
            path = f'{service.get_proj_dir()}/{path}'
        try:
            if os.path.isfile(path):
                downloader.upload_file(path, path_on_ya_drive)
            else:
                downloader.upload_folder(path, path_on_ya_drive)
        except Exception as e:
            self.fail(f"Ошибка: {e}")

    def test_file_downloading(self):
        self.download("me.jpg")

    def test_dir_downloading(self):
        self.download("testDirectory")

    def test_dir_uploading(self):
        self.upload('testDirectory/audio', "audio")

    def test_file_uploading(self):
        self.upload(f'C:/Users/MagicBook/Documents/GitHub/CloudStorageConnector/testDirectory/баран', "баран")
