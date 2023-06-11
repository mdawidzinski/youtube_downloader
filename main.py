import logging
from tkinter import *
from controllers import YoutubeDownloaderController, PathController
from model import YoutubeDownloaderModel
from gui import DownloaderGui, SettingsMenu

logging.basicConfig(level=logging.DEBUG, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)  # TODO coś z tą nazwą trzeba zrobić
handler = logging.FileHandler(filename='general.log', )
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    root = Tk()
    model = YoutubeDownloaderModel(logger)
    controller = YoutubeDownloaderController(model, logger)
    path_controller = PathController(model, logger)
    view = DownloaderGui(root, controller, path_controller, logger)
    view2 = SettingsMenu(root, path_controller, logger)

    root.mainloop()
