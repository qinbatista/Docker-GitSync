# -*- coding: utf-8 -*-
import S3Manager
import os
import platform
class GitSync:
    def __init__(self):
        self.__s3_manager = S3Manager.S3Manager()
        if platform.system() == "Darwin":
            self.__file_path = f"/GitRepositories"
        else:
            self.__file_path = f"/Users/{getpass.getuser()}/Desktop/download/logs.txt"
    def _start(self):
        for root, dirs, files in os.walk(self.__file_path):
            for folder in dirs:
                # Create a ZIP file for each folder
                with zipfile.ZipFile(folder + '.zip', 'w') as zip:
                    # Add all files in the folder to the ZIP archive
                    for file in os.listdir(os.path.join(root, folder)):
                        zip.write(os.path.join(root, folder, file))


if __name__ == "__main__":
    print("v1")
    qs = GitSync()
    qs._start()
