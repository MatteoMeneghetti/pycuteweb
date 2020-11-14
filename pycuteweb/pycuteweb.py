from PyQt5.QtCore import QUrl, QCoreApplication, Qt, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pathlib import Path
from threading import Event
from .window import Window


class Application(QObject):

    windows = {}

    folder_dialog_spawn = pyqtSignal(str)
    window_dialog_spawn = pyqtSignal(int, str)

    def __init__(self):
        QObject.__init__(self)

        self.__file_dialog_event = Event()
        self.__filename_dialog = None

        self.folder_dialog_spawn.connect(self.__on_folder_dialog)
        self.window_dialog_spawn.connect(self.__on_window)
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        self.__app = QApplication([])

    def spawn_window(self, url=""):
        id = len(Application.windows)
        self.window_dialog_spawn.emit(id, url)
        return id

    def spawn_folder_dialog(self, title="Select directory"):
        self.folder_dialog_spawn.emit(title)
        self.__file_dialog_event.wait()
        path = self.__filename_dialog
        self.__filename_dialog = None
        return Path(path) if path else None

    @pyqtSlot(int, str)
    def __on_window(self, id, url):
        window = Window(url=url)
        Application.windows[id] = window

    @pyqtSlot(str)
    def __on_folder_dialog(self, title):
        self.__filename_dialog = str(QFileDialog.getExistingDirectory(parent=None, caption=title, options=QFileDialog.ShowDirsOnly))
        self.__file_dialog_event.set()

    def start(self):
        from sys import exit

        for window in Application.windows.values():
            window.start()
        return exit(self.__app.exec_())
