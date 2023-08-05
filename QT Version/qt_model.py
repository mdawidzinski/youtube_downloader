import os
from typing import Union, Tuple, Optional
from PyQt5.QtWidgets import QMessageBox
from pytube import YouTube, Stream
from pytube.exceptions import RegexMatchError
import ffmpeg as ff
import os.path as mypath  # allows work with path
from utils import config_utils


class YoutubeDownloaderModel:
    """Class that handle downloading process and acquiring data from YouTube."""
    def __init__(self):
        self.audio_folder_path = ''
        self.video_folder_path = ''
        self.temp = ''
        self.url = ''
        self.file_name = ''

    def get_yt(self) -> Union[YouTube, None]:
        """Get YouTube object based on provided url"""
        try:
            yt = YouTube(self.url)
            return yt
        except RegexMatchError:
            QMessageBox.warning(None, 'Warning', f"Cannot find YouTube video")
            return None
        except Exception as e:
            print(e)
            QMessageBox.warning(None, 'Error', f'Something went wrong {e}')
            return None

    def get_author_and_title(self) -> Tuple[str, str]:
        """Retrieve author and title from YouTube"""
        yt = self.get_yt()
        if yt is not None:
            author, title = yt.author, yt.title
            return author, title
        else:
            return "", ""

    def get_video_duration(self) -> int:
        """Retrieve YouTube video duration."""
        yt = self.get_yt()
        duration = int(yt.length)
        return duration

    def download_video(self, start_time: str, end_time: str, split: bool) -> str:
        """Method responsible for downloading video.

        If split is true it use ffmpeg to cut downloaded file."""
        yt = self.get_yt()
        file_name = self.file_name

        video = yt.streams.get_highest_resolution()  # extract video from YouTube

        folder_creation = config_utils.create_folder(self.video_folder_path)

        if folder_creation is not None:
            return QMessageBox.warning(None, 'warning', folder_creation)

        if not split:
            file_path_name = mypath.join(self.video_folder_path, file_name)
        else:
            file_path_name = mypath.join(self.temp, file_name)

        if os.path.exists(file_path_name):
            file_path_name = config_utils.set_file_name(file_path_name)

        video.download(filename=file_path_name)

        if split:
            file_path_name = self.cut_file(file_path_name, file_name, start_time, end_time)

        return file_path_name

    def get_highest_bitrate_audio_stream(self) -> Optional[Stream]:
        """Method returned audio stream with highest bitrate"""
        yt = self.get_yt()
        audio_streams = yt.streams.filter(only_audio=True)

        audio_streams = sorted(audio_streams, key=lambda stream: int(stream.abr[:-4]), reverse=True)

        for audio_stream in audio_streams:
            if audio_stream.mime_type == 'audio/mp4':
                return audio_stream

    def download_mp4(self, start_time: str, end_time: str, split: bool) -> str:
        """Method responsible for downloading video.

        If split is true it use ffmpeg to cut downloaded file."""
        file_name = self.file_name

        audio_stream = self.get_highest_bitrate_audio_stream()

        folder_creation = config_utils.create_folder(self.audio_folder_path)

        if folder_creation is not None:
            QMessageBox.critical(None, 'Error', folder_creation)

        if not split:
            file_path_name = mypath.join(self.audio_folder_path, file_name)
        else:
            file_path_name = mypath.join(self.temp, file_name)

        if os.path.exists(file_path_name):
            file_path_name = config_utils.set_file_name(file_path_name)

        audio_stream.download(filename=file_path_name)

        if split:

            file_path_name = self.cut_file(file_path_name, file_name, start_time, end_time, False)

        return file_path_name

    def convert_to_mp3(self, audio_file_name: str) -> Union[str, None]:
        """Method that use ffmpeg to convert mp4 file to mp3"""
        base_file_name = self.file_name[:-4]
        path = self.audio_folder_path

        audio_file_mp3 = f'{path}/{base_file_name}.mp3'

        if os.path.exists(audio_file_mp3):  # if file name exist for mp fill add and number i parenthesis at end
            number = 1
            while os.path.exists(f'{path}/{base_file_name}({number}).mp3'):
                number += 1
            audio_file_mp3 = f'{path}/{base_file_name}({number}).mp3'

        try:  # try to convert file
            (
                ff.input(audio_file_name)
                .output(audio_file_mp3)
                .run()
            )
        except Exception as e:
            os.remove(audio_file_name)
            QMessageBox.warning(None, 'Warning', f'Something went wrong during file conversion to mp3 {e}')
            return None

        os.remove(audio_file_name)

        return audio_file_mp3

    def cut_file(self, input_filename: str, file_name: str, start_time: str, end_time: str, video=True) -> (
            Union)[str, None]:
        """Method that cut file according start and end time"""
        path = self.video_folder_path

        if not video:
            path = self.audio_folder_path

        base_name = file_name[:-4]
        extension = file_name[-4:]

        output_filename = f'{path}/{base_name}{extension}'

        if os.path.exists(output_filename):
            number = 1
            while os.path.exists(f'{path}/{base_name}({number}){extension}'):
                number += 1
            output_filename = f'{path}/{base_name}({number}){extension}'

        try:  # try cut file
            if end_time is None:
                ff.input(input_filename).output(output_filename, ss=start_time, acodec='copy').run()
            else:
                ff.input(input_filename).output(output_filename, ss=start_time, to=end_time, acodec='copy').run()
        except Exception as e:
            QMessageBox.warning(None, 'Warning', f'Somethings went wrong during cutting file: {e}')
            os.remove(input_filename)
            return None

        os.remove(input_filename)

        return output_filename
