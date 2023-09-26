import service
from yandex.yandex_drive_client import YandexDriveClient


if __name__ == '__main__':
    serv = service.configure_service()
    yandex_drive_access_token = service.get_yandex_drive_access_token()

    downloader = YandexDriveClient(yandex_drive_access_token)
    downloader.upload_file("1.jpeg")