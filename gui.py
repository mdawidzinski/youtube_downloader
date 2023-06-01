from tkinter import *
from tkinter.ttk import Combobox

# TODO cudzysłowy
# TODO bordery
# TODO ostatnie 10 wpisanych url, przykład w test.py, po kliknięciu DOWNLOAD dodanie do listy,
#  if > 10 ostatnie kasowane
# TODO in progres...
# TODO if count(-) > 1 przy bardziej złożonych nazwach plików do obserwacji
# TODO schemat grafiki, json. kontroler czy osobne cudo?
# TODO invalid link WARNING
# TODO controler grafiki, clasa
font = ('Arial', '28')


class DownloaderGui:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.geometry('1150x650')

        self.root.title('Youtube Downloader')

        self.selected_option = StringVar()
        self.mp_val = StringVar()
        self.length_option = StringVar()

        self.options = ['audio mp4', 'audio mp3', 'video']
        self.selected_option.set(self.options[0])

        self.length_option.set('Full')

        self.main_frame = Frame(self.root)  # TODO dołożyć historie
        self.main_frame.pack()

        self.info_label = Label(self.main_frame, text='Youtube url:', font=font)
        self.info_label.grid(row=0, column=0)

        self.url_entry = Entry(self.main_frame, font=font)
        self.url_entry.grid(row=0, column=1, columnspan=3, sticky='NSWE')
        self.url_entry.bind("<KeyRelease>", self.check_entry)

        self.settings_frame = Frame(self.root)
        self.settings_frame.pack()

        self.format_frame = Frame(self.settings_frame)
        self.format_frame.pack(side=LEFT)

        self.type_label = Label(self.format_frame, text='Choose Format:', font=font)
        self.type_label.grid(row=0)
        # TODO blokada zmiany tekstu:
        self.type_box = Combobox(self.format_frame, font=font, textvariable=self.selected_option, values=self.options)
        self.type_box.grid(row=1)

        self.length_frame = Frame(self.settings_frame, bg='#9DF1DF')
        self.length_frame.pack(side=LEFT)

        self.length_label = Label(self.length_frame, text='Length:', font=font, bg='#9DF1DF')
        self.length_label.grid(row=0)
        # TODO checkboxy do zablokowania i warunki
        self.full_checkbox = Radiobutton(self.length_frame, text='Full', font=font, variable=self.length_option,
                                         value='Full', bg='#9DF1DF')
        self.full_checkbox.grid(row=1)

        self.part_checkbox = Radiobutton(self.length_frame, text='Part', font=font, variable=self.length_option,
                                         value='Part', bg='#9DF1DF')
        self.part_checkbox.grid(row=2)

        self.start_label = Label(self.length_frame, text="Start Time:", font=font)
        self.start_label.grid(row=3, columnspan=3, sticky='E')

        self.start_hour_entry, self.start_minute_entry, self.start_second_entry = self.create_time_entries(
            self.length_frame, row=4)

        self.end_label = Label(self.length_frame, text="End Time:", font=font)
        self.end_label.grid(row=5)

        self.end_hour_entry, self.end_minute_entry, self.end_second_entry = self.create_time_entries(self.length_frame,
                                                                                                     row=6)

        self.destination_frame = Frame(self.settings_frame)
        self.destination_frame.pack()

        self.bottom_frame = Frame(self.root)
        self.bottom_frame.pack()
        # TODO do modyfikacji:
        self.download_button = Button(self.bottom_frame, text='Download', font=font, state=DISABLED,
                                      command=self.download)
        self.download_button.grid(row=0, column=1)

    def create_time_entries(self, frame, row):
        hour_label = Label(frame, text='HH:', font=font)
        hour_label.grid(row=row, column=0)

        hour_entry = Entry(frame, width=2, validate="key",
                           validatecommand=(self.root.register(self.validate_time_entry), "%P"), font=font)
        hour_entry.grid(row=row, column=1)
        hour_entry.insert(END, "00")
        hour_entry.bind("<FocusIn>", self.clear_entry)
        hour_entry.bind("<FocusOut>", self.fill_entry)

        minute_label = Label(frame, text='MM:', font=font)
        minute_label.grid(row=row, column=2)

        minute_entry = Entry(frame, width=2, validate="key",
                             validatecommand=(self.root.register(self.validate_time_entry), "%P"), font=font)
        minute_entry.grid(row=row, column=3)
        minute_entry.insert(END, "00")
        minute_entry.bind("<FocusIn>", self.clear_entry)
        minute_entry.bind("<FocusOut>", self.fill_entry)

        second_label = Label(frame, text='SS:', font=font)
        second_label.grid(row=row, column=4)

        second_entry = Entry(frame, width=2, validate="key",
                             validatecommand=(self.root.register(self.validate_time_entry), "%P"), font=font)
        second_entry.grid(row=row, column=5)
        second_entry.insert(END, "00")
        second_entry.bind("<FocusIn>", self.clear_entry)
        second_entry.bind("<FocusOut>", self.fill_entry)

        return hour_entry, minute_entry, second_entry

    def check_entry(self, event=None):
        if self.url_entry.get():
            self.download_button.config(state=NORMAL)  # Jeśli pole Entry nie jest puste, ustawiamy stan na NORMAL
        else:
            self.download_button.config(state=DISABLED)

    def clear_entry(self, event):
        entry = event.widget
        entry.delete(0, END)

    def fill_entry(self, event):
        entry = event.widget
        if not entry.get():
            entry.insert(END, "00")

    def validate_time_entry(self, value):
        if value == '':
            return True
        if value.isdigit():
            time = int(value)
            return 0 <= time < 60
        else:
            return False

    def download(self):
        url = self.url_entry.get()

        format_type = self.selected_option.get()

        hour, minute, second = self.get_start_values()
        start_time = (hour, minute, second)
        hour, minute, second = self.get_end_values()
        end_time = (hour, minute, second)

        self.controller.download(url, format_type, start_time, end_time)
        # TODO tu dołożyć dodanie do listy

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
