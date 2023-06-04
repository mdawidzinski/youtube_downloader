from tkinter import messagebox
from tkinter import filedialog
import json

CONFIG_FILE = 'config.json'  # TODO gdzie to upchnąć?


class PathController:
    def __init__(self, model):
        self.model = model

        self.default_file_paths = {
            'audio': 'download/audio',
            'video': 'download/video'
        }
        self.file_paths = self.load_paths_from_config()

        for key, value in self.default_file_paths.items():
            if key in self.file_paths:
                self.default_file_paths[key] = self.file_paths[key]
            else:
                self.file_paths[key] = value

        self.save_paths_to_config()

    def save_paths_to_config(self):
        with open(CONFIG_FILE, 'w') as file:
            json.dump(self.file_paths, file)

    def load_paths_from_config(self):
        try:
            with open(CONFIG_FILE, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def folder_path_set(self):
        path_dict = self.load_paths_from_config()
        for key, value in path_dict.items():
            if key == 'video':
                self.model.video_folder_path = value
            else:
                self.model.audio_folder_path = value

    def select_save_path(self, file_key):
        initial_dir = self.file_paths.get(file_key, None)  # Pobranie obecnej ścieżki jako initialdir
        save_path = filedialog.askdirectory(initialdir=initial_dir)
        if save_path:
            self.file_paths[file_key] = save_path
            self.save_paths_to_config()


class YoutubeDownloaderController:
    def __init__(self, model):
        self.model = model

    def download(self, url, format_type, s_time, e_time):
        video = True
        mp3 = False
        split = False

        if 'video' not in format_type:
            video = False
        if 'mp3' in format_type:
            mp3 = True
        if s_time != ('00', '00', '00') or e_time != ('00', '00', '00'):
            split = True

        start_time, end_time = self.time_check(url, s_time, e_time)
        if start_time == 'Time Error':
            return

        file_name = ''
        if video:
            file_name = self.model.download_video(url)  # ściąga video
            if split:
                self.model.cut_file(file_name, start_time, end_time)  # tnie pobrany plik, zostawia ucięty i kasuje cały
        else:
            file_name = self.model.download_mp4(url)
            if mp3:
                file_name = self.model.convert_to_mp3(file_name)
                if split:
                    self.model.cut_file(file_name, start_time, end_time)
            else:
                if split:
                    self.model.cut_file(file_name, start_time, end_time)

        self.task_done(file_name)

    def time_check(self, url, s_time, e_time):
        start_time = sum(int(t) * 60 ** i for i, t in enumerate(s_time[::-1]))
        end_time = sum(int(t) * 60 ** i for i, t in enumerate(e_time[::-1]))
        duration = self.model.get_video_duration(url)

        if start_time > end_time:
            if end_time > 0:
                messagebox.showwarning('Warning', 'start_time > end_time')
                return 'Time Error', 'Time Error'
        if start_time >= duration:
            messagebox.showwarning('Warning', 'start_time >= duration')
            return 'Time Error', 'Time Error'
        if end_time >= duration:  # TODO zapytanie czy end = duration
            messagebox.showwarning('Warning', 'end_time >= duration')
            return 'Time Error', 'Time Error'

        return self.time_convert(s_time, e_time)

    def time_convert(self, s_time, e_time):
        start_time = None
        end_time = None
        if s_time != ('00', '00', '00'):
            start_time = '%s:%s:%s' % (s_time[0], s_time[1], s_time[2])
        if e_time != ('00', '00', '00'):
            end_time = '%s:%s:%s' % (e_time[0], e_time[1], e_time[2])
        return start_time, end_time

    def task_done(self, filename):
        messagebox.showinfo('Download Complete', 'File downloaded: %s' % filename)