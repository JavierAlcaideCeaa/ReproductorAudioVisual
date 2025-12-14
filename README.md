# ReproductorAudioVisual
**Autor:** Javier Alcaide Cea

## Descripción

**EL SEÑOR DE LOS REPRODUCTORES** - Reproductor multimedia avanzado desarrollado en Python con PyQt5 que permite reproducir archivos de video y audio con funcionalidades profesionales incluyendo generación automática de subtítulos con IA, detección inteligente de idioma y traducción en tiempo real.

## Características Principales

### Reproducción Multimedia
- **Formatos de Video**: MP4, AVI, MKV, MOV
- **Formatos de Audio**: MP3, WAV, OGG, FLAC, M4A
- Sincronización perfecta entre audio y video
- Control de volumen en tiempo real (0-100%)
- Barra de progreso interactiva con seek clickeable
- Pantalla de bienvenida épica "EL SEÑOR DE LOS REPRODUCTORES"

### Sistema de Subtítulos Inteligente con IA
- **Generación automática de subtítulos** mediante reconocimiento de voz (Google Speech Recognition)
- **Detección automática de idioma** usando machine learning
- Idiomas soportados: Español, Inglés, Francés, Alemán, Italiano, Portugués, Japonés, Chino, Coreano, Ruso
- Subtítulos sincronizados con el audio/video
- Botón "Subtitles" para activar/desactivar subtítulos
- Interfaz limpia con fondo semi-transparente

### Traducción en Tiempo Real
- **Traducción automática de subtítulos** con deep-translator
- Traducción bidireccional Español ↔ Inglés
- Botón "Traducir" con indicador de idioma objetivo (→ Español / → English)
- Cambio instantáneo entre idioma original y traducido
- Sin necesidad de cargar subtítulos externos

