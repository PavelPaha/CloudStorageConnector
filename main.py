import service
from google_drive_uploader import GoogleDriveUploader
from google_drive_downloader import GoogleDriveDownloader
from yandex_drive_downloader import YandexDriveDownloader


if __name__ == '__main__':
    serv = service.configure_service()
    yandex_drive_access_token = service.get_yandex_drive_access_token()
    # folder_list = service.ListFile({'q': "trashed=false"}).GetList()
    # for folder in folder_list:
    #     print('folder title: %s, id: %s' % (folder['title'], folder['id']))

    # downloader = GoogleDriveDownloader(service)
    # a = downloader.get_file_names(500)
    # for i in a:
    #     print(i)

    # downloader.save('1y-qGLUW9gD19u7xQqrWzAxUMazcYS1yo')
    # # #

    # uploader = GoogleDriveUploader(service)
    # uploader.upload_basic('1.jpeg', '1.jpeg')
    # uploader.upload_folder_to_drive(r"C:\Users\MagicBook\Documents\GitHub\CloudStorageConnector\some")
    # uploader.upload_file_to_specific_folder('1Lcf-IdE80tcYMTA9Q05gYceyU8RJySvc', '1.jpeg')

    downloader = YandexDriveDownloader(yandex_drive_access_token)
    downloader.upload_file("1.jpeg")
    # downloader.download_file("kek")
    # resource_path = "some/1.jpeg"
    # destination_path = ""
    # downloader.upload_file_to_yandex_disk(resource_path, destination_path)
