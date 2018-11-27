from os import makedirs, walk
from os.path import isfile, join, splitext, realpath, abspath, dirname, exists
import sys 
from .FileSecurity import FileSecurity
import mimetypes

CLIENT_FOLDER_PATH = dirname(realpath(join(__file__, "../")))

class FileManager:
    def __init__(self, directory=CLIENT_FOLDER_PATH):
        self.directory = self.initialize_directory(directory)

    def get_all_files_in_dir(self, files_accepted):
        files = [f for root, dirs, files in walk(self.directory)
                    for f in files
                        if (splitext(f)[-1].replace('.', '') in files_accepted)]
        file_string = '\n'.join(files)
        return self.create_response(200, file_string);
    
    def get_file_content(self, file_path):
        if (FileSecurity.file_is_valid(self.directory, file_path)):
            file_to_read = join(self.directory, file_path)
            try:
                f = open(file_to_read, "r")
                content = f.read()
                return self.create_response(200, content, mimetypes.guess_type(file_to_read)[0])
            except FileNotFoundError:
                return self.create_response(404)
        return self.create_response(403)

    def post_file_content(self, file_path, new_content, overwrite=True):
        if (FileSecurity.file_is_valid(self.directory, file_path)):
            file_to_write = join(self.directory, file_path)
            if (not overwrite and isfile(file_to_write)):
                return self.create_response(409)
            else:
                status_code = 0
                try:
                    status_code = 200 if (exists(file_to_write)) else 201
                    f = open(file_to_write, 'w')
                    f.write(new_content)
                except:
                    status_code = 500
                return self.create_response(status_code)
        return self.create_response(403)

    def initialize_directory(self, directory):
        directory_path = join(CLIENT_FOLDER_PATH, directory)
        if (FileSecurity.file_is_valid(CLIENT_FOLDER_PATH, directory_path)):
            if not exists(directory_path):
                makedirs(directory_path)
            return directory_path
        else:
            raise ValueError('Invalid directory')

    def create_response(self, status_code, body='', mimetype='text/plain'):
        response = { 
            'content': body,
            'status': status_code,
            'mimetype': mimetype
        }
        return response