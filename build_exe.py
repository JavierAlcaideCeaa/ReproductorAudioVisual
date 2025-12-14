"""
Script para construir el ejecutable de ReproductorAudioVisual
Autor: Javier Alcaide Cea
"""

import PyInstaller.__main__
import os
import shutil

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    
    # Limpiar directorios anteriores
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    print("Construyendo ejecutable de ReproductorAudioVisual...")
    print("Este proceso puede tardar varios minutos...\n")
    
    # Configuración de PyInstaller
    PyInstaller.__main__.run([
        'src/main.py',                          # Script principal
        '--name=ReproductorAudioVisual',        # Nombre del ejecutable
        '--windowed',                            # Sin ventana de consola
        '--onefile',                             # Un solo archivo ejecutable
        '--icon=NONE',                           # Sin icono personalizado
        
        # Incluir módulos ocultos necesarios
        '--hidden-import=pygame',
        '--hidden-import=cv2',
        '--hidden-import=speech_recognition',
        '--hidden-import=pydub',
        '--hidden-import=langdetect',
        '--hidden-import=deep_translator',
        '--hidden-import=PyQt5',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        
        # Agregar archivos de datos
        '--add-data=src;src',
        
        # Configuración adicional
        '--noconfirm',                           # No pedir confirmación
        '--clean',                                # Limpiar caché
    ])
    
    print("\n¡Compilación completada!")
    print("Ejecutable creado en: dist/ReproductorAudioVisual.exe")
    print("\nNOTA: Para distribuir el ejecutable, asegúrate de que el usuario tenga:")
    print("  - FFmpeg instalado y en el PATH del sistema")
    print("  - Conexión a Internet (para reconocimiento de voz y traducción)")

if __name__ == '__main__':
    build_executable()
