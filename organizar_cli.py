import os
import shutil
import json
import argparse
from pathlib import Path
from datetime import datetime

class OrganizadorArchivos:
    """Versión CLI del organizador"""
    
    def __init__(self, carpeta_origen, dry_run=False, verbose=False):
        self.carpeta_origen = carpeta_origen
        self.dry_run = dry_run
        self.verbose = verbose
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        Path("logs").mkdir(exist_ok=True)
        
        self.tipos = {
            'Imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Documentos': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.doc'],
            'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv'],
            'Audio': ['.mp3', '.wav', '.flac', '.m4a'],
            'Comprimidos': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Codigo': ['.py', '.js', '.html', '.css', '.java', '.cpp'],
            'Otros': []
        }
        
        self.stats = {
            'carpeta': carpeta_origen,
            'timestamp': self.timestamp,
            'modo': 'dry-run' if dry_run else 'ejecucion',
            'archivos_procesados': 0,
            'archivos_movidos': 0,
            'errores': 0,
            'por_categoria': {cat: 0 for cat in self.tipos.keys()}
        }
    
    def organizar(self):
        """Proceso principal"""
        if self.dry_run:
            print("\n🔍 MODO DRY-RUN (simulación, no se moverán archivos)\n")
        else:
            print("\n🚀 ORGANIZANDO ARCHIVOS...\n")
        
        # Crear carpetas de destino
        if not self.dry_run:
            for categoria in self.tipos.keys():
                Path(f"{self.carpeta_origen}/{categoria}").mkdir(exist_ok=True)
        
        # Procesar archivos
        try:
            archivos = [f for f in os.listdir(self.carpeta_origen) 
                       if os.path.isfile(os.path.join(self.carpeta_origen, f))]
            
            print(f"📂 Archivos encontrados: {len(archivos)}\n")
            
            for archivo in archivos:
                self.procesar_archivo(archivo)
            
            self.mostrar_reporte()
            
            if not self.dry_run:
                self.guardar_reporte()
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def procesar_archivo(self, archivo):
        """Procesa un archivo individual"""
        self.stats['archivos_procesados'] += 1
        ext = Path(archivo).suffix.lower()
        categoria = 'Otros'
        
        for cat, extensiones in self.tipos.items():
            if ext in extensiones:
                categoria = cat
                break
        
        self.stats['por_categoria'][categoria] += 1
        
        if self.verbose or self.dry_run:
            accion = "MOVERÍA" if self.dry_run else "Moviendo"
            print(f"  {accion}: {archivo} → {categoria}/")
        
        if not self.dry_run:
            try:
                origen = os.path.join(self.carpeta_origen, archivo)
                destino = os.path.join(self.carpeta_origen, categoria, archivo)
                shutil.move(origen, destino)
                self.stats['archivos_movidos'] += 1
            except Exception as e:
                print(f"  ❌ Error con {archivo}: {str(e)}")
                self.stats['errores'] += 1
    
    def mostrar_reporte(self):
        """Reporte en consola"""
        print("\n" + "="*50)
        print("📊 REPORTE FINAL")
        print("="*50)
        print(f"Archivos procesados: {self.stats['archivos_procesados']}")
        
        if not self.dry_run:
            print(f"Archivos movidos: {self.stats['archivos_movidos']}")
            print(f"Errores: {self.stats['errores']}")
        
        print("\n📁 Por categoría:")
        for cat, cantidad in self.stats['por_categoria'].items():
            if cantidad > 0:
                print(f"  • {cat}: {cantidad}")
        print()
    
    def guardar_reporte(self):
        """Guarda reporte JSON"""
        archivo_reporte = f"logs/reporte_{self.timestamp}.json"
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
        print(f"💾 Reporte guardado: {archivo_reporte}\n")


def analizar_logs():
    """Analiza todos los reportes históricos"""
    print("\n📊 ANALIZANDO LOGS HISTÓRICOS...\n")
    
    reportes = list(Path("logs").glob("reporte_*.json"))
    
    if not reportes:
        print("❌ No se encontraron reportes previos")
        return
    
    print(f"Reportes encontrados: {len(reportes)}\n")
    
    total_archivos = 0
    total_errores = 0
    categorias_global = {}
    
    for reporte_path in reportes:
        with open(reporte_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            total_archivos += data.get('archivos_procesados', 0)
            total_errores += data.get('errores', 0)
            
            for cat, cant in data.get('por_categoria', {}).items():
                categorias_global[cat] = categorias_global.get(cat, 0) + cant
            
            print(f"📄 {reporte_path.name}")
            print(f"   Fecha: {data.get('timestamp', 'N/A')}")
            print(f"   Archivos: {data.get('archivos_procesados', 0)}")
            print()
    
    print("="*50)
    print("🎯 RESUMEN TOTAL")
    print("="*50)
    print(f"Total archivos organizados: {total_archivos}")
    print(f"Total errores: {total_errores}")
    print(f"Tasa de éxito: {((total_archivos-total_errores)/total_archivos*100):.1f}%")
    print("\n📊 Distribución por tipo:")
    
    for cat, cant in sorted(categorias_global.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (cant/total_archivos*100) if total_archivos > 0 else 0
        barra = "█" * int(porcentaje/5)
        print(f"  {cat:15} {cant:4} ({porcentaje:5.1f}%) {barra}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='🗂️  Organizador inteligente de archivos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python organizar_cli.py --carpeta ~/Descargas
  python organizar_cli.py --carpeta ~/Documentos --dry-run
  python organizar_cli.py --carpeta ~/Descargas --verbose
  python organizar_cli.py --analizar-logs
        """
    )
    
    parser.add_argument(
        '--carpeta', '-c',
        type=str,
        help='Ruta de la carpeta a organizar'
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Simulación (no mueve archivos, solo muestra qué haría)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Modo detallado (muestra cada archivo procesado)'
    )
    
    parser.add_argument(
        '--analizar-logs', '-a',
        action='store_true',
        help='Analiza todos los reportes históricos'
    )
    
    args = parser.parse_args()
    
    # Ejecutar análisis de logs
    if args.analizar_logs:
        analizar_logs()
        return
    
    # Validar carpeta
    if not args.carpeta:
        parser.print_help()
        print("\n❌ Error: Debes especificar --carpeta o --analizar-logs\n")
        return
    
    if not os.path.exists(args.carpeta):
        print(f"\n❌ Error: La carpeta '{args.carpeta}' no existe\n")
        return
    
    # Ejecutar organización
    organizador = OrganizadorArchivos(
        args.carpeta, 
        dry_run=args.dry_run,
        verbose=args.verbose
    )
    organizador.organizar()


if __name__ == "__main__":
    main()