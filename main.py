import os.path
import subprocess

import service
from client import Client
from dropbox.dropbox_client import DropboxClient
from yandex.yandex_drive_client import YandexDriveClient

print("Выберите хранилище: Yandex(Y) или DropBox(D)")
storage_type = input()

storage = Client()
if storage_type == 'Y':
    storage = YandexDriveClient(service.get_yandex_drive_access_token())
elif storage_type == 'D':
    storage = DropboxClient(service.get_dropbox_access_token())


def handle_command(client: Client, command):
    if command == 1:
        print(client.get_list_files_and_folders())
    elif command == 2:
        while True:
            print("Введите путь на выбранном хранилище")
            folder_path = input()
            try:
                directory_path = storage.download_folder(folder_path)
                print(fr"Скачано в {directory_path}")
                normalized_path = os.path.normpath(directory_path)
                subprocess.Popen(f'explorer "{normalized_path}"')
                break
            except Exception as e:
                print(f"Ошибка {e}")
    elif command == 3:
        while True:
            print("Введите путь на выбранном хранилище")
            folder_path = input()
            try:
                directory_path = storage.download_file(folder_path)
                print(fr"Скачано в {directory_path}")
                normalized_path = os.path.normpath(directory_path)
                subprocess.Popen(f'explorer "{normalized_path}"')
                break
            except Exception as e:
                print(f"Ошибка {e}")
    elif command == 4:
        try:
            while True:
                print("Введите путь папки, которую нужно загрузить в хранилище")
                folder_path = input()
                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    break
                print("Неверно указан путь к искомой папке")

            print("Введите путь на диске")
            destination_path = input()
            client.upload_folder(folder_path, destination_path)
        except Exception as e:
            print(f"Ошибка {e}")
    elif command == 5:
        try:
            while True:
                print("Введите путь к файлу, который нужно загрузить в хранилище")
                file_path = input()
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    break
                print("Неверно указан путь к искомому файлу")

            print("Введите путь на диске")
            destination_path = input()
            client.upload_file(file_path, destination_path)
        except Exception as e:
            print(f"Ошибка {e}")
    elif command == -1:
        exit(0)
    else:
        print("Не распознана команда!")


while True:
    print(
        """
    
Выберите операцию:
    1. Посмотреть список файлов и папок
    2. Скачать папку
    3. Скачать файл
    4. Загрузить папку
    5. Загрузить файл
    """)

    command = int(input())
    handle_command(storage, command)
