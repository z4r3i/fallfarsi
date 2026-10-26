"""
Main application logic.
"""
import sys
import logging
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import QTimer, Qt

from . import api
from .settings import settings as S
from .widget_window import FalWidget
from .main_window import MainWindow

logging.basicConfig(level=logging.INFO)


class FalApp:
    def __init__(self):
        self.qapp = QApplication(sys.argv)
        self.qapp.setQuitOnLastWindowClosed(False)

        self.config = S.load()

        self.widget = FalWidget(dark=self.config.get("dark_mode", False))
        self.main_win = MainWindow()

        self._wire_signals()
        self._place_widget()
        self.widget.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self._refresh)
        self.timer.start(self.config.get("refresh_seconds", 3600) * 1000)

        self._setup_tray()
        self._refresh()

    def _wire_signals(self):
        self.widget.refresh_btn.clicked.connect(self._refresh)
        self.widget.voice_btn.clicked.connect(self._play_voice)
        self.main_win.refresh_btn.clicked.connect(self._refresh)
        self.main_win.voice_btn.clicked.connect(self._play_voice)
        self.main_win.favorite_btn.clicked.connect(self._add_favorite)

    def _place_widget(self):
        pos = self.config.get("window_pos")
        if pos:
            self.widget.move(pos[0], pos[1])

    def _refresh(self):
        fal = api.fetch()
        if fal:
            self.widget.set_fal(fal)
            self.main_win.set_fal(fal)
            self.config["last_fal"] = {
                "number": fal.number,
                "ghazal": fal.ghazal,
                "tabir": fal.tabir,
                "image_url": fal.image_url,
            }
            S.save(self.config)

    def _play_voice(self):
        if hasattr(self, "current_fal") and self.current_fal.voice_url:
            import webbrowser
            webbrowser.open(self.current_fal.voice_url)

    def _add_favorite(self):
        if self.widget.current_fal:
            self.main_win.add_favorite(self.widget.current_fal.number)

    def _setup_tray(self):
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self._make_icon())
        menu = QMenu()
        menu.addAction("باز کردن", self._show_main)
        menu.addAction("فال جدید", self._refresh)
        menu.addSeparator()
        menu.addAction("خروج", self.quit)
        self.tray.setContextMenu(menu)
        self.tray.show()

    def _show_main(self):
        self.main_win.show()
        self.main_win.raise_()
        self.main_win.activateWindow()

    def _make_icon(self):
        pix = QPixmap(64, 64)
        pix.fill(QColor(0, 0, 0, 0))
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor("#FF6B35"))
        p.setPen(QColor(0, 0, 0, 0))
        p.drawEllipse(2, 2, 60, 60)
        p.setPen(QColor("#FFFFFF"))
        f = QFont()
        f.setBold(True)
        f.setPointSize(24)
        p.setFont(f)
        p.drawText(pix.rect(), Qt.AlignCenter, "☆")
        p.end()
        return QIcon(pix)

    def quit(self):
        pos = self.widget.pos()
        self.config["window_pos"] = [pos.x(), pos.y()]
        S.save(self.config)
        self.qapp.quit()

    def run(self):
        return self.qapp.exec()


def main():
    app = FalApp()
    sys.exit(app.run())
