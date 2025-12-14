# Instrucciones para Compilar ReproductorAudioVisual

**Autor:** Javier Alcaide Cea

## Requisitos Previos

Antes de compilar el ejecutable, asegúrate de tener instalado:

1. **Python 3.8+** (Recomendado: Python 3.11 o 3.13)
2. **FFmpeg** en el PATH del sistema
3. **Todas las dependencias** instaladas

### Instalación de Dependencias

```powershell
pip install -r requirements.txt
```

### Verificar FFmpeg

```powershell
ffmpeg -version
```

Si FFmpeg no está instalado:
- **Windows**: `choco install ffmpeg` (usando Chocolatey)
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

## Métodos de Compilación

### Método 1: Script Automático (Recomendado)

Ejecuta el script de automatización:

```powershell
python build_exe.py
```

Este script:
- Limpia compilaciones anteriores
- Configura PyInstaller automáticamente
- Incluye todos los módulos necesarios
- Crea un ejecutable optimizado en `dist/ReproductorAudioVisual.exe`

**Tiempo estimado:** 3-5 minutos

### Método 2: Archivo .spec Personalizado

Si necesitas más control sobre la compilación:

```powershell
pyinstaller ReproductorAudioVisual.spec
```

Este método usa el archivo de especificación predefinido con configuraciones optimizadas.

### Método 3: Comando Manual

Para compilación rápida sin configuraciones personalizadas:

```powershell
pyinstaller --name=ReproductorAudioVisual --windowed --onefile src/main.py
```

## Estructura de Salida

Después de la compilación exitosa:

```
video-player-python/
├── dist/
│   └── ReproductorAudioVisual.exe    ← Ejecutable final (137 MB aprox.)
├── build/                             ← Archivos temporales (puedes eliminar)
└── ReproductorAudioVisual.spec        ← Configuración de PyInstaller
```

## Resolución de Problemas

### Error: "ModuleNotFoundError"

Si falta algún módulo durante la compilación:

```powershell
pip install --upgrade [nombre-del-módulo]
```

Luego vuelve a compilar.

### Error: "No module named 'cgi'" (googletrans)

Asegúrate de usar `deep-translator` en lugar de `googletrans`:

```powershell
pip uninstall googletrans
pip install deep-translator
```

### El ejecutable no se crea

1. Verifica que todas las dependencias estén instaladas
2. Limpia los directorios de compilación:
   ```powershell
   Remove-Item -Recurse -Force dist, build
   ```
3. Vuelve a ejecutar `python build_exe.py`

### El ejecutable es muy grande (>100 MB)

Esto es normal debido a las dependencias:
- PyQt5: ~50 MB
- OpenCV: ~40 MB
- PyGame y otros: ~30 MB
- Código de aplicación: ~10 MB

**Total esperado:** 130-140 MB

Para reducir el tamaño:
- Usa `--onefile` (ya configurado)
- Activa compresión UPX (ya configurado)

### Error al ejecutar el .exe

Si el ejecutable falla al iniciarse:

1. **Ejecuta desde la consola** para ver errores:
   ```powershell
   .\dist\ReproductorAudioVisual.exe
   ```

2. **Verifica FFmpeg**:
   El usuario final debe tener FFmpeg instalado

3. **Recompila con consola visible** (para debug):
   Edita `build_exe.py` y cambia `--windowed` por `--console`

## Distribución del Ejecutable

### Opción 1: GitHub Releases (Recomendado)

Para archivos grandes como este ejecutable (137 MB):

1. Ve a tu repositorio en GitHub
2. Click en **"Releases"** → **"Create a new release"**
3. Asigna un tag (ej: `v1.0.0`)
4. Sube `dist/ReproductorAudioVisual.exe` como asset
5. Publica el release

**Ventajas:**
- Sin límite de tamaño de archivo (hasta 2 GB)
- Descarga directa para usuarios
- Versionado automático

### Opción 2: Servicios de Almacenamiento

Alternativas para distribución:
- **Google Drive** / **OneDrive**: Compartir enlace
- **Dropbox**: Enlace público
- **WeTransfer**: Transferencia temporal

### Opción 3: Archivo .zip Comprimido

Comprimir el ejecutable puede reducir el tamaño en ~30%:

```powershell
Compress-Archive -Path dist\ReproductorAudioVisual.exe -DestinationPath ReproductorAudioVisual.zip
```

## Requisitos para el Usuario Final

El usuario que ejecute `ReproductorAudioVisual.exe` necesita:

1. ✅ **Windows 10/11** (64-bit recomendado)
2. ✅ **FFmpeg** instalado y en el PATH
3. ✅ **Conexión a Internet** (para subtítulos y traducción)

**NO necesita:**
- ❌ Python instalado
- ❌ Dependencias pip
- ❌ Compiladores

## Actualizar el Ejecutable

Cuando hagas cambios en el código:

1. Modifica los archivos `.py` necesarios
2. Ejecuta nuevamente:
   ```powershell
   python build_exe.py
   ```
3. El nuevo ejecutable estará en `dist/`

## Testing del Ejecutable

Antes de distribuir, prueba:

1. **Reproducción de video**: MP4, AVI, MKV
2. **Reproducción de audio**: MP3, WAV, OGG
3. **Generación de subtítulos**: Con audio español e inglés
4. **Traducción**: Cambiar entre idiomas
5. **Controles**: Play, Pause, Stop, Seek, Volumen

## Notas Técnicas

### Módulos Incluidos en el Ejecutable

El ejecutable contiene:
- PyQt5 (interfaz gráfica)
- OpenCV (procesamiento de video)
- PyGame (reproducción de audio)
- SpeechRecognition (reconocimiento de voz)
- pydub (procesamiento de audio)
- langdetect (detección de idioma)
- deep-translator (traducción)
- NumPy (operaciones matemáticas)

### Dependencias Externas

**FFmpeg** NO está incluido en el ejecutable. El usuario debe instalarlo por separado.

## Contacto

Para problemas o sugerencias:
- **Autor**: Javier Alcaide Cea
- **Repositorio**: [ReproductorAudioVisual](https://github.com/tu-usuario/video-player-python)

---

**Última actualización**: Diciembre 2025
