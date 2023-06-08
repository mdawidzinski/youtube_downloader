import json
import os


def load_data_from_json(json_file):
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


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
    except OSError as e:
        return f"Nie można utworzyć folderu: {folder_path}. Błąd: {str(e)}"
