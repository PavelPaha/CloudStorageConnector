import os
import unittest

import service
from dropbox.dropbox_client import DropboxClient


class DropboxDrive(unittest.TestCase):

    @service.take_action
    def download(self, download_path):
        p = os.path.dirname(os.getcwd())
        os.chdir(p)
        client = DropboxClient(service.get_dropbox_access_token())
        path = client.download_file(download_path)
        self.assertEqual(os.path.exists(path), True)

    @service.take_action
    def upload_file(self, file_path, upload_path):
        p = os.path.dirname(os.getcwd())
        os.chdir(p)
        client = DropboxClient(service.get_dropbox_access_token())
        path = os.path.join(service.get_proj_dir(), file_path)
        client.upload_file(path, upload_path)

    @service.take_action
    def upload_folder(self, file_path, upload_path):
        p = os.path.dirname(os.getcwd())
        os.chdir(p)
        client = DropboxClient(service.get_dropbox_access_token())
        path = os.path.join(service.get_proj_dir(), file_path)
        client.upload_folder(path, upload_path)

    def test_images_downloading(self):
        self.download('/images/i.jpg')

    def test_pdf_downloading(self):
        self.download('/1.5.pdf')

    def test_image_uploading(self):
        path = os.path.join('testDirectory', 'images', 'i.jpg')
        self.upload_file(path, '/i.jpg')

    def test_pdf_uploading(self):
        path = os.path.join('testDirectory', 'pdf', 'someDoc.pdf')
        self.upload_file(path, '/someDoc.pdf')

    def test_folder_downloading(self):
        client = DropboxClient(service.get_dropbox_access_token())
        client.download_folder('/images')

    def test_folder_uploading(self):
        self.upload_folder('testDirectory', '/')

    @staticmethod
    def test_get_list_folder():
        client = DropboxClient(service.get_dropbox_access_token())
        data = client.get_list_files_and_folders()
        print(data)
