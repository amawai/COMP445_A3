from os.path import join, realpath, abspath
import sys 

class FileSecurity:
    @staticmethod
    def is_public_path(basedir, path, follow_symlinks=True):
        if follow_symlinks:
            return realpath(path).startswith(basedir)
        return abspath(path).startswith(basedir)

    @staticmethod
    def file_is_valid(base_dir, file_path):
        public_abs_path = abspath(base_dir)
        path_to_check = join(base_dir, file_path)
        return FileSecurity.is_public_path(public_abs_path, path_to_check)