from tkinter import *
from tkinter.ttk import Combobox


# TODO in progres.. progress bar
# TODO invalid link WARNING
bg_color = '#9DF1DF'

# TODO cleary dla time entry
class DownloaderGui:
    def __init__(self, root, controller, path_controller, logger):
        self.root = root
        self.controller = controller
        self.path_controller = path_controller
        self.logger = logger

        self.root.geometry('1150x650')
        self.root.title('Youtube Downloader')
        self.root.resizable(0, 0)

        self.root.option_add('*Font', 'Arial 28')  # set default font

        self.format_type = StringVar()
        self.mp_val = StringVar()
        self.length_option = StringVar()

        self.format_options = ['audio mp4', 'audio mp3', 'video']
        self.format_type.set(self.format_options[0])

        self.length_option.set('Full')

        self.start_hour = StringVar(value='00')
        self.start_minute = StringVar(value='00')
        self.start_second = StringVar(value='00')
        self.end_hour = StringVar(value='00')
        self.end_minute = StringVar(value='00')
        self.end_second = StringVar(value='00')

        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill='x')

        for i in range(4):
            self.main_frame.grid_columnconfigure(i, weight=1)

        self.info_label = Label(self.main_frame, text='Youtube url:')
        self.info_label.grid(row=0, column=0)

        self.url_entry = Entry(self.main_frame)
        self.url_entry.grid(row=0, column=1, columnspan=3, sticky='NSWE')
        self.url_entry.bind("<KeyRelease>", self.check_entry)

        self.clear_url_button = Button(self.main_frame, text='clear', command=self.clear_url_entry)
        self.clear_url_button.grid(row=0, column=5)

        self.settings_frame = Frame(self.root)
        self.settings_frame.pack()

        self.format_frame = Frame(self.settings_frame)
        self.format_frame.pack(side=LEFT)

        self.type_label = Label(self.format_frame, text='Choose Format:')
        self.type_label.grid(row=0)

        self.type_box = Combobox(self.format_frame, textvariable=self.format_type, values=self.format_options,
                                 state='readonly')
        self.type_box.grid(row=1)

        self.length_frame = Frame(self.settings_frame)
        self.length_frame.pack(side=LEFT)

        self.length_label = Label(self.length_frame, text='Length:')
        self.length_label.grid(row=0)

        self.full_checkbox = Radiobutton(self.length_frame, text='Full', variable=self.length_option,
                                         value='Full', command=self.length_check)
        self.full_checkbox.grid(row=1)

        self.part_checkbox = Radiobutton(self.length_frame, text='Part', variable=self.length_option,
                                         value='Part', command=self.length_check)
        self.part_checkbox.grid(row=2)

        self.start_label = Label(self.length_frame, text="Start Time:")
        self.start_label.grid(row=3, columnspan=3, sticky='E')

        self.start_hour_entry, self.start_minute_entry, self.start_second_entry = self.create_time_entries(
            self.length_frame, row=4, textvariable=(self.start_hour, self.start_minute, self.start_second))

        self.end_label = Label(self.length_frame, text="End Time:")
        self.end_label.grid(row=5)

        self.end_hour_entry, self.end_minute_entry, self.end_second_entry = self.create_time_entries(self.length_frame,
                                    row=6, textvariable=(self.end_hour, self.end_minute, self.end_second))

        self.destination_frame = Frame(self.settings_frame)
        self.destination_frame.pack()

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack()

        self.download_button = Button(self.bottom_frame, text='Download', state=DISABLED,
                                      command=self.download)
        self.download_button.grid(row=0, column=1)

        self.color_exception = [self.start_hour_entry, self.start_minute_entry, self.start_second_entry,
                                self.end_hour_entry, self.end_minute_entry, self.end_second_entry, self.url_entry]

        self.set_widget_style(self.root, bg_color)

    def set_widget_style(self, widget, bg_color):
        widget.configure(background=bg_color)

        if isinstance(widget, Frame):
            for child in widget.winfo_children():
                if child not in self.color_exception:
                    self.set_widget_style(child, bg_color)
        else:
            for child in widget.winfo_children():
                if isinstance(child, Frame):
                    self.set_widget_style(child, bg_color)

    def create_time_entries(self, frame, row, textvariable):
        hour_label = Label(frame, text='HH:')
        hour_label.grid(row=row, column=0)

        hour_entry = Entry(frame, width=2, validate="key", state=DISABLED, bg='black', textvariable=textvariable[0],
                           validatecommand=(self.root.register(self.validate_time_entry), "%P"))
        hour_entry.grid(row=row, column=1)
        hour_entry.insert(END, "00")
        hour_entry.bind("<FocusIn>", self.clear_entry)
        hour_entry.bind("<FocusOut>", self.fill_entry)

        minute_label = Label(frame, text='MM:')
        minute_label.grid(row=row, column=2)

        minute_entry = Entry(frame, width=2, validate="key", textvariable=textvariable[1],
                             validatecommand=(self.root.register(self.validate_time_entry), "%P"), state=DISABLED,)
        minute_entry.grid(row=row, column=3)
        minute_entry.insert(END, "00")
        minute_entry.bind("<FocusIn>", self.clear_entry)
        minute_entry.bind("<FocusOut>", self.fill_entry)

        second_label = Label(frame, text='SS:')
        second_label.grid(row=row, column=4)

        second_entry = Entry(frame, width=2, validate="key", textvariable=textvariable[2],
                             validatecommand=(self.root.register(self.validate_time_entry), "%P"), state=DISABLED)
        second_entry.grid(row=row, column=5)
        second_entry.insert(END, "00")
        second_entry.bind("<FocusIn>", self.clear_entry)
        second_entry.bind("<FocusOut>", self.fill_entry)

        return hour_entry, minute_entry, second_entry

    def check_entry(self, event=None):
        if self.url_entry.get():
            self.download_button.config(state=NORMAL)
        else:
            self.download_button.config(state=DISABLED)

    @staticmethod
    def clear_entry(event):
        entry = event.widget
        if entry.get() == '00':
            entry.delete(0, END)

    @staticmethod
    def fill_entry(event):
        entry = event.widget
        if not entry.get():
            entry.insert(END, '00')

    @staticmethod
    def validate_time_entry(value):
        if value == '':
            return True
        if value.isdigit():
            time = int(value)
            return 0 <= time < 60
        return False

    def download(self):
        self.download_button.configure(text='Downloading...')
        self.download_button.update_idletasks()  # refresh app allows change text

        url = self.url_entry.get()
        self.logger.debug('Start downloading: %s', url)  # dodaje zapis do logu

        format_type = self.format_type.get()
        if self.length_option.get() == 'Part':
            hour, minute, second = self.get_start_values()
            start_time = (hour, minute, second)
            hour, minute, second = self.get_end_values()
            end_time = (hour, minute, second)
        else:
            start_time, end_time = ('00', '00', '00'), ('00', '00', '00')

        self.path_controller.folder_path_set()
        self.controller.download(url, format_type, start_time, end_time)

        self.download_button.configure(text='Download')

    def get_start_values(self):
        hour = self.start_hour_entry.get() or '00'
        minute = self.start_minute_entry.get() or '00'
        second = self.start_second_entry.get() or '00'
        return hour, minute, second

    def get_end_values(self):
        hour = self.end_hour_entry.get() or '00'
        minute = self.end_minute_entry.get() or '00'
        second = self.end_second_entry.get() or '00'
        return hour, minute, second

    def length_check(self):
        if self.length_option.get() == 'Full':
            for i in self.color_exception:
                if i != self.url_entry:
                    i.configure(state=DISABLED, bg='black')
        else:
            for i in self.color_exception:
                if i != self.url_entry:
                    i.configure(state=NORMAL, bg='white')

    def clear_url_entry(self):
        self.url_entry.delete(0, END)
        self.download_button.config(state=DISABLED)


class SettingsMenu:
    def __init__(self, root, path_controller, logger):
        self.root = root
        self.path_controller = path_controller
        self.logger = logger
        self.root.option_add('*Font', 'Arial 12')

        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.settings_menu = Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(menu=self.settings_menu, label='Menu')

        self.path_menu = Menu(self.settings_menu, tearoff=False)
        self.path_menu.add_command(label='audio', command=self.select_audio_path)
        self.path_menu.add_command(label='video', command=self.select_video_path)

        self.settings_menu.add_cascade(label='path', menu=self.path_menu)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label='Exit', command=root.destroy)

    def select_audio_path(self):
        self.logger.debug('Audio path clicked')
        self.path_controller.select_save_path('audio')

    def select_video_path(self):
        self.logger.debug('Video path clicked')
        self.path_controller.select_save_path('video')
