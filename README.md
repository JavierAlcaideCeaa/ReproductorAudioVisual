# ReproductorAudioVisual
**Autor:** Javier Alcaide Cea

## Descripción

Reproductor multimedia avanzado desarrollado en Python con PyQt5 que permite reproducir archivos de video y audio con funcionalidades profesionales incluyendo generación automática de subtítulos, detección de idioma y traducción en tiempo real.

## Características Principales

### Reproducción Multimedia
- **Formatos de Video**: MP4, AVI, MKV, MOV
- **Formatos de Audio**: MP3, WAV, OGG, FLAC, M4A
- Sincronización perfecta entre audio y video
- Control de volumen en tiempo real
- Barra de progreso interactiva con seek clickeable

### Sistema de Subtítulos Inteligente
- **Generación automática de subtítulos** mediante reconocimiento de voz
- **Detección automática de idioma** (Español, Inglés, Francés, Alemán, Italiano, Portugués, Japonés, Chino, Coreano, Ruso)
- Subtítulos sincronizados con el audio/video
- Botón "Subtitles" para activar/desactivar subtítulos
- Interfaz limpia con fondo semi-transparente

### Traducción en Tiempo Real
- **Traducción automática de subtítulos**
- Traducción bidireccional Español ↔ Inglés
- Botón "Traducir" con indicador de idioma objetivo
- Cambio instantáneo entre idioma original y traducido

