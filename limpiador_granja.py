import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import re

class LimpiadorGranja:
    """Limpiador especializado para CSVs de granja avícola"""
    
    def __init__(self, archivo_csv):
        self.archivo = archivo_csv
        self.df = None
        self.reporte = {
            'archivo': archivo_csv,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'problemas_encontrados': [],
            'correcciones_aplicadas': []
        }
    
    def detectar_estructura(self):
        """Analiza la estructura del CSV antes de procesarlo"""
        print(f"\n🔍 ANALIZANDO ESTRUCTURA: {Path(self.archivo).name}\n")
        
        # Leer primeras líneas raw
        with open(self.archivo, 'r', encoding='utf-8') as f:
            primeras_lineas = [f.readline() for _ in range(10)]
        
        # Detectar delimitador
        delimitadores = [';', ',', '\t', '|']
        conteos = {d: sum(line.count(d) for line in primeras_lineas) for d in delimitadores}
        delimitador_real = max(conteos, key=conteos.get)
        
        print(f"✅ Delimitador detectado: '{delimitador_real}'")
        print(f"   (encontrado {conteos[delimitador_real]} veces en 10 líneas)\n")
        
        # Mostrar estructura
        print("📋 Primeras 5 líneas:")
        for i, linea in enumerate(primeras_lineas[:5], 1):
            preview = linea[:100] + "..." if len(linea) > 100 else linea
            print(f"   {i}. {preview.strip()}")
        
        print()
        return delimitador_real
    
    def cargar_inteligente(self):
        """Carga el CSV detectando automáticamente la estructura"""
        delimitador = self.detectar_estructura()
        
        # Intentar diferentes configuraciones
        configs = [
            {'sep': delimitador, 'skiprows': 0},
            {'sep': delimitador, 'skiprows': 1},
            {'sep': delimitador, 'skiprows': 2},
            {'sep': delimitador, 'skiprows': 3},
            {'sep': delimitador, 'skiprows': 4},
        ]
        
        print("🔧 Probando diferentes configuraciones de carga...\n")
        
        for i, config in enumerate(configs, 1):
            try:
                df_test = pd.read_csv(self.archivo, **config, encoding='utf-8')
                
                # Verificar si tiene sentido
                if len(df_test.columns) > 1 and len(df_test) > 0:
                    print(f"✅ Configuración {i} FUNCIONA:")
                    print(f"   - Columnas: {len(df_test.columns)}")
                    print(f"   - Filas: {len(df_test)}")
                    print(f"   - Skiprows: {config['skiprows']}")
                    print(f"   - Columnas: {list(df_test.columns[:5])}")
                    
                    respuesta = input("\n¿Usar esta configuración? (s/n): ").lower()
                    if respuesta == 's':
                        self.df = df_test
                        self.reporte['correcciones_aplicadas'].append(
                            f"Cargado con sep='{delimitador}', skiprows={config['skiprows']}"
                        )
                        return True
                    print()
            
            except Exception as e:
                print(f"❌ Configuración {i} falló: {str(e)[:50]}...")
        
        print("\n⚠️  No se encontró configuración automática óptima")
        print("📝 Recomendación: Revisar el archivo manualmente\n")
        return False
    
    def limpiar_columnas(self):
        """Limpia y normaliza nombres de columnas"""
        print("🧹 Limpiando nombres de columnas...\n")
        
        columnas_originales = self.df.columns.tolist()
        columnas_nuevas = []
        
        for col in columnas_originales:
            # Convertir a string y limpiar
            col_str = str(col).strip().upper()
            
            # Remover caracteres especiales excepto espacios
            col_limpio = re.sub(r'[^A-Z0-9\s]', '', col_str)
            
            # Reemplazar espacios múltiples
            col_limpio = re.sub(r'\s+', '_', col_limpio)
            
            # Si queda vacío, usar índice
            if not col_limpio or col_limpio == 'UNNAMED':
                col_limpio = f"COLUMNA_{len(columnas_nuevas) + 1}"
            
            columnas_nuevas.append(col_limpio)
        
        self.df.columns = columnas_nuevas
        
        print("✅ Columnas renombradas:")
        for orig, nuevo in zip(columnas_originales[:10], columnas_nuevas[:10]):
            print(f"   {orig[:40]:40} → {nuevo}")
        
        if len(columnas_originales) > 10:
            print(f"   ... y {len(columnas_originales) - 10} más")
        
        print()
        self.reporte['correcciones_aplicadas'].append(
            f"Columnas normalizadas: {len(columnas_nuevas)} columnas"
        )
    
    def analizar_calidad(self):
        """Análisis de calidad de datos"""
        print("="*70)
        print("📊 ANÁLISIS DE CALIDAD DE DATOS")
        print("="*70)
        print()
        
        # Información general
        print(f"📏 Dimensiones: {len(self.df)} filas × {len(self.df.columns)} columnas\n")
        
        # Análisis por columna
        problemas = []
        
        for col in self.df.columns:
            nulos = self.df[col].isna().sum()
            nulos_pct = (nulos / len(self.df)) * 100
            unicos = self.df[col].nunique()
            
            print(f"  {col[:30]:30} | Nulos: {nulos:4} ({nulos_pct:5.1f}%) | Únicos: {unicos:4}")
            
            # Detectar problemas
            if nulos_pct > 50:
                problemas.append(f"{col}: {nulos_pct:.1f}% nulos (columna casi vacía)")
            
            if unicos == 1:
                problemas.append(f"{col}: Solo 1 valor único (columna inútil)")
        
        print()
        
        if problemas:
            print("⚠️  PROBLEMAS DETECTADOS:")
            for problema in problemas:
                print(f"   • {problema}")
            print()
            self.reporte['problemas_encontrados'].extend(problemas)
    
    def limpiar_duplicados_inteligente(self):
        """Elimina duplicados considerando toda la fila"""
        print("🗑️  Buscando filas duplicadas...\n")
        
        duplicados = self.df.duplicated().sum()
        
        if duplicados > 0:
            print(f"⚠️  Encontradas {duplicados} filas completamente duplicadas")
            print(f"   Porcentaje: {(duplicados/len(self.df)*100):.1f}%\n")
            
            # Mostrar ejemplo
            if duplicados > 0:
                ejemplo = self.df[self.df.duplicated(keep=False)].head(2)
                print("   Ejemplo de duplicado:")
                print(ejemplo.to_string(index=False)[:200])
                print()
            
            self.df = self.df.drop_duplicates()
            print(f"✅ Eliminados {duplicados} duplicados\n")
            self.reporte['correcciones_aplicadas'].append(f"Eliminados {duplicados} duplicados")
        else:
            print("✅ No hay duplicados\n")
    
    def detectar_columnas_inutiles(self):
        """Detecta y elimina columnas sin información útil"""
        print("🔍 Detectando columnas inútiles...\n")
        
        columnas_eliminar = []
        
        for col in self.df.columns:
            # Columna vacía o casi vacía
            nulos_pct = (self.df[col].isna().sum() / len(self.df)) * 100
            if nulos_pct > 95:
                columnas_eliminar.append((col, f"95%+ nulos"))
                continue
            
            # Columna con un solo valor
            if self.df[col].nunique() == 1:
                columnas_eliminar.append((col, "1 valor único"))
                continue
            
            # Columna de solo espacios/vacíos
            if self.df[col].dtype == 'object':
                no_vacios = self.df[col].dropna().str.strip()
                if len(no_vacios) == 0 or (no_vacios == '').all():
                    columnas_eliminar.append((col, "solo espacios"))
        
        if columnas_eliminar:
            print(f"⚠️  Encontradas {len(columnas_eliminar)} columnas inútiles:")
            for col, razon in columnas_eliminar:
                print(f"   • {col[:40]:40} → {razon}")
            
            respuesta = input("\n¿Eliminar estas columnas? (s/n): ").lower()
            if respuesta == 's':
                cols_a_eliminar = [col for col, _ in columnas_eliminar]
                self.df = self.df.drop(columns=cols_a_eliminar)
                print(f"\n✅ Eliminadas {len(cols_a_eliminar)} columnas\n")
                self.reporte['correcciones_aplicadas'].append(
                    f"Eliminadas {len(cols_a_eliminar)} columnas inútiles"
                )
            else:
                print("\n⏭️  Columnas conservadas\n")
        else:
            print("✅ Todas las columnas tienen datos útiles\n")
    
    def guardar_limpio(self):
        """Guarda el archivo limpio"""
        nombre_base = Path(self.archivo).stem
        archivo_salida = f"{nombre_base}_LIMPIO.csv"
        
        self.df.to_csv(archivo_salida, index=False, encoding='utf-8', sep=';')
        
        print(f"💾 Archivo limpio guardado: {archivo_salida}")
        print(f"   Reducción: {self.reporte.get('filas_originales', 0)} → {len(self.df)} filas")
        print(f"   Columnas: {self.reporte.get('columnas_originales', 0)} → {len(self.df.columns)}\n")
        
        # Guardar reporte
        reporte_file = f"{nombre_base}_REPORTE.txt"
        with open(reporte_file, 'w', encoding='utf-8') as f:
            f.write(f"REPORTE DE LIMPIEZA - {self.reporte['timestamp']}\n")
            f.write("="*70 + "\n\n")
            f.write(f"Archivo: {self.archivo}\n\n")
            
            if self.reporte['problemas_encontrados']:
                f.write("PROBLEMAS ENCONTRADOS:\n")
                for p in self.reporte['problemas_encontrados']:
                    f.write(f"  • {p}\n")
                f.write("\n")
            
            f.write("CORRECCIONES APLICADAS:\n")
            for c in self.reporte['correcciones_aplicadas']:
                f.write(f"  • {c}\n")
        
        print(f"📄 Reporte guardado: {reporte_file}\n")
        
        return archivo_salida
    
    def pipeline_granja(self):
        """Pipeline completo para CSVs de granja"""
        print("\n🐔 LIMPIADOR ESPECIALIZADO PARA GRANJA AVÍCOLA")
        print("="*70)
        
        # Guardar estado original
        if not self.cargar_inteligente():
            return False
        
        self.reporte['filas_originales'] = len(self.df)
        self.reporte['columnas_originales'] = len(self.df.columns)
        
        self.limpiar_columnas()
        self.analizar_calidad()
        self.limpiar_duplicados_inteligente()
        self.detectar_columnas_inutiles()
        
        archivo_limpio = self.guardar_limpio()
        
        print("="*70)
        print("✅ LIMPIEZA COMPLETADA")
        print("="*70)
        print(f"\nArchivo listo para análisis: {archivo_limpio}\n")
        
        return True


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("\nUso: python limpiador_granja.py <archivo.csv>\n")
        return
    
    archivo = sys.argv[1]
    
    if not Path(archivo).exists():
        print(f"\n❌ Error: '{archivo}' no existe\n")
        return
    
    limpiador = LimpiadorGranja(archivo)
    limpiador.pipeline_granja()


if __name__ == "__main__":
    main()