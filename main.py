from tkinter import *
from controllers import YoutubeDownloaderController, PathController
from model import YoutubeDownloaderModel
from gui import DownloaderGui, SettingsMenu


if __name__ == '__main__':
    root = Tk()
    model = YoutubeDownloaderModel()
    controller = YoutubeDownloaderController(model)
    path_controller = PathController(model)
    view = DownloaderGui(root, controller, path_controller)
    view2 = SettingsMenu(root, path_controller)

    root.mainloop()
