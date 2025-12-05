from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from components.controls import Controls

class UserInterface(QMainWindow):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Video Player')
        self.setGeometry(100, 100, 800, 600)
        
        # Fondo negro para toda la ventana
        self.setStyleSheet("background-color: black;")
        
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: black;")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        central_widget.setLayout(layout)
        
        # Video widget (QLabel para mostrar frames)
        self.video_widget = QLabel()
        self.video_widget.setStyleSheet("background-color: black;")
        self.video_widget.setAlignment(Qt.AlignCenter)
        self.video_widget.setScaledContents(False)
        layout.addWidget(self.video_widget, stretch=1)
        
        # Controles
        self.controls = Controls(self.player)
        layout.addWidget(self.controls, stretch=0)
        
        # Conectar reproductor con video widget
        self.player.set_video_output(self.video_widget)