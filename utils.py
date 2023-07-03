from config import ACCEPTABLE_FILE_TYPES

def is_acceptable_file_type(file):
    for fileType in ACCEPTABLE_FILE_TYPES:
        if file.endswith(fileType):
            return True
    return False