### Interfaz de Usuario
- Diseño moderno con tema oscuro
- Botones con efecto hover en color naranja (#ff8c00)
- Controles intuitivos y responsivos
- Visualización de tiempo actual/total
- Sliders de progreso y volumen personalizados

## Estructura del Proyecto

```
video-player-python/
├── src/
│   ├── main.py                    # Punto de entrada de la aplicación
│   ├── player.py                  # Lógica de reproducción y subtítulos
│   ├── ui.py                      # Interfaz gráfica principal
│   ├── SubtitleGenerator.py      # Generador de subtítulos con IA
│   ├── player_types.py            # Tipos y constantes
│   └── components/
│       ├── controls.py            # Controles de reproducción
│       └── video_widget.py        # Widget de visualización de video
├── tests/
│   └── test_player.py             # Tests unitarios
├── requirements.txt               # Dependencias del proyecto
├── pyproject.toml                 # Configuración del proyecto
└── README.md                      # Este archivo
```

## Requisitos Previos

### Software Necesario
- **Python 3.8 o superior** (compatible con Python 3.13)
- **FFmpeg** instalado y agregado al PATH del sistema

### Instalación de FFmpeg

#### Windows
1. Descargar FFmpeg de [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extraer el archivo ZIP
3. Agregar la carpeta `bin` al PATH de Windows

O usando Chocolatey:
```powershell
choco install ffmpeg
```

#### Linux
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS
```bash
brew install ffmpeg
```

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/JavierAlcaideCeaa/ReproductorAudioVisual.git
   cd video-player-python
   ```

2. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Dependencias

```
Flask                  # Framework web
PyQt5                  # Interfaz gráfica
opencv-python          # Procesamiento de video
numpy                  # Operaciones numéricas
pytest                 # Framework de testing
pygame                 # Reproducción de audio
SpeechRecognition      # Reconocimiento de voz
pydub                  # Manipulación de audio
langdetect             # Detección automática de idioma
deep-translator        # Traducción de texto
```

## Uso

### Ejecución Básica

```bash
cd src
python main.py
```

### Controles de la Aplicación

| Botón | Función |
|-------|---------|
| **Open** | Abrir archivo de video o audio |
| **Play** | Reproducir el archivo cargado |
| **Pause** | Pausar la reproducción |
| **Stop** | Detener y reiniciar al inicio |
| **Subtitles** | Activar/Desactivar subtítulos |
| **Traducir** | Activar/Desactivar traducción |
| **Progress Slider** | Navegar por el video (click para saltar) |
| **Volume Slider** | Ajustar el volumen (0-100) |

### Flujo de Trabajo

1. **Abrir Archivo**: Click en "Open" y seleccionar un archivo multimedia
2. **Reproducción Automática**: El archivo comenzará a reproducirse automáticamente
3. **Generación de Subtítulos**: Los subtítulos se generan automáticamente en segundo plano
4. **Control de Subtítulos**: 
   - Click en "Subtitles" para mostrar/ocultar subtítulos
   - Click en "Traducir" para cambiar entre idioma original y traducido
5. **Navegación**: Click en la barra de progreso para saltar a cualquier posición

## Características Técnicas

### Arquitectura del Sistema

#### VideoPlayer (player.py)
- Gestión de reproducción de video y audio
- Extracción de audio con FFmpeg
- Sistema de subtítulos con almacenamiento dual (original + traducción)
- Sincronización temporal mediante timestamps

#### SubtitleGenerator (SubtitleGenerator.py)
- Procesamiento de audio en chunks
- Detección de silencios para segmentación inteligente
- Reconocimiento de voz con Google Speech Recognition
- Detección automática de idioma con langdetect
- Traducción con deep-translator

#### VideoThread (player.py)
- Thread separado para renderizado de video
- Sincronización frame-by-frame
- Compensación de lag automática

### Algoritmos de Subtitulado

1. **Segmentación por Silencio**:
   - Detecta pausas de 300ms o más
   - Umbral ajustable: -16dB
   - Mantiene 150ms de contexto

2. **Segmentación por Tiempo Fijo**:
   - Chunks de 3 segundos
   - Fallback cuando hay pocas pausas
   - Garantiza cobertura completa

3. **Compensación de Latencia**:
   - Adelanto de 0.2 segundos en generación
   - Adelanto de 0.1 segundos en visualización
   - Ajustable según necesidad

## Resolución de Problemas

### El audio y el video no están sincronizados
- El sistema usa tiempo real como referencia
- Ajustar los valores de compensación en `src/SubtitleGenerator.py` línea 119 y `src/player.py` línea 168

### Los subtítulos no se generan
- Verificar que FFmpeg esté instalado y en el PATH
- Comprobar conexión a Internet (necesaria para reconocimiento de voz)
- Revisar la consola para mensajes de error

### Error "No module named 'cgi'"
- Asegurarse de usar `deep-translator` en lugar de `googletrans`
- Ejecutar: `pip uninstall googletrans && pip install deep-translator`

### Los subtítulos pierden algunas voces
- Ajustar `energy_threshold` en `src/SubtitleGenerator.py` (línea 20)
- Reducir `min_silence_len` para mayor sensibilidad (línea 51)

## Testing

Ejecutar los tests unitarios:

```bash
pytest tests/
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Mejoras Futuras

- [ ] Soporte para subtítulos .srt/.vtt externos
- [ ] Grabación de audio con subtítulos integrados
- [ ] Lista de reproducción
- [ ] Efectos de video (brillo, contraste, saturación)
- [ ] Ecualizador de audio
- [ ] Exportación de subtítulos generados
- [ ] Soporte para más idiomas de reconocimiento
- [ ] Cache de subtítulos para videos ya procesados

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.

## Agradecimientos

- **SpeechRecognition**: Por el reconocimiento de voz
- **deep-translator**: Por la traducción de texto
- **FFmpeg**: Por el procesamiento de audio/video
- **PyQt5**: Por la interfaz gráfica
- **pydub**: Por la manipulación de audio

## Contacto

**Javier Alcaide Cea**
- GitHub: [@JavierAlcaideCeaa](https://github.com/JavierAlcaideCeaa)
- Repositorio: [ReproductorAudioVisual](https://github.com/JavierAlcaideCeaa/ReproductorAudioVisual)

---

**Nota**: Este proyecto requiere conexión a Internet para las funciones de reconocimiento de voz y traducción.
