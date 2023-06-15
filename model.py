import os
from pytube import YouTube
import ffmpeg as ff
import os.path as mypath  # allows work with path
from utils import config_utils
from tkinter import messagebox


# TODO super długie nazwy plików: https://www.youtube.com/watch?v=aamHoDycjro


class YoutubeDownloaderModel:
    def __init__(self, logger):
        self.logger = logger
        self.audio_folder_path = ''
        self.video_folder_path = ''
        self.temp = ''

    #  TODO zbiorcza funkcja dla youtuba

    @staticmethod
    def get_video_duration(url):
        yt = YouTube(url)
        duration = int(yt.length)
        return duration

    @staticmethod
    def data(url):
        yt = YouTube(url)
        title, autor = yt.title, yt.author  # extract title and author
        file_name = f'{autor} - {title}.mp4'
        return yt, file_name

    def download_video(self, url, split=False):
        yt, file_name = self.data(url)
        video = yt.streams.get_highest_resolution()  # extract video from YouTube

        folder_creation = config_utils.create_folder(self.video_folder_path)
        if folder_creation is not None:
            messagebox.showerror(folder_creation)

        if not split:
            file_path_name = mypath.join(self.video_folder_path, file_name)

        else:
            file_path_name = mypath.join(self.temp, file_name)

        if os.path.exists(file_path_name):
            file_path_name = config_utils.set_file_name(file_path_name)

        video.download(filename=file_path_name)  # download video TODO try/except

        return file_path_name, file_name

    def get_highest_bitrate_audio_stream(self, url):
        yt, file_name = self.data(url)
        audio_streams = yt.streams.filter(only_audio=True)
        audio_streams = sorted(audio_streams, key=lambda stream: int(stream.abr[:-4]), reverse=True)

        for audio_stream in audio_streams:
            if audio_stream.mime_type == 'audio/mp4':
                return audio_stream, file_name

    def download_mp4(self, url, split=False):
        audio_stream, file_name = self.get_highest_bitrate_audio_stream(url)

        folder_creation = config_utils.create_folder(self.audio_folder_path)

        if folder_creation is not None:
            messagebox.showerror(folder_creation)

        if not split:
            file_path_name = mypath.join(self.audio_folder_path, file_name)
        else:
            file_path_name = mypath.join(self.temp, file_name)

        if os.path.exists(file_path_name):
            file_path_name = config_utils.set_file_name(file_path_name)

        audio_stream.download(filename=file_path_name)  # TODO try/except

        return file_path_name, file_name

    def convert_to_mp3(self, audio_file_name, file_name, split=False):
        base_file_name = file_name[:-4]
        path = self.audio_folder_path
        if split:
            path = self.temp

        audio_file_mp3 = f'{path}/{base_file_name}.mp3'

        if os.path.exists(audio_file_mp3):
            number = 1
            while os.path.exists(f'{path}/{base_file_name}({number}).mp3'):
                number += 1
            audio_file_mp3 = f'{path}/{base_file_name}({number}).mp3'

        try:
            (
                ff.input(audio_file_name)
                .output(audio_file_mp3)
                .run()
            )
        except Exception as e:
            return e

        os.remove(audio_file_name)
        file_name = f'{base_file_name}.mp3'

        return audio_file_mp3, file_name

    def push_error(self, method_name: str, message: str, msg_param: str, title: str):
        """ Concatenates given params into log entry and shown msgbox with error. """
        error_msg = f'{message}: {msg_param}'
        log_entry = f'[model][{method_name}] {error_msg}'
        self.logger.error(log_entry)
        messagebox.showerror(title, error_msg)

    def cut_file(self, input_filename, file_name, start_time, end_time, video=True):
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

        try:
            if end_time is None:
                ff.input(input_filename).output(output_filename, ss=start_time, acodec='copy').run()
            else:
                ff.input(input_filename).output(output_filename, ss=start_time, to=end_time, acodec='copy').run()
        except ValueError:
            self.push_error('cut_file', 'File name was wrong', input_filename, 'Error in processing')
            return None
        except FileNotFoundError:
            self.push_error('cut_file', 'Original file was not found.', '\nPossibly disruption in connection.',
                            'Error in processing')
            return None
        except Exception as e:
            self.push_error('cut_file', 'Unknown exception', str(e), 'Error in processing')
            return None
        else:
            self.logger.debug(f'[model][cut_file] Successfully cut file: {input_filename}')

        try:
            os.remove(input_filename)
        except NotImplementedError:
            self.push_error('cut_file', 'Removing files is unavailable in this OS', '', 'Limited OS')
            return None
        except Exception as e:
            self.push_error('cut_file', 'Unknown exception', f'{str(e)}', 'Error in processing')
            return None
        else:
            self.logger.debug(f'[model][cut_file] Successfully cut file: {input_filename}')

        return output_filename
