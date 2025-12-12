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
        
        self.setStyleSheet("background-color: black;")
        
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: black;")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        central_widget.setLayout(layout)
        
        # Video widget
        self.video_widget = QLabel()
        self.video_widget.setStyleSheet("background-color: black;")
        self.video_widget.setAlignment(Qt.AlignCenter)
        self.video_widget.setScaledContents(False)
        layout.addWidget(self.video_widget, stretch=1)
        
        # Subtítulos
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
        
        self.player.set_video_output(self.video_widget)
        
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(100)
    
    def connect_signals(self):
        self.controls.play_pause_clicked.connect(self.toggle_play_pause)
        self.controls.stop_clicked.connect(self.stop)
        self.controls.volume_changed.connect(self.player.set_volume)
        self.controls.position_changed.connect(self.seek_position)
        self.controls.open_file_clicked.connect(self.open_video_file)
        self.controls.subtitles_toggled.connect(self.toggle_subtitles)
        self.controls.translation_toggled.connect(self.toggle_translation)
    
    def toggle_play_pause(self):
        if not self.player.cap and not self.player.is_audio_only:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Seleccionar Archivo", "",
                "Multimedia (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav *.ogg *.flac);;Videos (*.mp4 *.avi *.mkv *.mov);;Audio (*.mp3 *.wav *.ogg *.flac);;Todos (*.*)"
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
        self.player.stop()
        self.controls.set_play_pause_text("Play")
        self.controls.update_progress(0)
    
    def seek_position(self, position_ms):
        position_seconds = position_ms / 1000.0
        self.player.seek(position_seconds)
    
    def toggle_subtitles(self):
        enabled = self.player.toggle_subtitles()
        if not enabled:
            self.subtitle_label.setText("")
    
    def toggle_translation(self):
        """Activa/desactiva traducción"""
        enabled, target_lang = self.player.toggle_translation()
        
        if enabled:
            lang_name = "Español" if target_lang == 'es' else "English"
            self.controls.translation_btn.setText(f"→ {lang_name}")
        else:
            self.controls.translation_btn.setText("Traducir")
    
    def update_ui(self):
        if (self.player.cap or self.player.is_audio_only) and self.player.is_playing:
            current = int(self.player.get_current_position() * 1000)
            duration = int(self.player.get_duration() * 1000)
            
            self.controls.update_progress(current)
            self.controls.update_time_label(current, duration)
            
            subtitle_text = self.player.get_current_subtitle()
            self.subtitle_label.setText(subtitle_text)
    
    def open_video_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Archivo", "",
            "Multimedia (*.mp4 *.avi *.mkv *.mov *.mp3 *.wav *.ogg *.flac);;Videos (*.mp4 *.avi *.mkv *.mov);;Audio (*.mp3 *.wav *.ogg *.flac);;Todos (*.*)"
        )
        if file_path:
            if self.player.cap or self.player.is_audio_only:
                self.player.stop()
            
            self.player.load_video(file_path)
            duration = self.player.get_duration()
            self.controls.set_duration(int(duration * 1000))
            self.player.play()
            self.controls.set_play_pause_text("Pause")