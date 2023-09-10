import os
from typing import Tuple
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from utils import config_utils

CONFIG_FILE = '../configs/qt_config.json'


class PathController:
    """Class that handle a file saving directory."""
    def __init__(self, model):
        self.model = model
        self.temp_folder = 'temp'
        self.model.temp = self.temp_folder

        self.default_file_paths = {
            'audio': 'download/audio',
            'video': 'download/video'
        }

        if not os.path.exists('../configs'):  # create config file in not exist.
            os.makedirs('../configs')

        self.file_paths = config_utils.load_data_from_json(CONFIG_FILE)  # open config file as dictionary

        for key, value in self.default_file_paths.items():  # fill empty config file with data
            if key not in self.file_paths:
                self.file_paths[key] = value

        config_utils.save_data_to_json(self.file_paths, CONFIG_FILE)

        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder)

    def folder_path_set(self) -> None:
        """Retrieve save folder directory from config file and set it in model"""
        path_dir = config_utils.load_data_from_json(CONFIG_FILE)
        for key, value in path_dir.items():
            if key == 'video':
                self.model.video_folder_path = value
            else:
                self.model.audio_folder_path = value

    def select_save_path(self, file_key: str) -> None:
        """Allows change save folder directory for chosen file type"""
        initial_dir = self.file_paths.get(file_key, None)
        save_path = QFileDialog.getExistingDirectory(directory=initial_dir)
        if save_path:
            self.file_paths[file_key] = save_path
            config_utils.save_data_to_json(self.file_paths, CONFIG_FILE)


class YoutubeDownloaderController:
    """Class that prepare downloading proce and acquiring data from YouTube"""
    def __init__(self, model):
        self.model = model

    def set_url(self, url: str) -> None:
        """Passes url to model"""
        self.model.url = url

    def get_author_and_title(self, url: str) -> Tuple[str, str]:
        """Retrieve author and title from YouTube using provided url"""
        self.set_url(url)
        author, title = self.model.get_author_and_title()
        return author, title

    @staticmethod
    def create_filename(author: str, title: str) -> str:
        """Create file name using provided author and title"""
        file_name = f'{author} - {title}.mp4'
        return file_name

    def set_filename(self, author: str, title: str) -> None:
        """Set file name in model"""
        file_name = self.create_filename(author, title)
        self.model.file_name = file_name

    def download(self, url: str, format_type: str, start_time: str, end_time: str, author: str, title: str) -> None:
        """Set up download process using provided data from GUI"""
        self.set_url(url)
        yt = self.model.get_yt()

        if yt is not None:
            self.set_filename(author, title)

            format_type = format_type
            split = False
            error = False
        
            if start_time != "00:00:00" or end_time != "00:00:00":
                split = True

            if split:
                error = self.time_check(start_time, end_time)

            if not error:
                if "video" in format_type:
                    file_path_name = self.model.download_video(start_time, end_time, split)
                    if file_path_name is not None:
                        QMessageBox.information(None, 'Done', f'File {file_path_name} downloaded.')
                elif "mp4" in format_type:
                    file_path_name = self.model.download_mp4(start_time, end_time, split)
                    if file_path_name is not None:
                        QMessageBox.information(None, 'Done', f'File {file_path_name} downloaded.')
                elif "mp3" in format_type:
                    file_path_name = self.model.download_mp4(start_time, end_time, split)
                    file_path_name = self.model.convert_to_mp3(file_path_name)
                    if file_path_name is not None:
                        QMessageBox.information(None, 'Done', f'File {file_path_name} downloaded.')


    @staticmethod
    def int_to_time(time: int) -> str:
        """Convert time integer to string"""
        hours = time // 3600
        rest = time % 3600
        minutes = rest // 60
        seconds = rest % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def time_check(self, start_time: str, end_time: str) -> bool:
        """Compare download start, end time provided by user and file duration from YouTube"""
        duration_in_sec = self.model.get_video_duration()
        duration = self.int_to_time(duration_in_sec)

        if start_time >= end_time:
            QMessageBox.warning(None, "Warning", "Start time >= End time.")
            return True
        elif start_time >= duration:
            QMessageBox.warning(None, "Warning", "Start time >= duration.")
            return True
        elif end_time >= duration:
            QMessageBox.warning(None, "Warning", "End time >= duration.")
            return True
        return False
