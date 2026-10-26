"""
Main application window — shows ghazal details, interpretation, and favorites.
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QListWidget, QListWidgetItem
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fal4mir - تفسیر فال")
        self.resize(700, 600)
        self.setMinimumSize(500, 400)

        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # Header
        header = QLabel("فال امروز")
        header.setFont(QFont("B Titr", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        root.addWidget(header)

        # Main content - 2 columns
        content = QHBoxLayout()
        content.setSpacing(16)

        # Left - عکس + شاعری
        left = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setMinimumHeight(200)
        self.image_label.setAlignment(Qt.AlignCenter)
        left.addWidget(self.image_label)

        self.number_label = QLabel()
        self.number_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.number_label.setAlignment(Qt.AlignCenter)
        left.addWidget(self.number_label)

        scroll_ghazal = QScrollArea()
        scroll_ghazal.setWidgetResizable(True)
        self.ghazal_label = QLabel()
        self.ghazal_label.setWordWrap(True)
        self.ghazal_label.setFont(QFont("B Titr", 9))
        self.ghazal_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        scroll_ghazal.setWidget(self.ghazal_label)
        left.addWidget(scroll_ghazal, 1)

        # Right - تفسیر + دکمه‌ها
        right = QVBoxLayout()

        tabir_title = QLabel("تفسیر:")
        tabir_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        right.addWidget(tabir_title)

        scroll_tabir = QScrollArea()
        scroll_tabir.setWidgetResizable(True)
        self.tabir_label = QLabel()
        self.tabir_label.setWordWrap(True)
        self.tabir_label.setFont(QFont("B Titr", 9))
        self.tabir_label.setAlignment(Qt.AlignTop | Qt.AlignRight)
        scroll_tabir.setWidget(self.tabir_label)
        right.addWidget(scroll_tabir, 1)

        # Buttons
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("⟳ فال جدید")
        self.voice_btn = QPushButton("🔊 صوت")
        self.favorite_btn = QPushButton("★ علاقه‌مندی")
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.voice_btn)
        btn_layout.addWidget(self.favorite_btn)
        right.addLayout(btn_layout)

        content.addLayout(left, 1)
        content.addLayout(right, 1)
        root.addLayout(content, 1)

        # Favorites list
        fav_title = QLabel("علاقه‌مندی‌ها:")
        fav_title.setFont(QFont("Segoe UI", 10, QFont.Bold))
        root.addWidget(fav_title)

        self.favorites_list = QListWidget()
        self.favorites_list.setMaximumHeight(100)
        root.addWidget(self.favorites_list)

        self.setCentralWidget(central)

    def set_fal(self, fal_data):
        self.number_label.setText(fal_data.number)
        self.ghazal_label.setText(fal_data.ghazal)
        self.tabir_label.setText(fal_data.tabir)

        if fal_data.image_url:
            try:
                import requests
                img_data = requests.get(fal_data.image_url, timeout=5).content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                scaled = pixmap.scaledToHeight(200, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled)
            except Exception:
                self.image_label.setText("—")

    def add_favorite(self, number: str):
        item = QListWidgetItem(number)
        self.favorites_list.insertItem(0, item)
