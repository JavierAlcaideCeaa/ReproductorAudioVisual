from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from components.controls import Controls

class UserInterface(QMainWindow):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.timer = QTimer()
        self.initUI()
        self.connect_signals()
    
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
        
        # Subtítulos (nuevo)
        self.subtitle_label = QLabel("")
        self.subtitle_label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 180);
            font-size: 18px;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
        """)
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setMaximumHeight(80)
        layout.addWidget(self.subtitle_label, stretch=0)
        
        # Controles
        self.controls = Controls(self.player)
        layout.addWidget(self.controls, stretch=0)
        
        # Conectar reproductor con video widget
        self.player.set_video_output(self.video_widget)
        
        # Timer para actualizar progreso
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(100)
    
    def connect_signals(self):
        """Conecta las señales de los controles con las acciones del reproductor"""
        self.controls.play_pause_clicked.connect(self.toggle_play_pause)
        self.controls.stop_clicked.connect(self.stop)
        self.controls.volume_changed.connect(self.player.set_volume)
        self.controls.position_changed.connect(self.seek_position)
        self.controls.open_file_clicked.connect(self.open_video_file)
        self.controls.subtitles_toggled.connect(self.toggle_subtitles)  # Nueva conexión
    
    def toggle_play_pause(self):
        """Alterna entre play y pausa"""
        if not self.player.cap and not self.player.is_audio_only:
            # Si no hay video cargado, abrir diálogo
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Seleccionar Archivo", "",
                "Multimedia (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav *.ogg *.flac);;Videos (*.mp4 *.avi *.mkv *.mov);;Audio (*.mp3 *.wav *.ogg *.flac);;Todos los archivos (*.*)"
            )
            if file_path:
                self.player.load_video(file_path)
                duration = self.player.get_duration()
                self.controls.set_duration(int(duration * 1000))
                self.player.play()
                self.controls.set_play_pause_text("Pause")
        else:
            if self.player.is_playing:
                self.player.pause()
                self.controls.set_play_pause_text("Play")
            else:
                self.player.play()
                self.controls.set_play_pause_text("Pause")

    def stop(self):
        """Detiene la reproducción"""
        self.player.stop()
        self.controls.set_play_pause_text("Play")
        self.controls.update_progress(0)
    
    def seek_position(self, position_ms):
        """Busca una posición específica en el video"""
        position_seconds = position_ms / 1000.0
        self.player.seek(position_seconds)
    
    def toggle_subtitles(self):
        """Activa o desactiva los subtítulos"""
        enabled = self.player.toggle_subtitles()
        if not enabled:
            self.subtitle_label.setText("")
    
    def update_ui(self):
        """Actualiza la interfaz con el progreso actual"""
        if (self.player.cap or self.player.is_audio_only) and self.player.is_playing:
            current = int(self.player.get_current_position() * 1000)
            duration = int(self.player.get_duration() * 1000)
            
            self.controls.update_progress(current)
            self.controls.update_time_label(current, duration)
            
            # Actualizar subtítulos
            subtitle_text = self.player.get_current_subtitle()
            self.subtitle_label.setText(subtitle_text)
    
    def open_video_file(self):
        """Abre un diálogo para seleccionar un archivo multimedia"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Archivo", "",
            "Multimedia (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav *.ogg *.flac);;Videos (*.mp4 *.avi *.mkv *.mov);;Audio (*.mp3 *.wav *.ogg *.flac);;Todos los archivos (*.*)"
        )
        if file_path:
            # Detener reproducción actual
            if self.player.cap or self.player.is_audio_only:
                self.player.stop()
            
            # Cargar y reproducir nuevo archivo
            self.player.load_video(file_path)
            duration = self.player.get_duration()
            self.controls.set_duration(int(duration * 1000))
            self.player.play()
            self.controls.set_play_pause_text("Pause")