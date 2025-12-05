from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLabel
from PyQt5.QtCore import Qt, QTimer

class Controls(QWidget):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.initUI()
        
        # Timer para actualizar la barra de progreso
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Actualizar cada 100ms
    
    def initUI(self):
        # Layout principal vertical
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 8, 10, 8)
        main_layout.setSpacing(5)
        self.setLayout(main_layout)
        
        # Barra de progreso del video
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(10)
        
        self.time_label = QLabel('00:00')
        self.time_label.setFixedWidth(45)
        progress_layout.addWidget(self.time_label)
        
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.setMaximum(1000)
        self.progress_slider.setValue(0)
        self.progress_slider.sliderPressed.connect(self.on_progress_pressed)
        self.progress_slider.sliderReleased.connect(self.on_progress_released)
        progress_layout.addWidget(self.progress_slider, stretch=1)
        
        self.duration_label = QLabel('00:00')
        self.duration_label.setFixedWidth(45)
        progress_layout.addWidget(self.duration_label)
        
        main_layout.addLayout(progress_layout)
        
        # Controles (botones y volumen)
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        # Estilo
        self.setStyleSheet("""
            QWidget {
                background-color: orange;
            }
            QPushButton {
                background-color: #FF8C00;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 3px;
                font-size: 12px;
                min-width: 70px;
                max-height: 35px;
            }
            QPushButton:hover {
                background-color: #FFA500;
            }
            QLabel {
                color: white;
                font-size: 11px;
                padding: 0px 5px;
            }
            QSlider {
                max-height: 30px;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: white;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
                border: 2px solid #FF8C00;
            }
        """)
        
        # Botón Play
        self.play_button = QPushButton('Play')
        self.play_button.clicked.connect(self.toggle_play)
        controls_layout.addWidget(self.play_button)
        
        # Botón Stop
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.player.stop)
        controls_layout.addWidget(self.stop_button)
        
        # Control de volumen
        self.volume_label = QLabel('Vol:')
        controls_layout.addWidget(self.volume_label)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.setMinimumWidth(100)
        self.volume_slider.valueChanged.connect(self.change_volume)
        controls_layout.addWidget(self.volume_slider, stretch=1)
        
        # Botón para abrir archivo
        self.open_button = QPushButton('Open Video')
        self.open_button.clicked.connect(self.open_file)
        controls_layout.addWidget(self.open_button)
        
        main_layout.addLayout(controls_layout)
    
    def toggle_play(self):
        if self.player.is_playing:
            self.player.pause()
            self.play_button.setText('Play')
        else:
            self.player.play()
            self.play_button.setText('Pause')
    
    def change_volume(self, value):
        self.player.set_volume(value)
    
    def open_file(self):
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Open Video File", 
            "", 
            "Video Files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv)"
        )
        if file_path:
            self.player.load_video(file_path)
            # Actualizar duración
            duration = self.player.get_duration()
            self.duration_label.setText(self.format_time(duration))
    
    def update_progress(self):
        if self.player.cap and self.player.is_playing:
            current = self.player.get_current_position()
            duration = self.player.get_duration()
            
            if duration > 0:
                progress = int((current / duration) * 1000)
                self.progress_slider.setValue(progress)
                self.time_label.setText(self.format_time(current))
    
    def on_progress_pressed(self):
        self.timer.stop()
    
    def on_progress_released(self):
        duration = self.player.get_duration()
        new_position = (self.progress_slider.value() / 1000.0) * duration
        self.player.seek(new_position)
        self.timer.start(100)
    
    def format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f'{mins:02d}:{secs:02d}'