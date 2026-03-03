import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import re

class LimpiadorCSV:
    """Limpia y analiza cualquier CSV automáticamente"""
    
    def __init__(self, archivo_csv):
        self.archivo = archivo_csv
        self.df = None
        self.df_original = None
        self.reporte = {
            'archivo': archivo_csv,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'filas_originales': 0,
            'columnas_originales': 0,
            'cambios': []
        }
    
    def cargar(self):
        """Carga el CSV con detección automática"""
        print(f"\n📂 Cargando: {self.archivo}\n")
        
        try:
            # Intentar diferentes encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    self.df = pd.read_csv(self.archivo, encoding=encoding)
                    print(f"✅ Codificación detectada: {encoding}")
                    break
                except:
                    continue
            
            if self.df is None:
                raise Exception("No se pudo leer el archivo con ninguna codificación")
            
            self.df_original = self.df.copy()
            self.reporte['filas_originales'] = len(self.df)
            self.reporte['columnas_originales'] = len(self.df.columns)
            
            print(f"📊 Dimensiones: {len(self.df)} filas × {len(self.df.columns)} columnas\n")
            return True
            
        except Exception as e:
            print(f"❌ Error al cargar: {str(e)}")
            return False
    
    def analizar_inicial(self):
        """Análisis rápido de calidad de datos"""
        print("="*70)
        print("🔍 ANÁLISIS INICIAL DE CALIDAD")
        print("="*70)
        
        print(f"\n📋 Columnas encontradas: {list(self.df.columns)}\n")
        
        # Información por columna
        for col in self.df.columns:
            nulos = self.df[col].isna().sum()
            unicos = self.df[col].nunique()
            tipo = self.df[col].dtype
            
            print(f"  • {col:25} | Tipo: {str(tipo):10} | Nulos: {nulos:4} | Únicos: {unicos:4}")
        
        print()
    
    def limpiar_nombres_columnas(self):
        """Normaliza nombres de columnas"""
        print("🧹 Limpiando nombres de columnas...")
        
        columnas_nuevas = []
        for col in self.df.columns:
            # Convertir a minúsculas, reemplazar espacios y caracteres especiales
            nuevo = col.lower().strip()
            nuevo = re.sub(r'[^a-z0-9]+', '_', nuevo)
            nuevo = nuevo.strip('_')
            columnas_nuevas.append(nuevo)
        
        self.df.columns = columnas_nuevas
        self.reporte['cambios'].append("Nombres de columnas normalizados")
        print("✅ Columnas renombradas\n")
    
    def eliminar_duplicados(self):
        """Elimina filas duplicadas"""
        duplicados = self.df.duplicated().sum()
        
        if duplicados > 0:
            print(f"🗑️  Eliminando {duplicados} filas duplicadas...")
            self.df = self.df.drop_duplicates()
            self.reporte['cambios'].append(f"Eliminadas {duplicados} filas duplicadas")
            print("✅ Duplicados eliminados\n")
        else:
            print("✅ No hay duplicados\n")
    
    def manejar_nulos(self, estrategia='eliminar'):
        """Maneja valores nulos"""
        nulos_totales = self.df.isna().sum().sum()
        
        if nulos_totales > 0:
            print(f"🔧 Manejando {nulos_totales} valores nulos...")
            
            if estrategia == 'eliminar':
                antes = len(self.df)
                self.df = self.df.dropna()
                eliminadas = antes - len(self.df)
                print(f"✅ Eliminadas {eliminadas} filas con nulos\n")
                self.reporte['cambios'].append(f"Eliminadas {eliminadas} filas con nulos")
            
            elif estrategia == 'rellenar':
                # Rellenar numéricos con mediana, texto con "Desconocido"
                for col in self.df.columns:
                    if self.df[col].dtype in ['int64', 'float64']:
                        self.df[col].fillna(self.df[col].median(), inplace=True)
                    else:
                        self.df[col].fillna("Desconocido", inplace=True)
                print("✅ Nulos rellenados\n")
                self.reporte['cambios'].append("Nulos rellenados con valores por defecto")
        else:
            print("✅ No hay valores nulos\n")
    
    def detectar_y_limpiar_tipos(self):
        """Detecta y limpia tipos de datos comunes"""
        print("🔧 Detectando tipos de datos...\n")
        
        for col in self.df.columns:
            muestra = self.df[col].dropna().astype(str).head(10)
            
            # Detectar fechas
            if any(re.match(r'\d{4}-\d{2}-\d{2}', str(val)) for val in muestra):
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    print(f"  📅 {col} → Convertido a fecha")
                    self.reporte['cambios'].append(f"{col} convertido a fecha")
                except:
                    pass
            
            # Detectar precios/monedas
            elif any(re.search(r'[$€£]', str(val)) for val in muestra):
                try:
                    self.df[col] = self.df[col].str.replace(r'[$€£,]', '', regex=True).astype(float)
                    print(f"  💰 {col} → Limpiado como precio")
                    self.reporte['cambios'].append(f"{col} limpiado como precio")
                except:
                    pass
            
            # Detectar porcentajes
            elif any('%' in str(val) for val in muestra):
                try:
                    self.df[col] = self.df[col].str.replace('%', '').astype(float) / 100
                    print(f"  📊 {col} → Convertido a decimal")
                    self.reporte['cambios'].append(f"{col} convertido a decimal")
                except:
                    pass
        
        print()
    
    def generar_estadisticas(self):
        """Genera estadísticas descriptivas"""
        print("="*70)
        print("📊 ESTADÍSTICAS DESCRIPTIVAS")
        print("="*70)
        print()
        
        # Columnas numéricas
        numericas = self.df.select_dtypes(include=[np.number]).columns
        if len(numericas) > 0:
            print("Columnas numéricas:")
            print(self.df[numericas].describe().round(2))
            print()
        
        # Columnas categóricas (mostrar top 5 valores)
        categoricas = self.df.select_dtypes(include=['object']).columns
        if len(categoricas) > 0:
            print("\nColumnas categóricas (Top 5 valores):")
            for col in categoricas:
                print(f"\n  {col}:")
                top5 = self.df[col].value_counts().head(5)
                for valor, cantidad in top5.items():
                    print(f"    - {valor}: {cantidad}")
        
        print()
    
    def guardar_limpio(self, sufijo='_limpio'):
        """Guarda el CSV limpio"""
        archivo_salida = Path(self.archivo).stem + sufijo + '.csv'
        self.df.to_csv(archivo_salida, index=False, encoding='utf-8')
        
        print(f"💾 Archivo limpio guardado: {archivo_salida}")
        
        # Guardar reporte
        reporte_file = Path(self.archivo).stem + '_reporte.txt'
        with open(reporte_file, 'w', encoding='utf-8') as f:
            f.write(f"REPORTE DE LIMPIEZA - {self.reporte['timestamp']}\n")
            f.write("="*70 + "\n\n")
            f.write(f"Archivo original: {self.reporte['archivo']}\n")
            f.write(f"Filas originales: {self.reporte['filas_originales']}\n")
            f.write(f"Columnas originales: {self.reporte['columnas_originales']}\n")
            f.write(f"Filas finales: {len(self.df)}\n")
            f.write(f"Columnas finales: {len(self.df.columns)}\n\n")
            f.write("CAMBIOS REALIZADOS:\n")
            for cambio in self.reporte['cambios']:
                f.write(f"  • {cambio}\n")
        
        print(f"📄 Reporte guardado: {reporte_file}\n")
        
        return archivo_salida
    
    def pipeline_completo(self, manejar_nulos='eliminar'):
        """Ejecuta todo el proceso de limpieza"""
        if not self.cargar():
            return False
        
        self.analizar_inicial()
        self.limpiar_nombres_columnas()
        self.eliminar_duplicados()
        self.detectar_y_limpiar_tipos()
        self.manejar_nulos(estrategia=manejar_nulos)
        self.generar_estadisticas()
        
        archivo_limpio = self.guardar_limpio()
        
        print("="*70)
        print("✅ PROCESO COMPLETADO")
        print("="*70)
        print(f"\nReducción de datos: {self.reporte['filas_originales']} → {len(self.df)} filas")
        print(f"Archivo limpio: {archivo_limpio}\n")
        
        return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🧹 Limpiador universal de CSVs',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'archivo',
        type=str,
        help='Archivo CSV a limpiar'
    )
    
    parser.add_argument(
        '--nulos',
        choices=['eliminar', 'rellenar'],
        default='eliminar',
        help='Estrategia para valores nulos'
    )
    
    args = parser.parse_args()
    
    if not Path(args.archivo).exists():
        print(f"\n❌ Error: El archivo '{args.archivo}' no existe\n")
        return
    
    limpiador = LimpiadorCSV(args.archivo)
    limpiador.pipeline_completo(manejar_nulos=args.nulos)


if __name__ == "__main__":
    main()