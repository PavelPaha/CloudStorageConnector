from __future__ import print_function

import io
from googleapiclient.http import MediaIoBaseDownload

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Downloader:
    service = None

    mime_google_type_to_file_application = {
        "application/vnd.google-apps.spreadsheet": "xlsx",
        "application/vnd.google-apps.document": "docx"
    }

    mime_google_type_to_default_mime_type = {
        "application/vnd.google-apps.document": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }

    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

    def download_file_data(self, real_file_id):
        """Downloads a file
        Args:
            real_file_id: ID of the file to download
        Returns : IO object with location.

        Load pre-authorized user credentials from the environment.
        for guides on implementing OAuth2 for the application.
        """

        try:
            file_id = real_file_id

            # pylint: disable=maybe-no-member
            file_info = self.service.files().get(fileId=file_id).execute()
            mimeType = file_info['mimeType']
            request = None

            if self.mime_google_type_to_default_mime_type.__contains__(mimeType):
                request = self.service.files().export(fileId=file_id,
                                                      mimeType=self.mime_google_type_to_default_mime_type[mimeType])
            else:
                request = self.service.files().get_media(fileId=file_id)

            # request = self.service.files().export_media(fileId=file_id, mimeType=mimeType)

            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')

        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

        return file.getvalue(), file_info

    def get_file_names(self, count):
        results = self.service.files().list(
            pageSize=count, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

    def save_file(self, file_id, path='downloads'):
        data = self.download_file_data(real_file_id=file_id)
        file_name = f"{str(data[1]['name'])}"
        file_extension = self.mime_google_type_to_file_application[data[1]['mimeType']]
        file_path = os.path.join(path, f"{file_name}.{file_extension}")
        with open(file_path, 'wb+') as f:
            f.write(data[0])
