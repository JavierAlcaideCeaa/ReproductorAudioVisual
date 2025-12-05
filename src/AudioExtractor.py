import cv2
import numpy as np
import pygame
import subprocess
import os
import tempfile
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

class AudioExtractor:
    """Clase para extraer y manejar audio de videos"""
    
    @staticmethod
    def extract(video_path):
        """Extrae audio del video y retorna la ruta del archivo temporal"""
        try:
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_audio.close()
            
            subprocess.run([
                'ffmpeg', '-i', video_path,
                '-vn', '-acodec', 'pcm_s16le', 
                '-ar', '44100', '-ac', '2',
                '-y', temp_audio.name
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            return temp_audio.name
        except:
            return None
    
    @staticmethod
    def cleanup(audio_path):
        """Elimina archivo de audio temporal"""
        if audio_path and os.path.exists(audio_path):
            try:
                os.unlink(audio_path)
            except:
                pass

class AudioPlayer:
    """Clase para reproducir audio con pygame"""
    
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        self.audio_file = None
        self.volume = 50
    
    def load(self, audio_path):
        """Carga un archivo de audio"""
        self.audio_file = audio_path
        if self.audio_file:
            try:
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.set_volume(self.volume / 100.0)
                return True
            except:
                return False
        return False
    
    def play(self, start_pos=0):
        """Reproduce audio desde una posición específica"""
        if not self.audio_file:
            return
        try:
            if start_pos > 0:
                pygame.mixer.music.play(start=start_pos)
            else:
                pygame.mixer.music.play()
        except:
            try:
                pygame.mixer.music.play()
            except:
                pass
    
    def pause(self):
        pygame.mixer.music.pause()
    
    def stop(self):
        pygame.mixer.music.stop()
    
    def set_volume(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(volume / 100.0)
    
    def cleanup(self):
        AudioExtractor.cleanup(self.audio_file)
        pygame.mixer.quit()

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
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.change_pixmap_signal.emit(pixmap)
            
            self.msleep(int(1000 / self.fps))
    
    def stop(self):
        self.is_running = False
        self.wait()

class VideoPlayer:
    """Clase principal que coordina video y audio"""
    
    def __init__(self):
        self.cap = None
        self.is_playing = False
        self.volume = 50
        self.video_thread = None
        self.audio_player = AudioPlayer()
        
    def set_video_output(self, widget):
        self.video_widget = widget
    
    def load_video(self, path):
        # Limpiar video anterior
        if self.cap:
            self.stop()
            self.cap.release()
        
        # Limpiar audio anterior
        self.audio_player.cleanup()
        
        # Cargar video
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        
        # Extraer y cargar audio
        audio_file = AudioExtractor.extract(path)
        self.audio_player.load(audio_file)
    
    def play(self):
        if not self.cap:
            return
        self.is_playing = True
        
        # Iniciar video
        if self.video_thread is None or not self.video_thread.isRunning():
            self.video_thread = VideoThread(self.cap, self.fps)
            self.video_thread.change_pixmap_signal.connect(self.update_frame)
            self.video_thread.start()
        
        # Iniciar audio
        self.audio_player.play(self.get_current_position())
    
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
        self.audio_player.pause()
    
    def stop(self):
        self.is_playing = False
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread = None
        self.audio_player.stop()
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def set_volume(self, volume):
        if volume < 0 or volume > 100:
            raise ValueError("Volume must be between 0 and 100")
        self.volume = volume
        self.audio_player.set_volume(volume)
    
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
        self.audio_player.stop()
        
        frame_number = int(seconds * self.fps)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        if was_playing:
            self.play()
    
    def __del__(self):
        if self.video_thread:
            self.video_thread.stop()
        if self.cap:
            self.cap.release()
        self.audio_player.cleanup()