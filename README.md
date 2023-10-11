Использование

Следующие ключи осуществляют различные функции:

--save-tokens: Сохраняет токены для Yandex.Disk и Dropbox.

--yandex-disk-token: Укажите токен доступа для Yandex.Disk.

--dropbox-token: Укажите токен доступа для Dropbox.

--storage: Выберите хранилище: yandex-disk или dropbox.

--token: Укажите токен доступа для хранилища.

--upload-file: Загрузить файл в хранилище.

--download-file: Скачать файл из хранилища.

--create-folder: Создать папку в хранилище.

--upload-folder: Загрузить папку в хранилище.

--download-folder: Скачать папку из хранилища.

--list-files: Получить список файлов и папок.

Примеры использования.

Сохранить токены:
python main.py --save-tokens --yandex-disk-token <yandex-disk-token> --dropbox-token <dropbox-token>

Загрузить файл в Yandex.Disk:
python main.py --storage yandex-disk --token <yandex-disk-token> --upload-file <path_to_file>

Скачать файл из Dropbox:
python main.py --storage dropbox --token <dropbox-token> --download-file <path_to_file>