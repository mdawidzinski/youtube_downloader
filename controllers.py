import os
from tkinter import messagebox
from tkinter import filedialog
from utils import config_utils


CONFIG_FILE = 'configs/config.json'


class PathController:
    def __init__(self, model, logger):
        self.model = model
        self.logger = logger

        self.default_file_paths = {
            'audio': 'download/audio',
            'video': 'download/video'
        }

        if not os.path.exists('configs'):
            os.makedirs('configs')

        self.file_paths = config_utils.load_data_from_json(CONFIG_FILE)

        for key, value in self.default_file_paths.items():
            if key in self.file_paths:
                self.default_file_paths[key] = self.file_paths[key]
            else:
                self.file_paths[key] = value

        config_utils.save_data_to_json(self.file_paths, CONFIG_FILE)

    def folder_path_set(self):
        path_dict = config_utils.load_data_from_json(CONFIG_FILE)
        for key, value in path_dict.items():
            if key == 'video':
                self.model.video_folder_path = value
            else:
                self.model.audio_folder_path = value

    def select_save_path(self, file_key):
        initial_dir = self.file_paths.get(file_key, None)
        save_path = filedialog.askdirectory(initialdir=initial_dir)
        if save_path:
            self.file_paths[file_key] = save_path
            config_utils.save_data_to_json(self.file_paths, CONFIG_FILE)


class YoutubeDownloaderController:
    def __init__(self, model, logger):
        self.model = model
        self.logger = logger

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
            file_name = self.model.download_video(url)
            if split:
                self.model.cut_file(file_name, start_time, end_time)
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
        if end_time >= duration:
            messagebox.showwarning('Warning', 'end_time >= duration')
            return 'Time Error', 'Time Error'

        return self.time_convert(s_time, e_time)

    @staticmethod
    def time_convert(s_time, e_time):
        start_time = '00:00:00'
        end_time = None
        if s_time != ('00', '00', '00'):
            start_time = '%s:%s:%s' % (s_time[0], s_time[1], s_time[2])
        if e_time != ('00', '00', '00'):
            end_time = '%s:%s:%s' % (e_time[0], e_time[1], e_time[2])
        return start_time, end_time

    @staticmethod
    def task_done(filename):
        messagebox.showinfo('Download Complete', 'File downloaded: %s' % filename)
