import service


class Client:
    def upload_file(self, file_path, upload_path='/'):
        pass

    def download_file(self, save_path, path=service.get_downloads_dir()):
        pass

    def download_folder(self, folder_path, download_path=None):
        pass

    def create_folder(self, folder_path):
        pass

    def upload_folder(self, folder_path, destination_path):
        pass

    def get_list_files_and_folders(self, path=""):
        pass
