from zlib import compress, decompress
from pickle import dumps, loads

from os import listdir, mkdir
from os.path import join, isfile, isdir

class File:
    def __init__(self, filename, filepath, filedata):
        self.filename = filename
        self.filepath = filepath
        self.filedata = filedata

class Directory:
    def __init__(self, dirname, dirpath):
        self.dirname = dirname
        self.dirpath = dirpath

        self.subdirectories: list[Directory] = []
        self.files: list[File] = []

def create(dirname, path):
    directory = Directory(dirname, path)
    for item in listdir(path):
        item_path = join(path, item)
        if isfile(item_path):
            with open(item_path, "rb") as filestream:
                compressed_data = compress(filestream.read())
                file = File(item, item_path, compressed_data)
            directory.files.append(file)
        elif isdir(item_path):
            subdirectory = create(item, item_path)
            directory.subdirectories.append(subdirectory)

    return directory

def archive(directory):
    with open(directory.dirname+".bin", "wb") as compressed_file:
        directory_bytes = dumps(directory)
        compressed_bytes = compress(directory_bytes, level=9)
        compressed_file.write(compressed_bytes)

def unarchive(directory):

    mkdir(directory.dirpath)

    for file in directory.files:
        with open(file.filepath, "wb") as filestream:
            filestream.write(decompress(file.filedata))

    for subdirectory in directory.subdirectories:
        unarchive(subdirectory)

if __name__ == "__main__":
    # 1) Archiving directories
    path = "a"
    directory = create(path, "a")
    archive(directory)

    # 2) Unarchiving directories
    path = "a.bin"
    with open(path, "rb") as compressed_file:
        directory_bytes = decompress(compressed_file.read())
        directory = loads(directory_bytes)

    unarchive(directory)