from  google_drive_downloader import GoogleDriveDownloader
from google_drive_uploader import GoogleDriveUploader

import io
from googleapiclient.http import MediaIoBaseDownload

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

if __name__ == '__main__':
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly',
              'https://www.googleapis.com/auth/drive.file',
              'https://www.googleapis.com/auth/drive']
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

    service = build('drive', 'v3', credentials=creds)

    # folder_list = service.ListFile({'q': "trashed=false"}).GetList()
    # for folder in folder_list:
    #     print('folder title: %s, id: %s' % (folder['title'], folder['id']))

    # downloader = GoogleDriveDownloader(service)
    # downloader.save('1kIYt4Xa0fPt-MC5k04XQoSci8RoX3Ibu')
    # # #
    uploader = GoogleDriveUploader(service)
    uploader.upload_basic('1.jpeg', '1.jpeg')
    uploader.upload_folder_to_drive(r"C:\Users\MagicBook\Documents\GitHub\CloudStorageConnector\some")
    # uploader.upload_file_to_specific_folder('1Lcf-IdE80tcYMTA9Q05gYceyU8RJySvc', '1.jpeg')
