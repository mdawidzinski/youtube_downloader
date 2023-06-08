import os
from pytube import YouTube
import ffmpeg as ff
import os.path as mypath  # allows work with path
from utils import config_utils
from tkinter import messagebox


# TODO problem z zerami, gdzie dodajemy błędy?
class YoutubeDownloaderModel:
    def __init__(self):
        self.audio_folder_path = ''
        self.video_folder_path = ''

    def get_video_duration(self, url):
        yt = YouTube(url)
        duration = int(yt.length)
        return duration

    def data(self, url):
        yt = YouTube(url)
        title, autor = yt.title, yt.author  # extract title and autor
        file_name = f'{autor} - {title}.mp4'
        return yt, file_name

    def download_video(self, url):

        yt, file_name = self.data(url)
        video = yt.streams.get_highest_resolution()  # extract video from YouTube

        folder_creation = config_utils.create_folder(self.video_folder_path)
        if folder_creation is not None:
            messagebox.showerror(folder_creation)

        file_name = mypath.join(self.video_folder_path, file_name)
        video.download(filename=file_name)  # download video

        return file_name

    def get_highest_bitrate_audio_stream(self, url):
        yt, file_name = self.data(url)
        audio_streams = yt.streams.filter(only_audio=True)
        audio_streams = sorted(audio_streams, key=lambda stream: int(stream.abr[:-4]), reverse=True)

        for audio_stream in audio_streams:
            if audio_stream.mime_type == 'audio/mp4':
                return audio_stream, file_name

    def download_mp4(self, url):
        audio_stream, file_name = self.get_highest_bitrate_audio_stream(url)

        folder_creation = config_utils.create_folder(self.video_folder_path)
        if folder_creation is not None:
            messagebox.showerror(folder_creation)

        file_name = mypath.join(self.audio_folder_path, file_name)
        audio_name = audio_stream.download(filename=file_name)

        return audio_name

    def convert_to_mp3(self, audio_filename):
        audio_file_mp3 = audio_filename[:-4] + '.mp3'
        (
            ff.input(audio_filename)
            .output(audio_file_mp3)
            .run()
        )
        os.remove(audio_filename)
        return audio_file_mp3

    def cut_file(self, input_filename, start_time, end_time):
        base = input_filename
        output_filename = 'temp.mp4'
        print(end_time, start_time)
        if end_time is None:
            ff.input(input_filename).output(output_filename, ss=start_time, acodec='copy').run()
        else:
            ff.input(input_filename).output(output_filename, ss=start_time, to=end_time, acodec='copy').run()

        os.remove(input_filename)
        os.rename(output_filename, base)
