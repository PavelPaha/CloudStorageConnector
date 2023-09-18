import unittest
import service
import os
from google_drive_downloader import GoogleDriveDownloader
import shutil


def clear_downloads():
    shutil.rmtree(service.get_downloads_dir())


class GoogleDriveTests(unittest.TestCase):

    def download(self, id):
        clear_downloads()
        srv = service.configure_service()
        downloader = GoogleDriveDownloader(srv)
        try:
            path = downloader.save(id)
        except Exception as e:
            self.fail(f"Ошибка: {e}")

        self.assertEqual(os.path.exists(path), True)

    def test_images_downloading(self):
        photo_id = '1y-qGLUW9gD19u7xQqrWzAxUMazcYS1yo'
        self.download(photo_id)

    def test_spreadsheet_downloading(self):
        spreadsheet_id = '1uW5TKmzAZ4CkOqqe1oVbeyHocB04T8IGyyZpVP5P6ng'
        self.download(spreadsheet_id)

    def test_docs_downloading(self):
        doc_id = '106TnB4S76iVGs2VvoCiLUFY7icw2cVp3TLsA0hPXsUs'
        self.download(doc_id)

    def test_pdf_downloading(self):
        pdf_id = '1VN_Do7RLwM7zf41L2Z3gvqLxg7uzQ7uD'
        self.download(pdf_id)

    def test_other_type_downloading(self):
        ids = ['1iGk2yu60o6-cwYiZdw0aTwilmDENBJTi', '126CLUN19ar2vmx3yftZ6Qbqwj__hJWdv',
               '1-UxZGoC7jXgnV3BeT_zCNLSFSpIIW898', '14KjlU84oy8mpC9Y2x-mnyJSlC6pSugut']
        for id in ids:
            self.download(id)
