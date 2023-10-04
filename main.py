import argparse
import json

import service
from yandex.yandex_drive_client import YandexDriveClient
from dropbox.dropbox_client import DropboxClient


def save_tokens(yandex_disk_token, dropbox_token):
    tokens = {
        "yandex_disk_token": yandex_disk_token,
        "dropbox_token": dropbox_token
    }

    with open("secrets/tokens.json", "w") as file:
        json.dump(tokens, file)


parser = argparse.ArgumentParser(description="Yandex.Disk and Dropbox CLI")

parser.add_argument("--save-tokens", action="store_true", help="Save tokens for Yandex.Disk and Dropbox.")
parser.add_argument("--yandex-disk-token", type=str, help="Access token for Yandex.Disk.")
parser.add_argument("--dropbox-token", type=str, help="Access token for Dropbox.")
parser.add_argument("--storage", type=str, default="yandex-disk", help="Choose storage: yandex-disk or dropbox.")
parser.add_argument("--token", type=str, help="Access token for the storage.")

parser.add_argument("--upload-file", type=str, help="Upload file to the storage.")
parser.add_argument("--download-file", type=str, help="Download file from the storage.")
parser.add_argument("--create-folder", type=str, help="Create folder on the storage.")
parser.add_argument("--upload-folder", type=str, help="Upload folder to the storage.")
parser.add_argument("--download-folder", type=str, help="Download folder from the storage.")
parser.add_argument("--list-files", action="store_true", help="List files and folders on the storage.")

args = parser.parse_args()

if args.storage == "yandex-disk":
    client = YandexDriveClient(service.get_yandex_drive_access_token() if args.token is None else args.token)
elif args.storage == "dropbox":
    client = DropboxClient(service.get_dropbox_access_token() if args.token is None else args.token)
else:
    print("Invalid storage selected!")
    exit(1)
print(client.__class__.__name__)

if args.upload_file:
    client.upload_file(args.upload_file)
elif args.download_file:
    client.download_file(args.download_file)
elif args.create_folder:
    client.create_folder(args.create_folder)
elif args.upload_folder:
    client.upload_folder(args.upload_folder)
elif args.download_folder:
    client.download_folder(args.download_folder)
elif args.list_files:
    files_and_folders = client.get_list_files_and_folders()
    print(files_and_folders)
elif args.save_tokens:
    if not args.yandex_disk_token or not args.dropbox_token:
        print("Please provide both Yandex.Disk token and Dropbox token.")
        exit(1)

    save_tokens(args.yandex_disk_token, args.dropbox_token)
    print("Tokens saved successfully.")
else:
    print("Invalid command!")
