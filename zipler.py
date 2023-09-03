import zipfile


def create_zip_archive(file_paths, zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for file_path in file_paths:
            zipf.write(file_path)


# Пример использования
file_paths = ['ability_000.py', 'requirements.txt', 'index.py', 'reactions.py']
zip_file_name = 'Tutu2Alice.zip'
create_zip_archive(file_paths, zip_file_name)
