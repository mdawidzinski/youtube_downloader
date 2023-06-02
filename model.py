import os
from pytube import YouTube
import ffmpeg as ff
# TODO super długie nazwy plików: https://www.youtube.com/watch?v=aamHoDycjro
# TODO age restriction, https://www.youtube.com/watch?v=kgboGhzs3A4 WARNING
# TODO plik docelowy, schemat w jsonie ?

class YoutubeDownloaderModel:
    def get_video_duration(self, url):
        yt = YouTube(url)
        duration = int(yt.length)
        return duration

    def data(self, url):  # TODO dużo tego url
        yt = YouTube(url)
        title, autor = yt.title, yt.author  # extract title and autor
        file_name = f'{autor} - {title}.mp4'
        return yt, file_name

    def download_video(self, url):
        yt, file_name = self.data(url)
        video = yt.streams.get_highest_resolution()  # extract video from YouTube
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
        print(file_name)
        audio_name = audio_stream.download(filename=file_name)
        return audio_name

    def convert_to_mp3(self, audio_filename):
        audio_file_mp3 = audio_filename[:-4] + ".mp3"
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
        if end_time is None:
            ff.input(input_filename).output(output_filename, ss=start_time, acodec="copy").run()
        else:
            ff.input(input_filename).output(output_filename, ss=start_time, to=end_time, acodec="copy").run()

        os.remove(input_filename)
        os.rename(output_filename, base)
