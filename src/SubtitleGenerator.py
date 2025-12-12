import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from PyQt5.QtCore import QThread, pyqtSignal

class SubtitleGenerator(QThread):
    subtitle_ready = pyqtSignal(str, float, float)  # texto, tiempo_inicio, tiempo_fin
    generation_finished = pyqtSignal()
    generation_progress = pyqtSignal(int)  # porcentaje de progreso
    
    def __init__(self, audio_path):
        super().__init__()
        self.audio_path = audio_path
        self.recognizer = sr.Recognizer()
        # Ajustar para mejor detección de voz
        self.recognizer.energy_threshold = 300  # Más sensible a voces suaves
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5  # Reducir pausa entre palabras
    
    def run(self):
        """Genera subtítulos del audio extraído"""
        try:
            # Cargar audio
            audio = AudioSegment.from_file(self.audio_path)
            
            # Método 1: Dividir por silencios (más precisos pero pueden perder algunas voces)
            chunks_silence = split_on_silence(
                audio,
                min_silence_len=300,  # Reducido de 500ms a 300ms
                silence_thresh=audio.dBFS - 16,  # Más sensible (era -14)
                keep_silence=150  # Reducido de 250ms a 150ms
            )
            
            # Método 2: Chunks de tiempo fijo (captura todo pero menos preciso)
            chunk_length_ms = 3000  # Chunks de 3 segundos
            chunks_fixed = []
            for i in range(0, len(audio), chunk_length_ms):
                chunk = audio[i:i + chunk_length_ms]
                if len(chunk) > 500:  # Mínimo 500ms
                    chunks_fixed.append(chunk)
            
            # Combinar ambos métodos: usar chunks por silencio si hay suficientes, sino usar fijos
            if len(chunks_silence) > len(audio) / 5000:  # Si hay al menos 1 chunk cada 5 segundos
                chunks = chunks_silence
                method = "silence"
            else:
                chunks = chunks_fixed
                method = "fixed"
            
            print(f"Usando método: {method}, {len(chunks)} chunks detectados")
            
            total_chunks = len(chunks)
            current_time = 0
            
            for i, chunk in enumerate(chunks):
                # Exportar chunk temporal
                chunk_file = f"temp_chunk_{i}.wav"
                chunk.export(chunk_file, format="wav")
                
                # Reconocer voz
                with sr.AudioFile(chunk_file) as source:
                    # Ajustar para ruido ambiente (primeros 0.2 segundos)
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio_data = self.recognizer.record(source)
                    
                    try:
                        # Usar reconocimiento de Google
                        text = self.recognizer.recognize_google(
                            audio_data, 
                            language='es-ES',
                            show_all=False  # Obtener la mejor coincidencia
                        )
                        
                        if text:  # Solo emitir si hay texto
                            # Calcular tiempos con un pequeño adelanto (compensar retardo)
                            duration = len(chunk) / 1000.0
                            # Adelantar el subtítulo 0.2 segundos para compensar retardo
                            start_time = max(0, current_time - 0.2)
                            end_time = start_time + duration
                            
                            self.subtitle_ready.emit(text, start_time, end_time)
                            print(f"[{start_time:.2f}s - {end_time:.2f}s] {text}")
                        
                        current_time += len(chunk) / 1000.0
                        
                    except sr.UnknownValueError:
                        # No se pudo reconocer el audio
                        current_time += len(chunk) / 1000.0
                        
                    except sr.RequestError as e:
                        print(f"Error en el servicio de reconocimiento: {e}")
                        current_time += len(chunk) / 1000.0
                
                # Limpiar archivo temporal
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
                
                # Emitir progreso
                if total_chunks > 0:
                    progress = int((i + 1) / total_chunks * 100)
                    self.generation_progress.emit(progress)
            
            self.generation_finished.emit()
            print("Generación de subtítulos completada")
                    
        except Exception as e:
            print(f"Error generando subtítulos: {e}")
            import traceback
            traceback.print_exc()
            self.generation_finished.emit()