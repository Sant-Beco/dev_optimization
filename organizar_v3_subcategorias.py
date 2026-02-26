import os
import shutil
import json
from pathlib import Path
from datetime import datetime

class OrganizadorJerarquico:
    """Organizador con subcategorías inteligentes"""
    
    def __init__(self, carpeta_origen, dry_run=False):
        self.carpeta_origen = carpeta_origen
        self.dry_run = dry_run
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        Path("logs").mkdir(exist_ok=True)
        
        # Estructura jerárquica: Categoría → Subcategoría → Extensiones
        self.estructura = {
            'Imagenes': {
                'Fotos': ['.jpg', '.jpeg', '.heic'],
                'Graficos': ['.png', '.svg', '.webp'],
                'Animaciones': ['.gif']
            },
            'Documentos': {
                'PDFs': ['.pdf'],
                'Excel': ['.xlsx', '.xls', '.xlsm', '.csv'],
                'Word': ['.docx', '.doc', '.odt'],
                'Presentaciones': ['.pptx', '.ppt'],
                'Textos': ['.txt', '.md', '.rtf']
            },
            'Multimedia': {
                'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv'],
                'Audio': ['.mp3', '.wav', '.flac', '.m4a', '.aac']
            },
            'Archivos': {
                'Comprimidos': ['.zip', '.rar', '.7z', '.tar', '.gz'],
                'Codigo': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.sh'],
                'Ejecutables': ['.exe', '.dmg', '.app', '.deb']
            }
        }
        
        self.stats = {
            'timestamp': self.timestamp,
            'modo': 'dry-run' if dry_run else 'ejecucion',
            'archivos_procesados': 0,
            'archivos_movidos': 0,
            'errores': 0,
            'por_categoria': {},
            'por_subcategoria': {}
        }
    
    def crear_estructura(self):
        """Crea toda la jerarquía de carpetas"""
        print("📁 Creando estructura de carpetas...\n")
        
        for categoria, subcategorias in self.estructura.items():
            for subcategoria in subcategorias.keys():
                ruta = Path(f"{self.carpeta_origen}/{categoria}/{subcategoria}")
                
                if not self.dry_run:
                    ruta.mkdir(parents=True, exist_ok=True)
                
                # Inicializar contadores
                key = f"{categoria}/{subcategoria}"
                self.stats['por_subcategoria'][key] = 0
                
                if self.dry_run:
                    print(f"  CREARÍA: {key}/")
        
        # Categoría "Otros" sin subcategorías
        if not self.dry_run:
            Path(f"{self.carpeta_origen}/Otros").mkdir(exist_ok=True)
        self.stats['por_subcategoria']['Otros'] = 0
        
        print()
    
    def encontrar_ubicacion(self, extension):
        """Encuentra la categoría y subcategoría para una extensión"""
        ext_lower = extension.lower()
        
        for categoria, subcategorias in self.estructura.items():
            for subcategoria, extensiones in subcategorias.items():
                if ext_lower in extensiones:
                    return categoria, subcategoria
        
        return 'Otros', None
    
    def organizar(self):
        """Proceso principal de organización"""
        if self.dry_run:
            print("\n🔍 MODO DRY-RUN (Simulación)\n")
        else:
            print("\n🚀 ORGANIZANDO CON SUBCATEGORÍAS...\n")
        
        self.crear_estructura()
        
        try:
            # Obtener archivos (excluyendo carpetas ya creadas)
            archivos = []
            for item in os.listdir(self.carpeta_origen):
                ruta_completa = os.path.join(self.carpeta_origen, item)
                if os.path.isfile(ruta_completa):
                    archivos.append(item)
            
            print(f"📂 Archivos a procesar: {len(archivos)}\n")
            
            for archivo in archivos:
                self.procesar_archivo(archivo)
            
            self.mostrar_reporte()
            
            if not self.dry_run:
                self.guardar_reporte()
        
        except Exception as e:
            print(f"❌ Error crítico: {str(e)}")
    
    def procesar_archivo(self, archivo):
        """Procesa un archivo individual"""
        self.stats['archivos_procesados'] += 1
        
        ext = Path(archivo).suffix
        categoria, subcategoria = self.encontrar_ubicacion(ext)
        
        # Construir ruta destino
        if subcategoria:
            ruta_destino = f"{categoria}/{subcategoria}"
        else:
            ruta_destino = categoria
        
        # Actualizar estadísticas
        self.stats['por_subcategoria'][ruta_destino] = \
            self.stats['por_subcategoria'].get(ruta_destino, 0) + 1
        
        if self.dry_run:
            print(f"  MOVERÍA: {archivo:40} → {ruta_destino}/")
        else:
            try:
                origen = os.path.join(self.carpeta_origen, archivo)
                destino = os.path.join(self.carpeta_origen, ruta_destino, archivo)
                
                # Verificar duplicado
                if os.path.exists(destino):
                    nombre, extension = os.path.splitext(archivo)
                    nuevo_nombre = f"{nombre}_{self.timestamp}{extension}"
                    destino = os.path.join(self.carpeta_origen, ruta_destino, nuevo_nombre)
                    print(f"  ⚠️  Renombrado: {archivo} → {nuevo_nombre}")
                
                shutil.move(origen, destino)
                self.stats['archivos_movidos'] += 1
                print(f"  ✅ {archivo:40} → {ruta_destino}/")
                
            except Exception as e:
                print(f"  ❌ Error con {archivo}: {str(e)}")
                self.stats['errores'] += 1
    
    def mostrar_reporte(self):
        """Muestra reporte en consola"""
        print("\n" + "="*70)
        print("📊 REPORTE DE ORGANIZACIÓN JERÁRQUICA")
        print("="*70)
        
        print(f"\nArchivos procesados: {self.stats['archivos_procesados']}")
        
        if not self.dry_run:
            print(f"Archivos movidos: {self.stats['archivos_movidos']}")
            print(f"Errores: {self.stats['errores']}")
        
        print("\n📁 Distribución por ubicación:\n")
        
        # Agrupar por categoría principal
        categorias = {}
        for ubicacion, cantidad in self.stats['por_subcategoria'].items():
            if cantidad > 0:
                if '/' in ubicacion:
                    categoria = ubicacion.split('/')[0]
                else:
                    categoria = ubicacion
                
                if categoria not in categorias:
                    categorias[categoria] = []
                categorias[categoria].append((ubicacion, cantidad))
        
        # Mostrar organizado
        for categoria, items in sorted(categorias.items()):
            total_cat = sum(cant for _, cant in items)
            print(f"  📂 {categoria} ({total_cat} archivos)")
            
            for ubicacion, cantidad in sorted(items, key=lambda x: x[1], reverse=True):
                if '/' in ubicacion:
                    subcategoria = ubicacion.split('/')[1]
                    print(f"     └─ {subcategoria}: {cantidad}")
            print()
    
    def guardar_reporte(self):
        """Guarda reporte JSON"""
        archivo_reporte = f"logs/reporte_jerarquico_{self.timestamp}.json"
        
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Reporte guardado: {archivo_reporte}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🗂️  Organizador jerárquico con subcategorías',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--carpeta', '-c',
        type=str,
        required=True,
        help='Carpeta a organizar'
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Simulación (no mueve archivos)'
    )
    
    args = parser.parse_args()
    
    if not os.path.exists(args.carpeta):
        print(f"\n❌ Error: La carpeta '{args.carpeta}' no existe\n")
        return
    
    organizador = OrganizadorJerarquico(args.carpeta, dry_run=args.dry_run)
    organizador.organizar()


if __name__ == "__main__":
    main()