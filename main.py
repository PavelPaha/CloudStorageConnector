import fileDownloader

if __name__ == '__main__':
    downloader = fileDownloader.Downloader()
    file_id = '1-74-JwelSUzVxUCUblThfs9AtuFr_QdFZ1RFrbluxW0'
    downloader.save_file(file_id)
    downloader.get_file_names(100)
