import json
import os


# Podawać nazwy plików, których dotyczy błąd?
def load_data_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return f'Cannot decode json file'
    except PermissionError:
        return f'No permission to load file'
    except IsADirectoryError:
        return f'{json_file} is a directory, not a file'
    except UnicodeDecodeError:
        return f'Error decoding {json_file}: invalid encoding'
    except Exception as e:
        return f'Error occurred: {str(e)}'


def save_data_to_json(data, json_file):
    try:
        with open(json_file, 'w') as file:
            json.dump(data, file)
    except PermissionError:
        return f'Lack of permission to save the file'
    except TypeError:
        return f'Cannot convert data to json format'
    except Exception as e:
        return f'Error occurred: {str(e)}'


def create_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except PermissionError:
        return f'Lack of permission to create folder'
    except Exception as e:
        return f'Error occurred:{str(e)}'
