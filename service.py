import json
import os.path
import shutil
import tarfile


def clear_downloads():
    downloads_dir = get_downloads_dir()
    if os.path.exists(downloads_dir):
        shutil.rmtree(downloads_dir)


def take_action(func):
    # clear_downloads()

    def wrapper(*args):
        try:
            func(*args)
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    return wrapper


def operation_status(operation_name):
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{operation_name} started.")
            result = func(*args, **kwargs)
            print(f"{operation_name} completed successfully.")
            return result

        return wrapper

    return decorator


def get_yandex_drive_access_token():
    try:
        with open(os.path.join(get_proj_dir(), 'secrets', 'tokens.json')) as token:
            return json.load(token)["yandex-disk-token"]
    except Exception as e:
        print(f"Не установлен токен, {e}")


def get_dropbox_access_token():
    try:
        p = os.path.join(get_proj_dir(), 'secrets', 'tokens.json')
        with open(p) as file:
            json_data = json.load(file)
            return json_data['dropbox-token']
    except Exception as e:
        print(f"Не установлен токен, {e}")


def get_proj_dir():
    absolute_file_path = os.path.realpath(__file__)
    dir_name = os.path.dirname(absolute_file_path)
    return dir_name


def get_downloads_dir():
    return os.path.join(get_proj_dir(), 'Downloads')


def size_limit_exceeded(path, threshold_size=10 * 1024 * 1024):
    size = get_size(path)
    return size > threshold_size


def is_archive(path):
    extension = os.path.splitext(path)[1]
    return extension in [".tar.gz", ".tar", ".gz"]


def archive(path):
    if is_archive(path):
        return path
    archive_path = f"{os.path.splitext(path)[0]}.tar.gz"
    archive_directory(path, archive_path)
    print(f"Archived {path} to {archive_path}.")
    return archive_path


def get_size(path):
    total_size = 0
    if os.path.isfile(path):
        total_size = os.path.getsize(path)
    else:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
    return total_size


def archive_directory(directory_path, archive_path):
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(directory_path, arcname=os.path.basename(directory_path))
