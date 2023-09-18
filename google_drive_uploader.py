from __future__ import print_function

import os
import os.path

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class GoogleDriveUploader:
    def __init__(self, service):
        self.service = service

    def upload_basic(self, file_name, file_path, folder_id=None):
        try:
            media = MediaFileUpload(file_path)
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            print(f"Файл с id = {file.get('id')} успешно загружен на диск")

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.get('id')

    def upload_file_to_specific_folder(self, folder_id, file_name):
        file_metadata = {'title': file_name, "parents": [{"id": folder_id, "kind": "drive#childList"}]}
        folder = self.service.CreateFile(file_metadata)
        folder.SetContentFile(file_name)
        folder.Upload()

    def upload_folder_to_drive(self, folder_path, parent_folder_id=None):
        folder_metadata = {
            'name': os.path.basename(folder_path),
            'mimeType': 'application/vnd.google-apps.folder',
        }

        if parent_folder_id is not None:
            folder_metadata['parents'] = [parent_folder_id]

        folder = self.service.files().create(body=folder_metadata, fields='id').execute()

        for file_name in os.listdir(folder_path):
            current_path = os.path.join(folder_path, file_name)
            if os.path.isfile(current_path):
                self.upload_basic(file_name, current_path, folder['id'])
            else:
                self.upload_folder_to_drive(current_path, folder['id'])

        print(f"Папка с id = {folder['id']} успешно загружена на диск")
