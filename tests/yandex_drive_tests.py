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

    def upload(self, path):
        path = f'{service.get_proj_dir()}/{path}'
        access_token = service.get_yandex_drive_access_token()
        downloader = YandexDriveDownloader(access_token)
        try:
            downloader.upload_file(path)
        except Exception as e:
            self.fail(f"Ошибка: {e}")

    def test_downloading(self):
        self.download("me.jpg")
        self.download('kek')

    def test_uploading(self):
        self.upload('1.jpeg')
