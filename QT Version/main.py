import sys
from PyQt5.QtWidgets import QApplication
from qt_gui import YoutubeDownloaderGui
from qt_controllers import YoutubeDownloaderController, PathController
from qt_model import YoutubeDownloaderModel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = YoutubeDownloaderModel()
    controller = YoutubeDownloaderController(model)
    path_controller = PathController(model)
    window = YoutubeDownloaderGui(controller, path_controller)
    window.show()
    sys.exit(app.exec_())
