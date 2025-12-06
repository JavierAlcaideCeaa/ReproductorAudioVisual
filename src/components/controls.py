from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel, QStyle
from PyQt5.QtCore import Qt, pyqtSignal

class ProgressSlider(QSlider):
    """Custom slider that allows clicking to seek"""
    
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setMouseTracking(True)
    
    def mousePressEvent(self, event):
        """Handle mouse press to seek to clicked position"""
        if event.button() == Qt.MouseButton.LeftButton:
            value = QStyle.sliderValueFromPosition(
                self.minimum(),
                self.maximum(),
                event.pos().x(),
                self.width()
            )
            self.setValue(value)
            self.sliderMoved.emit(value)
        super().mousePressEvent(event)

class Controls(QWidget):
    play_pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    volume_changed = pyqtSignal(int)
    position_changed = pyqtSignal(int)
    open_file_clicked = pyqtSignal()  # Nueva señal

    def __init__(self, player=None):
        super().__init__()
        self.player = player
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Open File button (nuevo)
        self.open_file_btn = QPushButton("Open Video")
        self.open_file_btn.setMinimumSize(100, 40)
        self.open_file_btn.clicked.connect(self.open_file_clicked.emit)
        layout.addWidget(self.open_file_btn)

        # Play/Pause button
        self.play_pause_btn = QPushButton("Play")
        self.play_pause_btn.setMinimumSize(80, 40)
        self.play_pause_btn.clicked.connect(self.play_pause_clicked.emit)
        layout.addWidget(self.play_pause_btn)

        # Stop button
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setMinimumSize(80, 40)
        self.stop_btn.clicked.connect(self.stop_clicked.emit)
        layout.addWidget(self.stop_btn)

        # Progress slider
        self.progress_slider = ProgressSlider(Qt.Orientation.Horizontal)
        self.progress_slider.sliderMoved.connect(self.position_changed.emit)
        layout.addWidget(self.progress_slider)

        # Time label
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(self.time_label)

        # Volume label
        volume_label = QLabel("Volume:")
        volume_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(volume_label)

        # Volume slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.valueChanged.connect(self.volume_changed.emit)
        layout.addWidget(self.volume_slider)

        self.setLayout(layout)

    def apply_styles(self):
        """Aplica estilos CSS a los controles"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
            }
            
            QPushButton {
                background-color: #ff8c00;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
            
            QPushButton:hover {
                background-color: #ffa500;
            }
            
            QPushButton:pressed {
                background-color: #cc7000;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #333333;
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #ff8c00;
                border: 1px solid #ff8c00;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #ffa500;
            }
            
            QSlider::sub-page:horizontal {
                background: #ff8c00;
                border-radius: 4px;
            }
        """)

    def update_progress(self, position):
        self.progress_slider.setValue(position)

    def set_duration(self, duration):
        self.progress_slider.setMaximum(duration)

    def update_time_label(self, current, total):
        current_time = self.format_time(current)
        total_time = self.format_time(total)
        self.time_label.setText(f"{current_time} / {total_time}")

    def format_time(self, ms):
        s = ms // 1000
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"

    def set_play_pause_text(self, text):
        self.play_pause_btn.setText(text)