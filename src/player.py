import cv2
import numpy as np
import pygame
import subprocess
import os
import tempfile
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from SubtitleGenerator import SubtitleGenerator
from deep_translator import GoogleTranslator

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QPixmap)
    
    def __init__(self, cap, fps, start_time):
        super().__init__()
        self.cap = cap
        self.fps = fps
        self.is_running = True
        self.start_time = start_time
    
    def run(self):
        frame_duration = 1.0 / self.fps
        
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
            
            elapsed = time.time() - self.start_time
            expected_frame = int(elapsed * self.fps)
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            
            if current_frame < expected_frame - 2:
                continue
            elif current_frame > expected_frame + 2:
                time.sleep(frame_duration)
            else:
                time.sleep(frame_duration)
    
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
        self.is_audio_only = False
        self.subtitles = []
        self.subtitle_generator = None
        self.subtitles_enabled = True
        self.play_start_time = 0
        self.pause_position = 0
        self.translation_enabled = False
        self.translation_target = 'es'
        self.detected_language = None
        
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
    
    def set_video_output(self, widget):
        self.video_widget = widget
    
    def _extract_audio(self, video_path):
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

    def load_video(self, path):
        if self.cap:
            self.stop()
            self.cap.release()
        
        if self.audio_file and os.path.exists(self.audio_file):
            try:
                if not self.is_audio_only:
                    os.unlink(self.audio_file)
            except:
                pass
        
        self.subtitles = []
        self.pause_position = 0
        self.detected_language = None
        
        file_ext = os.path.splitext(path)[1].lower()
        if file_ext in ['.mp3', '.wav', '.ogg', '.flac', '.m4a']:
            self.is_audio_only = True
            self.cap = None
            self.audio_file = path
            
            try:
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.set_volume(self.volume / 100.0)
                self.generate_subtitles()
                # NO iniciar reproducción automáticamente
            except Exception as e:
                print(f"Error cargando audio: {e}")
        else:
            self.is_audio_only = False
            self.cap = cv2.VideoCapture(path)
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            
            self.audio_file = self._extract_audio(path)
            if self.audio_file:
                try:
                    pygame.mixer.music.load(self.audio_file)
                    pygame.mixer.music.set_volume(self.volume / 100.0)
                    self.generate_subtitles()
                    # NO iniciar reproducción automáticamente
                except:
                    pass


    
    def generate_subtitles(self):
        if self.audio_file and self.subtitles_enabled:
            self.subtitles = []
            self.subtitle_generator = SubtitleGenerator(self.audio_file)
            self.subtitle_generator.subtitle_ready.connect(self.add_subtitle)
            self.subtitle_generator.start()
    
    def add_subtitle(self, text, start_time, end_time, language):
        """Añade un subtítulo con traducción"""
        if self.detected_language is None:
            self.detected_language = language
        
        translated_text = ""
        if language != self.translation_target:
            try:
                # Usar deep-translator en lugar de googletrans
                translator = GoogleTranslator(source=language, target=self.translation_target)
                translated_text = translator.translate(text)
            except Exception as e:
                print(f"Error traduciendo: {e}")
                translated_text = text
        else:
            translated_text = text
        
        self.subtitles.append((text, translated_text, start_time, end_time, language))
        print(f"Subtítulo: [{language}] {text} | [{self.translation_target}] {translated_text}")
    
    def get_current_subtitle(self):
        if not self.subtitles_enabled:
            return ""
        
        current_pos = self.get_current_position()
        
        for original, translated, start, end, lang in self.subtitles:
            if (start - 0.1) <= current_pos <= end:
                if self.translation_enabled and translated:
                    return translated
                return original
        
        return ""
    
    def toggle_translation(self, target_language='es'):
        """Activa/desactiva la traducción"""
        self.translation_enabled = not self.translation_enabled
        
        if self.translation_enabled:
            if self.detected_language == target_language:
                self.translation_target = 'en' if target_language == 'es' else 'es'
            else:
                self.translation_target = target_language
        
        return self.translation_enabled, self.translation_target
    
    def toggle_subtitles(self):
        self.subtitles_enabled = not self.subtitles_enabled
        return self.subtitles_enabled
    
    def play(self):
        if not self.cap and not self.is_audio_only:
            return
            
        self.is_playing = True
        self.play_start_time = time.time() - self.pause_position
        
        if not self.is_audio_only and self.cap:
            if self.video_thread is None or not self.video_thread.isRunning():
                self.video_thread = VideoThread(self.cap, self.fps, self.play_start_time)
                self.video_thread.change_pixmap_signal.connect(self.update_frame)
                self.video_thread.start()
        
        if self.audio_file:
            try:
                if self.pause_position > 0:
                    pygame.mixer.music.play(start=self.pause_position)
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
        self.pause_position = self.get_current_position()
        
        if self.video_thread:
            self.video_thread.stop()
        pygame.mixer.music.pause()
    
    def stop(self):
        self.is_playing = False
        self.pause_position = 0
        
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
        if self.is_audio_only:
            try:
                sound = pygame.mixer.Sound(self.audio_file)
                return sound.get_length()
            except:
                return 0
        elif self.cap:
            frame_count = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            return frame_count / self.fps if self.fps > 0 else 0
        return 0
    
    def get_current_position(self):
        if not self.is_playing:
            return self.pause_position
        
        return time.time() - self.play_start_time
    
    def seek(self, seconds):
        was_playing = self.is_playing
        
        if self.video_thread:
            self.video_thread.stop()
        pygame.mixer.music.stop()
        
        self.pause_position = seconds
        
        if self.cap:
            frame_number = int(seconds * self.fps)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        if was_playing:
            self.play_start_time = time.time() - seconds
            self.play()
    
    def __del__(self):
        if self.video_thread:
            self.video_thread.stop()
        if self.cap:
            self.cap.release()
        if self.audio_file and os.path.exists(self.audio_file) and not self.is_audio_only:
            try:
                os.unlink(self.audio_file)
            except:
                pass
        pygame.mixer.quit()