import unittest
import service
import os
from dropbox.dropbox_downloader import DropboxDownloader
import shutil


def clear_downloads():
    shutil.rmtree(service.get_downloads_dir())


class DropboxDriveTests(unittest.TestCase):

    def download(self, download_path, file_name):
        downloader = DropboxDownloader(service.get_dropbox_access_token())
        try:
            path = downloader.download_file(download_path, file_name=file_name)
        except Exception as e:
            self.fail(f"Ошибка: {e}")
        self.assertEqual(os.path.exists(path), True)

    def upload_file(self, file_path, upload_path):
        downloader = DropboxDownloader(service.get_dropbox_access_token())
        try:
            downloader.upload_file(upload_path, f'{service.get_proj_dir()}/{file_path}')
        except Exception as e:
            self.fail(f"Ошибка: {e}")

    def upload_folder(self, file_path, upload_path):
        downloader = DropboxDownloader(service.get_dropbox_access_token())
        try:
            downloader.upload_folder_to_drive(f'{service.get_proj_dir()}/{file_path}', upload_path)
        except Exception as e:
            self.fail(f"Ошибка: {e}")

    def test_images_downloading(self):
        self.download('/images/i.jpg', 'i.jpg')

    def test_pdf_downloading(self):
        self.download('/1.5.pdf', '1.5.pdf')

    def test_image_uploading(self):
        self.upload_file('testDirectory/images/i.jpg', '/i.jpg')

    def test_pdf_uploading(self):
        self.upload_file('testDirectory/pdf/someDoc.pdf', '/someDoc.pdf')

    def test_folder_downloading(self):
        downloader = DropboxDownloader(service.get_dropbox_access_token())
        downloader.download_folder('/images')

    def test_folder_uploading(self):
        self.upload_folder('testDirectory', '/b')
