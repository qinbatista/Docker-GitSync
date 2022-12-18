# -*- coding: utf-8 -*-
import S3Manager
import os
import platform
import zipfile
import threading
import time
import getpass

class GitSync:
    def __init__(self):
        self.__s3_manager = S3Manager.S3Manager()
        if platform.system() == "Darwin":
            self.__folder_path = f"/Users/qin/Desktop/GitRepositories"
            self.__file_path = f"/Users/{getpass.getuser()}/Desktop/logs.txt"
        else:
            self.__file_path = "/GitRepositories/GitSync.txt"
            self.__folder_path = f"/GitRepositories"
        self.__folder_list = ["qin"]

    def __log(self, result):
        if os.path.isfile(self.__file_path) == False:
            return
        with open(self.__file_path, "a+") as f:
            f.write(f"{str(result)}\n")
        if os.path.getsize(self.__file_path) > 1024 * 512:
            with open(self.__file_path, "r") as f:
                content = f.readlines()
                os.remove(self.__file_path)

    def _start_sync(self):
        while True:
            try:
                for folder in self.__folder_list:
                    _path = self.__folder_path+"/"+folder
                    _list = self.__find_all_folders_in_path(_path)
                    for _folder in _list:
                        _zip_path = self.__zip_folder(_path, _folder)
                        self.__s3_manager._sync_folder_zip(self.__folder_path, "/GitRepositories")
                        os.remove(_zip_path)
                time.sleep(6)
            except Exception as e:
                self.__log(f"[_sync_folder] failed:" + str(e))
                return []

    def __find_all_folders_in_path(self, _path):
        _folder_list = []
        files_and_dirs = os.listdir(_path)
        for entry in files_and_dirs:
            if os.path.isdir(_path+"/"+entry):
                _folder_list.append(entry)
        return _folder_list

    def __zip_folder(self, _path, _folder):
        with zipfile.ZipFile(_path+"/"+_folder + '.zip', 'w') as zip:
            # Add all files in the folder to the ZIP archive
            for file in os.listdir(os.path.join(_path, _folder)):
                zip.write(os.path.join(_path, _folder, file))
        return _path+"/"+_folder + '.zip'

    def _thread_SSR(self):
        thread_refresh = threading.Thread(target=self._start_sync, name="", args=())
        thread_refresh.start()


if __name__ == "__main__":
    qs = GitSync()
    qs._thread_SSR()
