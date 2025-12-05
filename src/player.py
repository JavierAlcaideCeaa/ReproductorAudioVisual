import cv2
import numpy as np
import pygame
import subprocess
import os
import tempfile
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QPixmap)
    
    def __init__(self, cap, fps):
        super().__init__()
        self.cap = cap
        self.fps = fps
        self.is_running = True
    
    def run(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Convertir BGR a RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            
            # Crear QImage y emitir señal
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.change_pixmap_signal.emit(pixmap)
            
            # Control de FPS
            self.msleep(int(1000 / self.fps))
    
    def stop(self):
        self.is_running = False
        self.wait()

class VideoPlayer:
    def __init__(self):
        self.cap = None
        self.is_playing = False
        self.volume = 50
        self.video_thread = None
        self.audio_file = None
        
        # Inicializar pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        
    def set_video_output(self, widget):
        self.video_widget = widget
    
    def _extract_audio(self, video_path):
        """Extrae audio del video usando ffmpeg"""
        try:
            # Crear archivo temporal para el audio
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_audio.close()
            
            # Extraer audio con ffmpeg (debe estar instalado en el sistema)
            subprocess.run([
                'ffmpeg', '-i', video_path,
                '-vn', '-acodec', 'pcm_s16le', 
                '-ar', '44100', '-ac', '2',
                '-y', temp_audio.name
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            return temp_audio.name
        except:
            return None
    
    def load_video(self, path):
        if self.cap:
            self.stop()
            self.cap.release()
        
        # Limpiar audio anterior
        if self.audio_file and os.path.exists(self.audio_file):
            try:
                os.unlink(self.audio_file)
            except:
                pass
        
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        
        # Extraer y cargar audio
        self.audio_file = self._extract_audio(path)
        if self.audio_file:
            try:
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.set_volume(self.volume / 100.0)
            except:
                pass
    
    def play(self):
        if not self.cap:
            return
        self.is_playing = True
        
        # Iniciar video thread
        if self.video_thread is None or not self.video_thread.isRunning():
            self.video_thread = VideoThread(self.cap, self.fps)
            self.video_thread.change_pixmap_signal.connect(self.update_frame)
            self.video_thread.start()
        
        # Reproducir audio
        if self.audio_file:
            try:
                current_pos = self.get_current_position()
                if current_pos > 0:
                    pygame.mixer.music.play(start=current_pos)
                else:
                    pygame.mixer.music.play()
            except:
                try:
                    pygame.mixer.music.play()
                except:
                    pass
    
    def update_frame(self, pixmap):
        if hasattr(self, 'video_widget'):
            self.video_widget.setPixmap(pixmap.scaled(
                self.video_widget.size(),
                aspectRatioMode=1
            ))
    
    def pause(self):
        self.is_playing = False
        if self.video_thread:
            self.video_thread.stop()
        pygame.mixer.music.pause()
    
    def stop(self):
        self.is_playing = False
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread = None
        pygame.mixer.music.stop()
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def set_volume(self, volume):
        if volume < 0 or volume > 100:
            raise ValueError("Volume must be between 0 and 100")
        self.volume = volume
        pygame.mixer.music.set_volume(volume / 100.0)
    
    def get_duration(self):
        if not self.cap:
            return 0
        frame_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        return frame_count / self.fps if self.fps > 0 else 0
    
    def get_current_position(self):
        if not self.cap:
            return 0
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        return current_frame / self.fps if self.fps > 0 else 0
    
    def seek(self, seconds):
        if not self.cap:
            return
        was_playing = self.is_playing
        
        if self.video_thread:
            self.video_thread.stop()
        
        pygame.mixer.music.stop()
        
        frame_number = int(seconds * self.fps)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        if was_playing:
            self.play()
    
    def __del__(self):
        if self.video_thread:
            self.video_thread.stop()
        if self.cap:
            self.cap.release()
        if self.audio_file and os.path.exists(self.audio_file):
            try:
                os.unlink(self.audio_file)
            except:
                pass
        pygame.mixer.quit()