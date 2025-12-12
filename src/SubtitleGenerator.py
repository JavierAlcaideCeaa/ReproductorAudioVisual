import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from PyQt5.QtCore import QThread, pyqtSignal
from langdetect import detect
from deep_translator import GoogleTranslator

class SubtitleGenerator(QThread):
    subtitle_ready = pyqtSignal(str, float, float, str)
    generation_finished = pyqtSignal()
    generation_progress = pyqtSignal(int)
    
    def __init__(self, audio_path):
        super().__init__()
        self.audio_path = audio_path
        self.recognizer = sr.Recognizer()
        self.detected_language = None
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5
        
        self.language_map = {
            'es': 'es-ES',
            'en': 'en-US',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-PT',
            'ja': 'ja-JP',
            'zh': 'zh-CN',
            'ko': 'ko-KR',
            'ru': 'ru-RU'
        }
    
    def detect_language_from_text(self, text):
        try:
            lang = detect(text)
            return lang
        except:
            return 'es'
    
    def run(self):
        try:
            audio = AudioSegment.from_file(self.audio_path)
            
            chunks_silence = split_on_silence(
                audio,
                min_silence_len=300,
                silence_thresh=audio.dBFS - 16,
                keep_silence=150
            )
            
            chunk_length_ms = 3000
            chunks_fixed = []
            for i in range(0, len(audio), chunk_length_ms):
                chunk = audio[i:i + chunk_length_ms]
                if len(chunk) > 500:
                    chunks_fixed.append(chunk)
            
            if len(chunks_silence) > len(audio) / 5000:
                chunks = chunks_silence
                method = "silence"
            else:
                chunks = chunks_fixed
                method = "fixed"
            
            print(f"Método: {method}, {len(chunks)} chunks")
            
            total_chunks = len(chunks)
            current_time = 0
            first_detection = True
            
            for i, chunk in enumerate(chunks):
                chunk_file = f"temp_chunk_{i}.wav"
                chunk.export(chunk_file, format="wav")
                
                with sr.AudioFile(chunk_file) as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio_data = self.recognizer.record(source)
                    
                    text = None
                    
                    if first_detection and self.detected_language is None:
                        languages_to_try = ['es-ES', 'en-US', 'fr-FR', 'de-DE', 'it-IT']
                        
                        for lang in languages_to_try:
                            try:
                                text = self.recognizer.recognize_google(audio_data, language=lang)
                                if text:
                                    detected_lang = self.detect_language_from_text(text)
                                    self.detected_language = self.language_map.get(detected_lang, lang)
                                    print(f"Idioma detectado: {self.detected_language}")
                                    first_detection = False
                                    break
                            except:
                                continue
                    else:
                        try:
                            text = self.recognizer.recognize_google(
                                audio_data,
                                language=self.detected_language or 'es-ES',
                                show_all=False
                            )
                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as e:
                            print(f"Error: {e}")
                    
                    if text:
                        duration = len(chunk) / 1000.0
                        start_time = max(0, current_time - 0.2)
                        end_time = start_time + duration
                        
                        lang_code = self.detected_language.split('-')[0] if self.detected_language else 'es'
                        self.subtitle_ready.emit(text, start_time, end_time, lang_code)
                        print(f"[{start_time:.2f}s] [{lang_code}] {text}")
                    
                    current_time += len(chunk) / 1000.0
                
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
                
                if total_chunks > 0:
                    progress = int((i + 1) / total_chunks * 100)
                    self.generation_progress.emit(progress)
            
            self.generation_finished.emit()
            print("Generación completada")
                    
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            self.generation_finished.emit()