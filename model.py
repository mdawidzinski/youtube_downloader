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


    #  TODO zbiorcza funkcja dla youtuba

    @staticmethod
    def get_video_duration(url):
        yt = YouTube(url)  # TODO to się powtarza i try/except
        duration = int(yt.length)
        return duration

    @staticmethod
    def data(url):
        yt = YouTube(url)  # TODO to się powtarza i try/except
        title, autor = yt.title, yt.author  # extract title and author
        file_name = f'{autor} - {title}.mp4'
        return yt, file_name

    def download_video(self, url):

        yt, file_name = self.data(url)
        video = yt.streams.get_highest_resolution()  # extract video from YouTube

        folder_creation = config_utils.create_folder(self.video_folder_path)
        if folder_creation is not None:
            messagebox.showerror(folder_creation)

        file_name = mypath.join(self.video_folder_path, file_name)

        if os.path.exists(file_name):
            file_name = config_utils.set_file_name(file_name)

        video.download(filename=file_name)  # download video TODO try/except

        return file_name

    def get_highest_bitrate_audio_stream(self, url):
        yt, file_name = self.data(url) # TODO to też w teorii się powtarza
        audio_streams = yt.streams.filter(only_audio=True)
        audio_streams = sorted(audio_streams, key=lambda stream: int(stream.abr[:-4]), reverse=True)

        for audio_stream in audio_streams:
            if audio_stream.mime_type == 'audio/mp4':
                return audio_stream, file_name

    def download_mp4(self, url):
        audio_stream, file_name = self.get_highest_bitrate_audio_stream(url)

        folder_creation = config_utils.create_folder(self.audio_folder_path)
        if folder_creation is not None:
            messagebox.showerror(folder_creation)

        file_name = mypath.join(self.audio_folder_path, file_name)

        if os.path.exists(file_name):
            file_name = config_utils.set_file_name(file_name)

        audio_stream.download(filename=file_name)  # TODO try/except

        return file_name

    @staticmethod
    def convert_to_mp3(audio_file_name):  # TODO to musowo w try/except

        basename = os.path.splitext(audio_file_name)[0]
        audio_file_mp3 = f'{basename}.mp3'

        try:
            if os.path.exists(audio_file_mp3):
                number = 1
                while os.path.exists(f'{basename}({number}).mp3'):
                    number += 1
                audio_file_mp3 = f'{basename}({number}).mp3'
        except Exception as e:
            return e

        (
            ff.input(audio_file_name)
            .output(audio_file_mp3)
            .run()
        )
        os.remove(audio_file_name)

        return audio_file_mp3

    @staticmethod
    def cut_file(input_filename, start_time, end_time):
        base = input_filename
        output_filename = 'temp.mp4'
        # TODO jeden try/except
        if end_time is None:
            ff.input(input_filename).output(output_filename, ss=start_time, acodec='copy').run()
        else:
            ff.input(input_filename).output(output_filename, ss=start_time, to=end_time, acodec='copy').run()
        # TODO drugi
        os.remove(input_filename)
        os.rename(output_filename, base)
