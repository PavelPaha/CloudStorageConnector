from abc import abstractmethod
import service


class Client:
    @abstractmethod
    @service.operation_status("Загрузка файла")
    def upload_file(self, file_path, upload_path=''):
        pass

    @abstractmethod
    @service.operation_status("Скачивание файла")
    def download_file(self, save_path, path=service.get_downloads_dir()):
        pass

    @abstractmethod
    @service.operation_status("Скачивание папки")
    def download_folder(self, folder_path, download_path=None):
        pass

    @abstractmethod
    @service.operation_status("Создание папки")
    def create_folder(self, folder_path):
        pass

    @abstractmethod
    @service.operation_status("Загрузка папки")
    def upload_folder(self, folder_path, destination_path):
        pass

    @abstractmethod
    @service.operation_status("Получение листинга файлов и папок")
    def get_list_files_and_folders(self, path=""):
        pass
