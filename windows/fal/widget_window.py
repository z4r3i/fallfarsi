"""
Floating widget window — displays current fortune.
"""
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
)
from PySide6.QtNetwork import QNetworkAccessManager
from PySide6.QtGui import QFont

CARD_WIDTH = 300
CARD_HEIGHT = 400


class FalWidget(QWidget):
    def __init__(self, dark=False):
        super().__init__()
        self.dark = dark
        self.current_fal = None

        self.setWindowTitle("Fal4mir")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(CARD_WIDTH, CARD_HEIGHT)

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(8)

        # Header - شماره
        header = QLabel()
        header.setFont(QFont("Segoe UI", 11, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        self.header_label = header
        root.addWidget(header)

        # عکس
        self.image_label = QLabel()
        self.image_label.setMinimumHeight(120)
        self.image_label.setAlignment(Qt.AlignCenter)
        root.addWidget(self.image_label)

        # Ghazal - شاعری
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.ghazal_label = QLabel()
        self.ghazal_label.setWordWrap(True)
        self.ghazal_label.setFont(QFont("B Titr", 9))
        self.ghazal_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        scroll.setWidget(self.ghazal_label)
        root.addWidget(scroll, 1)

        # Buttons
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("⟳")
        self.refresh_btn.setMaximumWidth(40)
        self.voice_btn = QPushButton("🔊")
        self.voice_btn.setMaximumWidth(40)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.voice_btn)
        root.addLayout(btn_layout)

        self.apply_theme()

    def apply_theme(self):
        if self.dark:
            self.setStyleSheet("""
                QWidget { background-color: #1e1e1e; }
                QLabel { color: #e0e0e0; }
                QPushButton { background-color: #333; border: 1px solid #555; color: #e0e0e0; border-radius: 4px; }
                QPushButton:hover { background-color: #444; }
                QScrollArea { border: none; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #f5f5f5; }
                QLabel { color: #333; }
                QPushButton { background-color: #e0e0e0; border: 1px solid #ccc; color: #333; border-radius: 4px; }
                QPushButton:hover { background-color: #d0d0d0; }
                QScrollArea { border: none; }
            """)

    def set_fal(self, fal_data):
        self.current_fal = fal_data
        self.header_label.setText(fal_data.number)
        self.ghazal_label.setText(fal_data.ghazal)

        if fal_data.image_url:
            try:
                img_data = __import__('requests').get(fal_data.image_url, timeout=5).content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                scaled = pixmap.scaledToWidth(280, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled)
            except Exception:
                self.image_label.setText("—")

    def set_dark(self, dark: bool):
        self.dark = dark
        self.apply_theme()
