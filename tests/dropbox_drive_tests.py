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

    def upload(self, file_path, upload_path):
        downloader = DropboxDownloader(service.get_dropbox_access_token())
        try:
            if os.path.isfile(file_path):
                downloader.upload_file(upload_path, f'{service.get_proj_dir()}/{file_path}')
            else:
                downloader.upload_folder_to_drive(f'{service.get_proj_dir()}/{file_path}', upload_path)
        except Exception as e:
            self.fail(f"Ошибка: {e}")

    def test_images_downloading(self):
        self.download('/images/i.jpg', 'i.jpg')

    def test_pdf_downloading(self):
        self.download('/1.5.pdf', '1.5.pdf')

    def test_image_uploading(self):
        self.upload('testDirectory/images/i.jpg', '/i.jpg')

    def test_pdf_uploading(self):
        self.upload('testDirectory/pdf/someDoc.pdf', '/someDoc.pdf')

    def test_folder_uploading(self):
        self.upload('testDirectory', '/a')

    def test_folder_downloading(self):
        self.download('/a', 'a')

    # def test_spreadsheet_downloading(self):
    #     spreadsheet_id = '1uW5TKmzAZ4CkOqqe1oVbeyHocB04T8IGyyZpVP5P6ng'
    #     self.download(spreadsheet_id)
    #
    # def test_docs_downloading(self):
    #     doc_id = '106TnB4S76iVGs2VvoCiLUFY7icw2cVp3TLsA0hPXsUs'
    #     self.download(doc_id)
    #
    # def test_pdf_downloading(self):
    #     pdf_id = '1VN_Do7RLwM7zf41L2Z3gvqLxg7uzQ7uD'
    #     self.download(pdf_id)
    #
    # def test_other_type_downloading(self):
    #     ids = ['1iGk2yu60o6-cwYiZdw0aTwilmDENBJTi', '126CLUN19ar2vmx3yftZ6Qbqwj__hJWdv',
    #            '1-UxZGoC7jXgnV3BeT_zCNLSFSpIIW898', '14KjlU84oy8mpC9Y2x-mnyJSlC6pSugut']
    #     for id in ids:
    #         self.download(id)
