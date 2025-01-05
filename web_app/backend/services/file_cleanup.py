# web_app/backend/services/file_cleanup.py

import os
import shutil

def remove_files_in_folder(folder, file_list):
    """
    Attempts to remove each filename in 'file_list' from 'folder'.
    Ignores if missing.
    """
    for f in file_list:
        path = os.path.join(folder, f)
        if os.path.exists(path):
            os.remove(path)
