import os
import json
import pytest
from utils.config_utils import load_data_from_json, save_data_to_json, create_folder
# TODO skrypt do testowania power shell ew. bash
# creating a valid temporary json file using pytest
@pytest.fixture
def valid_json_file(tmpdir):
    data = {'key': 'value'}
    file_path = tmpdir.join('valid.json')
    with open(file_path, 'w') as file:
        json.dump(data, file)
    return str(file_path)

# creating an invalid json temporary file using pytest
@pytest.fixture
def invalid_json_file(tmpdir):
    file_path = tmpdir.join('invalid.json')
    with open(file_path, 'w') as file:
        file.write('Invalid JSON')
    return str(file_path)


def test_load_data_from_json(valid_json_file, invalid_json_file):
    # testing a valid json file
    data = load_data_from_json(valid_json_file)
    assert data == {'key': 'value'}

    # testing a non-existent json file
    data = load_data_from_json('nonexistent.json')
    assert data == {}

    # testing an invalid json file
    data = load_data_from_json(invalid_json_file)
    assert data == 'Cannot decode json file'


def test_save_data_to_json(tmpdir):
    # testing saving date to json file
    data = {'key': 'value'}
    file_path = str(tmpdir.join('output.json'))
    save_data_to_json(data, file_path)
    assert os.path.exists(file_path)


def test_create_folder_success():
    # testing PermissionError
    folder_path = '../../restricted file/a'
    result = create_folder(folder_path)
    assert result == 'Lack of permission to create folder'

