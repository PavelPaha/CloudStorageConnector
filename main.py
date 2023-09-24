import json

import service
from google_drive_uploader import GoogleDriveUploader
from google_drive_downloader import GoogleDriveDownloader
from dropbox.dropbox_downloader import DropboxDownloader


if __name__ == '__main__':
    # service = service.configure_service()

    # folder_list = service.ListFile({'q': "trashed=false"}).GetList()
    # for folder in folder_list:
    #     print('folder title: %s, id: %s' % (folder['title'], folder['id']))

    # downloader = GoogleDriveDownloader(service.get_token())
    # downloader.create_file('testDirectory/images/i.jpg', 'kek')
    # downloader.save('1y-qGLUW9gD19u7xQqrWzAxUMazcYS1yo')

    dropbox_access_token = json.load(open('secrets/dropbox_access_token.json'))['token']
    downloader = DropboxDownloader(dropbox_access_token)
    downloader.upload_file('/Homework/math/t.txt', 'requirements.txt')
    # downloader.download_file('/1.5.pdf', 'abc.pdf')
    # # #

    # uploader = GoogleDriveUploader(service)
    # uploader.upload_basic('1.jpeg', '1.jpeg')
    # uploader.upload_folder_to_drive(r"C:\Users\MagicBook\Documents\GitHub\CloudStorageConnector\some")
    # uploader.upload_file_to_specific_folder('1Lcf-IdE80tcYMTA9Q05gYceyU8RJySvc', '1.jpeg')
