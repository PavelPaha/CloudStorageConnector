from abc import abstractmethod

import service


class Client:
    @abstractmethod
    def upload_file(self, file_path, upload_path=''):
        pass

    @abstractmethod
    def download_file(self, save_path, path=service.get_downloads_dir()):
        pass

    @abstractmethod
    def download_folder(self, folder_path, download_path=None):
        pass

    @abstractmethod
    def create_folder(self, folder_path):
        pass

    @abstractmethod
    def upload_folder(self, folder_path, destination_path):
        pass

    @abstractmethod
    def get_list_files_and_folders(self, path=""):
        pass
