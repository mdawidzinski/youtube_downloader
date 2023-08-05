import sys
from typing import Tuple
from typing import Union
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic


TimeFormat = str


class YoutubeDownloaderGui(QMainWindow):
    """Main GUI window for the YouTube downloader application."""

    def __init__(self, controller, path_controller):
        super().__init__()
        self.controller = controller
        self.path_controller = path_controller

        uic.loadUi("youtube downloader.ui", self)  # load GUI from file

        # connect GUI elements to methods
        self.download_button.clicked.connect(self.download)
        self.get_data_button.clicked.connect(self.set_data)
        self.video_path.triggered.connect(self.select_video_path)
        self.audio_path.triggered.connect(self.select_audio_path)

    def select_video_path(self) -> None:
        """Open a FileDialog to select save path for video"""
        self.path_controller.select_save_path("video")

    def select_audio_path(self) -> None:
        """Open a FileDialog to select save path for audio"""
        self.path_controller.select_save_path("audio")

    def get_url(self) -> Union[str, None]:
        """Retrieve YouTube url entered by user"""
        url = self.url_entry.text()
        if not url:
            QMessageBox.warning(None, "No url", "Please enter youtube link.")
            return None
        return url

    def get_author_and_title_from_entry(self) -> Tuple[str, str]:
        """Retrieve author and title from respective entry's"""
        author = self.author_entry.text()
        title = self.title_entry.text()
        return author, title

    def get_format(self) -> str:
        """Retrieve the selected file format"""
        format_type = self.format_box.currentText()
        return format_type

    def get_time(self) -> Tuple[TimeFormat, TimeFormat]:
        """Retrieve start and end time for the video"""
        start_time = self.start_time.time().toString("hh:mm:ss")
        end_time = self.end_time.time().toString("hh:mm:ss")
        return start_time, end_time

    def get_author_and_title_from_url(self) -> Tuple[str, str]:
        """Retrieve author and title from YouTube video using provided url """
        url = self.get_url()
        if url is None:
            return "", ""
        else:
            author, title = self.controller.get_author_and_title(url)
        return author, title

    def set_author_and_title(self, author: str, title: str) -> None:
        """Set author and title in respective entry fields"""
        self.author_entry.setText(author)
        self.title_entry.setText(title)

    def clear_author_and_title(self) -> None:
        """Clear author and title entry fields"""
        self.author_entry.clear()
        self.title_entry.clear()

    def set_data(self) -> None:
        """Set author and title based on the YouTube url.

        This method fetches the YouTube url from entry field and use controller method to obtain
        author and title from YouTube video. Then it sets the values in respective entry fields"""
        author, title = self.get_author_and_title_from_url()
        if author is None or title is None:
            return

        self.set_author_and_title(author, title)

    def download(self) -> None:
        """Handle the Download button click event.

        Method is called when download_button is clicked. It collects all the necessary data from GUI.
        Then passes it to controller download method to initiate downloading process."""
        url = self.get_url()
        if url is None:
            return

        start_time = self.start_time.time().toString("hh:mm:ss")
        end_time = self.end_time.time().toString("hh:mm:ss")
        selected_option = self.format_box.currentText()
        author, title = self.get_author_and_title_from_entry()

        if not author or not title:  # if user didn't input author and title it collect data from YouTube.
            author, title = self.get_author_and_title_from_url()

        if author and title:
            self.path_controller.folder_path_set()  # ensure that file is downloaded to correct folder
            self.controller.download(url, selected_option, start_time, end_time, author, title)
