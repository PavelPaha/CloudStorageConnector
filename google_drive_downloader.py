from __future__ import print_function

import io
import os.path

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

import service


class GoogleDriveDownloader:
    mime_google_type_to_file_application = {
        "application/vnd.google-apps.spreadsheet": ".xlsx",
        "application/vnd.google-apps.document": ".docx",
        "image/jpeg": ".jpeg",
        "application/pdf": ".pdf"
    }

    mime_google_type_to_default_mime_type = {
        "application/vnd.google-apps.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }

    def __init__(self, service):
        self.service = service

    def download_file_data(self, file_info):
        try:
            file_id = file_info["id"]
            mimeType = file_info['mimeType']
            if self.mime_google_type_to_default_mime_type.__contains__(mimeType):
                request = self.service.files().export(fileId=file_id,
                                                      mimeType=self.mime_google_type_to_default_mime_type[mimeType])
            else:
                request = self.service.files().get_media(fileId=file_id)

            # request = self.service.files().export_media(fileId=file_id, mimeType=mimeType)

            file = self.send_request(request)

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.getvalue()

    def send_request(self, request):
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')
        return file

    def download_folder(self, folder_info):
        folder_name = folder_info["name"]
        folder_id = folder_info["id"]

        if not os.path.exists(folder_name):
            os.mkdir(f"downloads/{folder_name}")

        results = self.service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=2, fields="nextPageToken, files(id, name)",
            pageToken=None).execute()
        inner_files = results.get('files', [])
        for file in inner_files:
            file_id = file["id"]
            file_info = self.service.files().get(fileId=file_id).execute()
            file = self.download_file_data(file_info)

            self.save_file_in_directory(file, file_info, folder_name)

    def get_file_names(self, count):
        results = self.service.files().list(
            pageSize=count, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        return [item['id'] for item in items]

    def is_folder(self, file_info):
        mimeType = file_info['mimeType']
        return mimeType == 'application/vnd.google-apps.folder'

    def save(self, file_id, path=None):
        print(f"Началась загрузка файла с id = {file_id}")
        file_info = self.service.files().get(fileId=file_id).execute()

        if self.is_folder(file_info):
            self.download_folder(file_info)
            return path

        data = self.download_file_data(file_info)
        file_info = self.service.files().get(fileId=file_id).execute()
        file = data

        return self.save_file_in_directory(file, file_info, path)


    def save_file_in_directory(self, file, file_info, path):
        file_id = file_info["id"]
        file_name = f"{str(file_info['name'])}"
        mimeType = file_info['mimeType']
        file_extension = ""
        if self.mime_google_type_to_file_application.__contains__(mimeType):
            file_extension = self.mime_google_type_to_file_application[mimeType]

        path_to_dir = service.get_downloads_dir() if path is None else path

        if not os.path.exists(path_to_dir):
            os.mkdir(path_to_dir)

        file_path = os.path.join(path_to_dir, f"{file_name}{file_extension}")
        with open(file_path, 'wb+') as f:
            f.write(file)

        print(f"Файл с id = {file_id} загружен в {file_path}")
        return file_path
