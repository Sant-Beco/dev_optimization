import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class OrganizadorArchivos:
    def __init__(self, carpeta_origen):
        self.carpeta_origen = carpeta_origen
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"logs/organizacion_{self.timestamp}.log"
        
        # Crear carpeta de logs si no existe
        Path("logs").mkdir(exist_ok=True)
        
        # Configuración de tipos (ahora fácil de modificar)
        self.tipos = {
            'Imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Documentos': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.doc'],
            'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv'],
            'Audio': ['.mp3', '.wav', '.flac', '.m4a'],
            'Comprimidos': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Codigo': ['.py', '.js', '.html', '.css', '.java', '.cpp'],
            'Otros': []  # Por defecto
        }
        
        # Estadísticas
        self.stats = {
            'archivos_procesados': 0,
            'archivos_movidos': 0,
            'errores': 0,
            'por_categoria': {}
        }
    
    def log(self, mensaje, nivel="INFO"):
        """Registra eventos en archivo y consola"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_mensaje = f"[{timestamp}] {nivel}: {mensaje}"
        
        # Escribir en archivo
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_mensaje + '\n')
        
        # Mostrar en consola con colores
        if nivel == "ERROR":
            print(f"❌ {mensaje}")
        elif nivel == "SUCCESS":
            print(f"✅ {mensaje}")
        else:
            print(f"ℹ️  {mensaje}")
    
    def crear_carpetas(self):
        """Crea las carpetas de destino"""
        for categoria in self.tipos.keys():
            carpeta_destino = Path(f"{self.carpeta_origen}/{categoria}")
            carpeta_destino.mkdir(exist_ok=True)
            self.stats['por_categoria'][categoria] = 0
        
        self.log("Carpetas de categorías creadas")
    
    def organizar(self):
        """Proceso principal de organización"""
        self.log(f"Iniciando organización de: {self.carpeta_origen}")
        self.crear_carpetas()
        
        try:
            archivos = [f for f in os.listdir(self.carpeta_origen) 
                       if os.path.isfile(os.path.join(self.carpeta_origen, f))]
            
            self.log(f"Archivos encontrados: {len(archivos)}")
            
            for archivo in archivos:
                self.stats['archivos_procesados'] += 1
                self.procesar_archivo(archivo)
            
            # Reporte final
            self.generar_reporte()
            
        except Exception as e:
            self.log(f"Error crítico en organización: {str(e)}", "ERROR")
    
    def procesar_archivo(self, archivo):
        """Procesa un archivo individual"""
        try:
            ext = Path(archivo).suffix.lower()
            categoria_destino = 'Otros'
            
            # Buscar categoría correspondiente
            for categoria, extensiones in self.tipos.items():
                if ext in extensiones:
                    categoria_destino = categoria
                    break
            
            # Construir rutas
            origen = os.path.join(self.carpeta_origen, archivo)
            destino = os.path.join(self.carpeta_origen, categoria_destino, archivo)
            
            # Verificar si ya existe
            if os.path.exists(destino):
                # Agregar timestamp al nombre para evitar sobrescribir
                nombre, extension = os.path.splitext(archivo)
                nuevo_nombre = f"{nombre}_{self.timestamp}{extension}"
                destino = os.path.join(self.carpeta_origen, categoria_destino, nuevo_nombre)
                self.log(f"Archivo duplicado renombrado: {archivo} → {nuevo_nombre}")
            
            # Mover archivo
            shutil.move(origen, destino)
            
            # Actualizar estadísticas
            self.stats['archivos_movidos'] += 1
            self.stats['por_categoria'][categoria_destino] += 1
            
            self.log(f"Movido: {archivo} → {categoria_destino}/", "SUCCESS")
            
        except PermissionError:
            self.log(f"Permiso denegado para mover: {archivo}", "ERROR")
            self.stats['errores'] += 1
        except Exception as e:
            self.log(f"Error al procesar {archivo}: {str(e)}", "ERROR")
            self.stats['errores'] += 1
    
    def generar_reporte(self):
        """Genera reporte final en JSON y texto"""
        self.log("\n" + "="*50)
        self.log("REPORTE FINAL DE ORGANIZACIÓN")
        self.log("="*50)
        self.log(f"Archivos procesados: {self.stats['archivos_procesados']}")
        self.log(f"Archivos movidos: {self.stats['archivos_movidos']}")
        self.log(f"Errores: {self.stats['errores']}")
        self.log("\nPor categoría:")
        
        for categoria, cantidad in self.stats['por_categoria'].items():
            if cantidad > 0:
                self.log(f"  - {categoria}: {cantidad} archivo(s)")
        
        # Guardar reporte en JSON
        reporte_json = f"logs/reporte_{self.timestamp}.json"
        with open(reporte_json, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        self.log(f"\nReporte guardado en: {reporte_json}")


# ============================================
# EJECUCIÓN
# ============================================
if __name__ == "__main__":
    # Configuración
    CARPETA_A_ORGANIZAR = "/ruta/a/tu/carpeta"  # ← CAMBIA ESTO
    
    print("\n🚀 ORGANIZADOR DE ARCHIVOS v2.0")
    print("="*50)
    
    # Verificar que la carpeta existe
    if not os.path.exists(CARPETA_A_ORGANIZAR):
        print(f"❌ Error: La carpeta {CARPETA_A_ORGANIZAR} no existe")
    else:
        organizador = OrganizadorArchivos(CARPETA_A_ORGANIZAR)
        organizador.organizar()
        print("\n✅ Proceso completado. Revisa la carpeta 'logs/' para detalles")