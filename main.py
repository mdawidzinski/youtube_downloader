from tkinter import *
from controler import YoutubeDownloaderController
from model import YoutubeDownloaderModel
from gui import DownloaderGui

# TODO clean url po pobraniu
# TODO multitone

if __name__ == '__main__':
    root = Tk()
    model = YoutubeDownloaderModel()  # singleton
    controller = YoutubeDownloaderController(model)
    view = DownloaderGui(root, controller)

    root.mainloop()