### Interfaz de Usuario Moderna
- Diseño oscuro profesional con tema naranja (#ff8c00)
- Botones con efectos hover y animaciones
- Controles intuitivos y responsivos
- Visualización de tiempo actual/total (HH:MM:SS)
- Sliders personalizados de progreso y volumen
- Responsive design que se adapta al tamaño de ventana

## Estructura del Proyecto

```
video-player-python/
├── src/
│   ├── main.py                    # Punto de entrada de la aplicación
│   ├── player.py                  # Lógica de reproducción y subtítulos
│   ├── ui.py                      # Interfaz gráfica principal
│   ├── SubtitleGenerator.py      # Generador de subtítulos con IA
│   ├── AudioExtractor.py          # Extractor de audio con FFmpeg
│   ├── player_types.py            # Tipos y constantes
│   └── components/
│       ├── controls.py            # Controles de reproducción
│       └── video_widget.py        # Widget de visualización de video
├── tests/
│   └── test_player.py             # Tests unitarios
├── build_exe.py                   # Script de compilación del ejecutable
├── ReproductorAudioVisual.spec    # Configuración de PyInstaller
├── BUILD_INSTRUCTIONS.md          # Guía de compilación detallada
├── requirements.txt               # Dependencias del proyecto
├── pyproject.toml                 # Configuración del proyecto
├── .gitignore                     # Exclusiones de Git
└── README.md                      # Este archivo
```

## Requisitos Previos

### Para Ejecutar desde Código Fuente

#### Software Necesario
- **Python 3.8 o superior** (Recomendado: Python 3.11 o 3.13)
- **FFmpeg** instalado y agregado al PATH del sistema
- **Conexión a Internet** (para reconocimiento de voz y traducción)

#### Instalación de FFmpeg

**Windows:**
```powershell
# Opción 1: Usando Chocolatey (recomendado)
choco install ffmpeg

# Opción 2: Manual
# 1. Descargar de https://ffmpeg.org/download.html
# 2. Extraer el archivo ZIP
# 3. Agregar la carpeta 'bin' al PATH de Windows
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Verificar instalación:**
```powershell
ffmpeg -version
```

### Para Ejecutar el Archivo Ejecutable (.exe)

Si descargas el ejecutable precompilado desde [GitHub Releases](https://github.com/JavierAlcaideCeaa/ReproductorAudioVisual/releases):

**Necesitas:**
- Windows 10/11 (64-bit)
- FFmpeg instalado en el sistema
- Conexión a Internet

**NO necesitas:**
- Python instalado
- Dependencias pip
- Compiladores o herramientas de desarrollo

## Instalación y Configuración

### Opción 1: Descargar Ejecutable (Más Fácil)

1. **Descargar el ejecutable desde GitHub Releases:**
   - Ve a [Releases](https://github.com/JavierAlcaideCeaa/ReproductorAudioVisual/releases)
   - Descarga `ReproductorAudioVisual.exe` (~137 MB)
   - Ejecuta el archivo directamente

2. **Instalar FFmpeg** (requisito obligatorio)

3. **¡Listo!** Ejecuta `ReproductorAudioVisual.exe`

### Opción 2: Ejecutar desde Código Fuente

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/JavierAlcaideCeaa/ReproductorAudioVisual.git
   cd ReproductorAudioVisual
   ```

2. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**
   ```bash
   cd src
   python main.py
   ```

### Opción 3: Compilar tu Propio Ejecutable

Para crear un ejecutable de Windows (.exe):

```powershell
# Instalar dependencias (incluye PyInstaller)
pip install -r requirements.txt

# Compilar el ejecutable
python build_exe.py
```

El ejecutable se creará en `dist/ReproductorAudioVisual.exe`

📖 **Para instrucciones detalladas de compilación**, consulta [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

## Dependencias

El proyecto utiliza las siguientes librerías de Python:

```
PyQt5              # Interfaz gráfica de usuario
opencv-python      # Procesamiento y reproducción de video
pygame             # Reproducción de audio con sincronización
numpy              # Operaciones numéricas y procesamiento de arrays
SpeechRecognition  # Reconocimiento de voz (Google Speech API)
pydub              # Manipulación y procesamiento de audio
langdetect         # Detección automática de idioma con ML
deep-translator    # Traducción de texto multi-idioma
pyinstaller        # Compilación de ejecutables (solo para desarrollo)
pytest             # Framework de testing (solo para desarrollo)
```

**Dependencias Externas:**
- **FFmpeg**: Necesario para extracción de audio y procesamiento multimedia

## Uso

### Inicio de la Aplicación

**Desde ejecutable:**
```
Doble click en ReproductorAudioVisual.exe
```

**Desde código fuente:**
```bash
cd src
python main.py
```

### Primera Ejecución

1. La aplicación se abre mostrando la pantalla de inicio: **"EL SEÑOR DE LOS REPRODUCTORES"**
2. Click en el botón **"Open"** para seleccionar un archivo multimedia
3. O presiona **"Play"** para que se abra automáticamente el selector de archivos
4. Una vez cargado el archivo, presiona **"Play"** manualmente para comenzar la reproducción

### Controles de la Aplicación

| Botón | Función | Atajo |
|-------|---------|-------|
| **Open** | Abrir archivo de video o audio | - |
| **Play** | Reproducir el archivo cargado | - |
| **Pause** | Pausar la reproducción | - |
| **Stop** | Detener y reiniciar al inicio | - |
| **Subtitles** | Activar/Desactivar subtítulos | Botón toggleable |
| **Traducir** | Activar/Desactivar traducción | Muestra idioma objetivo |
| **Progress Slider** | Navegar por el video (click para saltar) | Click en cualquier posición |
| **Volume Slider** | Ajustar el volumen (0-100) | Desliza o click |

### Flujo de Trabajo Completo

1. **Cargar Archivo**: 
   - Click en "Open" → Seleccionar archivo (MP4, MP3, etc.)
   - El título de bienvenida desaparece automáticamente

2. **Reproducción**: 
   - Presiona "Play" para iniciar manualmente
   - El botón cambia a "Pause" durante la reproducción

3. **Generación de Subtítulos** (automática en segundo plano):
   - El sistema extrae el audio del video
   - Detecta automáticamente el idioma del contenido
   - Genera subtítulos sincronizados con IA
   - Los subtítulos aparecen en tiempo real

4. **Control de Subtítulos**: 
   - Click en "Subtitles" para mostrar/ocultar subtítulos
   - Click en "Traducir" para activar traducción
   - El botón muestra el idioma objetivo: "→ Español" o "→ English"

5. **Navegación**: 
   - Click en cualquier punto de la barra de progreso para saltar
   - Ajusta el volumen con el slider lateral
   - Los tiempos se muestran en formato MM:SS o HH:MM:SS

### Tipos de Archivos Soportados

**Videos:**
- `.mp4` - MPEG-4 Video
- `.avi` - Audio Video Interleave
- `.mkv` - Matroska Video
- `.mov` - QuickTime Movie

**Audio:**
- `.mp3` - MPEG Audio Layer 3
- `.wav` - Waveform Audio
- `.ogg` - Ogg Vorbis
- `.flac` - Free Lossless Audio Codec
- `.m4a` - MPEG-4 Audio

## Características Técnicas

### Arquitectura del Sistema

#### VideoPlayer (`player.py`)
- **Gestión de reproducción** de video y audio con OpenCV y PyGame
- **Extracción de audio** automática usando FFmpeg
- **Sistema de subtítulos dual**: almacena texto original + traducción
- **Sincronización temporal** mediante timestamps de tiempo real
- **Manejo de estado**: play, pause, stop, seek
- **Thread de video** separado para renderizado no bloqueante

#### SubtitleGenerator (`SubtitleGenerator.py`)
- **Procesamiento de audio** en chunks inteligentes
- **Detección de silencios** para segmentación automática (pydub)
- **Reconocimiento de voz** con Google Speech Recognition API
- **Detección de idioma** con langdetect (machine learning)
- **Traducción automática** con deep-translator
- **Procesamiento en background** usando QThread de PyQt5

#### VideoThread (clase interna en `player.py`)
- **Thread separado** para renderizado de frames
- **Sincronización frame-by-frame** con FPS del video
- **Compensación automática de lag** (adelanto/retraso)
- **Emisión de señales** para actualización de UI

#### UserInterface (`ui.py`)
- **Diseño responsivo** con PyQt5
- **Pantalla de bienvenida** épica al inicio
- **Subtítulos overlay** con fondo semi-transparente
- **Actualización de UI** cada 100ms con QTimer
- **Manejo de eventos** de redimensionamiento

### Algoritmos de Subtitulado Inteligente

#### 1. **Segmentación por Silencio** (Método Principal)
```python
Parámetros:
- min_silence_len: 300ms    # Detecta pausas de 0.3 segundos
- silence_thresh: -16dB     # Umbral relativo al volumen promedio
- keep_silence: 150ms       # Mantiene contexto antes/después
```
**Ventajas:** Segmentación natural según pausas del hablante

#### 2. **Segmentación por Tiempo Fijo** (Fallback)
```python
Parámetros:
- chunk_length: 3000ms      # Chunks de 3 segundos
- min_chunk_length: 500ms   # Descarta chunks muy cortos
```
**Ventajas:** Garantiza cobertura cuando hay pocas pausas

#### 3. **Compensación de Latencia Temporal**
```python
start_time = current_time - 0.2s   # Adelanto en generación
```
**Ventajas:** Mejora la sincronización subtítulo-audio

### Detección de Idioma Multi-Nivel

1. **Primera fase**: Intenta reconocimiento con 5 idiomas comunes
   - Español (es-ES)
   - Inglés (en-US)
   - Francés (fr-FR)
   - Alemán (de-DE)
   - Italiano (it-IT)

2. **Segunda fase**: Usa langdetect para confirmar idioma del texto reconocido

3. **Caché**: El idioma detectado se usa para los chunks restantes

### Sistema de Traducción

- **Biblioteca**: deep-translator (compatible con Python 3.13+)
- **Dirección**: Bidireccional ES ↔ EN
- **Almacenamiento**: Cada subtítulo guarda original + traducción
- **Toggle**: Cambio instantáneo sin regenerar subtítulos

## Resolución de Problemas

### El audio y el video no están sincronizados
**Causa:** Diferencia entre tiempo de procesamiento y tiempo real

**Solución:**
- El sistema usa `time.time()` como referencia absoluta
- Ajustar valores de compensación:
  - `SubtitleGenerator.py` línea 119: `start_time = current_time - 0.2`
  - Aumentar/disminuir el valor `-0.2` según sea necesario

### Los subtítulos no se generan
**Causas posibles:**

1. **FFmpeg no instalado**
   ```powershell
   ffmpeg -version  # Verificar instalación
   ```
   **Solución:** Instalar FFmpeg y agregarlo al PATH

2. **Sin conexión a Internet**
   - Google Speech Recognition requiere conexión
   **Solución:** Conectarse a Internet

3. **Audio inaudible o muy bajo**
   **Solución:** Ajustar `energy_threshold` en `SubtitleGenerator.py`:
   ```python
   self.recognizer.energy_threshold = 200  # Más sensible
   ```

### Error: "No module named 'cgi'" (con googletrans)
**Causa:** googletrans no es compatible con Python 3.13+

**Solución:**
```powershell
pip uninstall googletrans
pip install deep-translator
```
Ya está configurado en `requirements.txt` actual

### Los subtítulos pierden algunas voces
**Causa:** Umbral de energía muy alto o silencios muy largos

**Soluciones:**

1. **Aumentar sensibilidad del reconocedor:**
   ```python
   # En SubtitleGenerator.py línea 20
   self.recognizer.energy_threshold = 200  # Reducir de 300 a 200
   ```

2. **Reducir duración mínima de silencio:**
   ```python
   # En SubtitleGenerator.py línea 51
   min_silence_len=200,  # Cambiar de 300 a 200
   ```

3. **Ajustar umbral de silencio:**
   ```python
   # En SubtitleGenerator.py línea 52
   silence_thresh=audio.dBFS - 14,  # Cambiar de -16 a -14
   ```

### El ejecutable (.exe) no se ejecuta
**Diagnóstico:**

1. **Ejecutar desde terminal para ver errores:**
   ```powershell
   cd dist
   .\ReproductorAudioVisual.exe
   ```

2. **Verificar dependencias:**
   - FFmpeg debe estar en el PATH del sistema
   - Conexión a Internet activa

3. **Recompilar con consola visible** (para debug):
   ```python
   # En build_exe.py, cambiar:
   '--windowed',  # ← Eliminar esta línea
   '--console',   # ← Agregar esta línea
   ```

### Error: "Could not find ffmpeg"
**Solución Windows:**
```powershell
# 1. Verificar instalación
where ffmpeg

# 2. Si no está instalado, usar Chocolatey
choco install ffmpeg

# 3. O agregar manualmente al PATH:
# Panel de Control → Sistema → Variables de entorno
# Agregar ruta de ffmpeg\bin a la variable PATH
```

### Los subtítulos aparecen con mucho retraso
**Solución:** Aumentar la compensación de tiempo
```python
# En SubtitleGenerator.py línea 119
start_time = max(0, current_time - 0.5)  # Aumentar de 0.2 a 0.5
```

### Error: "ModuleNotFoundError" al compilar
**Solución:** Reinstalar dependencias
```powershell
pip install --upgrade -r requirements.txt
python build_exe.py
```

### El volumen no funciona
**Causa:** pygame.mixer no inicializado correctamente

**Solución:** Reiniciar la aplicación. Si persiste, verificar:
```python
# En player.py, verificar inicialización:
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
```

## Testing

### Ejecutar Tests Unitarios

```bash
# Ejecutar todos los tests
pytest tests/

# Ejecutar con verbose
pytest tests/ -v

# Ejecutar tests específicos
pytest tests/test_player.py

# Con cobertura de código
pytest tests/ --cov=src
```

### Tests Manuales Recomendados

Antes de distribuir el ejecutable, verifica:

- [ ] **Reproducción de video**: Probar con MP4, AVI, MKV
- [ ] **Reproducción de audio**: Probar con MP3, WAV, OGG
- [ ] **Generación de subtítulos**: Audio en español e inglés
- [ ] **Detección de idioma**: Verificar detección correcta
- [ ] **Traducción**: Cambiar entre idiomas original/traducido
- [ ] **Controles**: Play, Pause, Stop funcionan correctamente
- [ ] **Seek**: Click en barra de progreso salta correctamente
- [ ] **Volumen**: Slider ajusta volumen correctamente
- [ ] **Sincronización**: Audio y video están sincronizados
- [ ] **Pantalla de inicio**: Título aparece correctamente
- [ ] **Subtítulos**: Aparecen sincronizados con el audio

## Compilación del Ejecutable

### Compilación Rápida

```powershell
# Instalar dependencias (incluye PyInstaller)
pip install -r requirements.txt

# Ejecutar script de compilación
python build_exe.py
```

**Resultado:** `dist/ReproductorAudioVisual.exe` (~137 MB)

### Compilación Manual

```powershell
pyinstaller --name=ReproductorAudioVisual --windowed --onefile src/main.py
```

### Distribución del Ejecutable

#### Opción 1: GitHub Releases (Recomendado)

Para archivos grandes (>100 MB):

1. Ve a tu repositorio en GitHub
2. Click en **"Releases"** → **"Create a new release"**
3. Asigna un tag de versión (ej: `v1.0.0`)
4. Arrastra `dist/ReproductorAudioVisual.exe` como asset
5. Publica el release

**Ventajas:**
- Soporta archivos hasta 2 GB
- Descarga directa para usuarios
- Versionado automático
- Changelog integrado

#### Opción 2: Archivo Comprimido

Comprimir puede reducir el tamaño ~30%:

```powershell
Compress-Archive -Path dist\ReproductorAudioVisual.exe -DestinationPath ReproductorAudioVisual-v1.0.0.zip
```

**Instrucciones completas:** Consulta [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

## Contribuciones

Las contribuciones son bienvenidas y apreciadas. Para contribuir:

### Proceso de Contribución

1. **Fork el repositorio**
   ```bash
   # Click en "Fork" en GitHub
   ```

2. **Clonar tu fork**
   ```bash
   git clone https://github.com/TU-USUARIO/ReproductorAudioVisual.git
   cd ReproductorAudioVisual
   ```

3. **Crear una rama para tu feature**
   ```bash
   git checkout -b feature/NombreDelFeature
   ```

4. **Hacer cambios y commit**
   ```bash
   git add .
   git commit -m "Descripción clara del cambio"
   ```

5. **Push a tu fork**
   ```bash
   git push origin feature/NombreDelFeature
   ```

6. **Crear Pull Request**
   - Ve a GitHub y crea un Pull Request
   - Describe los cambios realizados
   - Espera revisión

### Áreas de Contribución

- Reportar bugs
- Proponer nuevas features
- Mejorar documentación
- Agregar soporte para más idiomas
- Mejorar el diseño de UI
- Optimizar rendimiento
- Agregar más tests

### Guías de Estilo

- **Python**: Seguir PEP 8
- **Commits**: Mensajes descriptivos en inglés o español
- **Código**: Comentarios en español para coherencia

## Mejoras Futuras

### En Desarrollo
- [ ] Sistema de plugins para extensibilidad
- [ ] Soporte para más idiomas de traducción
- [ ] Cache inteligente de subtítulos generados

### Planificadas
- [ ] Soporte para subtítulos .srt/.vtt externos
- [ ] Exportación de subtítulos generados a archivo
- [ ] Grabación de audio con subtítulos integrados (hardsubbing)
- [ ] Lista de reproducción (playlist)
- [ ] Efectos de video (brillo, contraste, saturación, filtros)
- [ ] Ecualizador de audio con presets
- [ ] Atajos de teclado personalizables
- [ ] Marcadores/bookmarks para posiciones del video
- [ ] Captura de screenshots del video
- [ ] Picture-in-Picture mode
- [ ] Soporte para streaming de URLs
- [ ] Temas personalizables (modo claro/oscuro)
- [ ] Historial de archivos reproducidos
- [ ] Sincronización de subtítulos manual (ajuste de offset)

### Contribuciones Bienvenidas
- Interfaz multi-idioma (i18n)
- Visualizador de espectro de audio
- Estadísticas de reproducción
- Integración con servicios en la nube

## Agradecimientos

Este proyecto utiliza tecnologías y bibliotecas de código abierto:

- **[SpeechRecognition](https://github.com/Uberi/speech_recognition)** - Por el reconocimiento de voz con Google Speech API
- **[deep-translator](https://github.com/nidhaloff/deep-translator)** - Por la traducción multi-idioma
- **[FFmpeg](https://ffmpeg.org/)** - Por el procesamiento de audio y video
- **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/)** - Por la interfaz gráfica moderna
- **[pydub](https://github.com/jiaaro/pydub)** - Por la manipulación de audio
- **[OpenCV](https://opencv.org/)** - Por el procesamiento de video
- **[pygame](https://www.pygame.org/)** - Por la reproducción de audio sincronizada
- **[langdetect](https://github.com/Mimino666/langdetect)** - Por la detección de idioma con ML

Un agradecimiento especial a la comunidad de código abierto por hacer posible este proyecto.

## Contacto y Soporte

### Autor
**Javier Alcaide Cea**

### Enlaces
- GitHub: [@JavierAlcaideCeaa](https://github.com/JavierAlcaideCeaa)
- Repositorio: [ReproductorAudioVisual](https://github.com/JavierAlcaideCeaa/ReproductorAudioVisual)
- Reportar Issues: [GitHub Issues](https://github.com/JavierAlcaideCeaa/ReproductorAudioVisual/issues)
- Discusiones: [GitHub Discussions](https://github.com/JavierAlcaideCeaa/ReproductorAudioVisual/discussions)

### Soporte

Si encuentras algún problema o tienes sugerencias:

1. **Revisa** la sección [Resolución de Problemas](#resolución-de-problemas)
2. **Busca** en [Issues existentes](https://github.com/JavierAlcaideCeaa/ReproductorAudioVisual/issues)
3. **Crea** un nuevo Issue si no existe uno similar
4. **Incluye**:
   - Descripción del problema
   - Pasos para reproducirlo
   - Versión de Python y sistema operativo
   - Logs de error (si aplica)

---

<div align="center">

**Si te gusta este proyecto, dale una estrella en GitHub**

Desarrollado por Javier Alcaide Cea

*"EL SEÑOR DE LOS REPRODUCTORES"*

</div>

---

**Nota**: Este proyecto requiere conexión a Internet para las funciones de reconocimiento de voz y traducción.
