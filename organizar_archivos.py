import os
import shutil
from pathlib import Path

# Script que organiza archivos por extensión
def organizar_descargas(carpeta):
    """
    Organiza archivos en subcarpetas según su tipo
    """
    # Diccionario de categorías
    tipos = {
        'Imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Documentos': ['.pdf', '.docx', '.txt', '.xlsx', 'pptx', 'htm', 'webp'],
        'Videos': ['.mp4', '.avi', '.mov'],
        'Comprimidos': ['.zip', '.rar', '.7z'],
        'programas': ['.exe', '.example','pptx', 'htm', 'webp']
    }
    
    # Crear carpetas si no existen
    for categoria in tipos.keys():
        Path(f"{carpeta}/{categoria}").mkdir(exist_ok=True)
    
    # Mover archivos
    archivos_movidos = 0
    for archivo in os.listdir(carpeta):
        if os.path.isfile(f"{carpeta}/{archivo}"):
            ext = Path(archivo).suffix.lower()
            
            for categoria, extensiones in tipos.items():
                if ext in extensiones:
                    origen = f"{carpeta}/{archivo}"
                    destino = f"{carpeta}/{categoria}/{archivo}"
                    shutil.move(origen, destino)
                    archivos_movidos += 1
                    print(f"✓ Movido: {archivo} → {categoria}/")
                    break
    
    print(f"\n🎯 Total organizado: {archivos_movidos} archivos")

# Ejemplo de uso (cambia la ruta)
if __name__ == "__main__":
    carpeta_descargas = r"C:\Users\Usuario\Downloads"
    organizar_descargas(carpeta_descargas)
