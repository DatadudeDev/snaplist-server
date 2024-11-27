import os

def remove_files(*file_paths):
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except Exception as error:
            print('failed to delete the requested file(s)')