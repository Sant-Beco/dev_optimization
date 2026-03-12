import time
import pandas as pd

class MedidorPerformance:
    """Mide y compara velocidad de diferentes implementaciones"""
    
    def generar_datos_prueba(self, n_archivos):
        """Simula lista de archivos de granja"""
        extensiones = ['.pdf', '.xlsx', '.csv', '.txt', '.docx']
        archivos = []
        
        for i in range(n_archivos):
            lote = i % 100
            fecha = f"2024-01-{(i % 30) + 1:02d}"
            ext = extensiones[i % len(extensiones)]
            archivos.append(f"LOTE_{lote}_{fecha}_produccion{ext}")
        
        return archivos
    
    def metodo_lento_nested_loops(self, archivos):
        """❌ O(n²) - Loops anidados"""
        extensiones = ['.pdf', '.xlsx', '.csv', '.txt', '.docx']
        categorias = {
            '.pdf': 'Reportes',
            '.xlsx': 'Datos',
            '.csv': 'Datos',
            '.txt': 'Notas',
            '.docx': 'Documentos'
        }
        
        resultados = []
        for archivo in archivos:
            for ext in extensiones:
                if archivo.endswith(ext):
                    resultados.append((archivo, categorias[ext]))
                    break
        
        return resultados
    
    def metodo_rapido_dict_lookup(self, archivos):
        """✅ O(n) - Búsqueda en diccionario"""
        categorias = {
            '.pdf': 'Reportes',
            '.xlsx': 'Datos',
            '.csv': 'Datos',
            '.txt': 'Notas',
            '.docx': 'Documentos'
        }
        
        resultados = []
        for archivo in archivos:
            ext = '.' + archivo.split('.')[-1]
            categoria = categorias.get(ext, 'Otros')
            resultados.append((archivo, categoria))
        
        return resultados
    
    def comparar_metodos(self):
        """Compara velocidades en diferentes tamaños"""
        print("\n🔬 COMPARACIÓN DE PERFORMANCE")
        print("="*70)
        print(f"{'N Archivos':>12} | {'Lento O(n²)':>15} | {'Rápido O(n)':>15} | {'Mejora':>10}")
        print("-"*70)
        
        tamaños = [100, 500, 1000, 5000]
        
        for n in tamaños:
            archivos = self.generar_datos_prueba(n)
            
            # Medir método lento
            inicio = time.time()
            self.metodo_lento_nested_loops(archivos)
            tiempo_lento = time.time() - inicio
            
            # Medir método rápido
            inicio = time.time()
            self.metodo_rapido_dict_lookup(archivos)
            tiempo_rapido = time.time() - inicio
            
            mejora = tiempo_lento / tiempo_rapido if tiempo_rapido > 0 else 0
            
            print(f"{n:>12} | {tiempo_lento:>13.4f}s | {tiempo_rapido:>13.4f}s | {mejora:>8.1f}x")
        
        print()
    
    def analizar_tu_codigo(self):
        """Analiza el código real de tu granja"""
        print("\n📊 ANÁLISIS DE TU CÓDIGO REAL")
        print("="*70)
        
        # Simular tu caso: 5 años de datos
        n_filas = 5 * 365 * 10  # 5 años × 365 días × 10 lotes
        
        print(f"\nDatos de producción: {n_filas:,} filas")
        print(f"Columnas: FECHA, LOTE, HUEVOS, MORTALIDAD, etc.\n")
        
        # Estimar tiempos
        print("OPERACIÓN: Filtrar por lote")
        print(f"  O(n) - df[df['LOTE'] == 39]     → ~{n_filas * 0.00001:.2f}s  ✅")
        print(f"  O(n²) - nested loops            → ~{n_filas * n_filas * 0.000001:.1f}s  ❌")
        
        print("\nOPERACIÓN: Agrupar por fecha")
        print(f"  O(n log n) - df.groupby()       → ~{n_filas * 0.00002:.2f}s  ✅")
        
        print("\nRECOMENDACIÓN:")
        print("  • Usa pandas .loc[], .groupby(), .merge() (optimizados)")
        print("  • Evita loops en Python puro sobre DataFrames")
        print("  • 1 línea de pandas > 100 líneas de loops")
        print()


if __name__ == "__main__":
    medidor = MedidorPerformance()
    
    print("\n⚡ MEDIDOR DE PERFORMANCE - Big O en Acción")
    print("Procesando archivos de granja avícola...\n")
    
    medidor.comparar_metodos()
    medidor.analizar_tu_codigo()
    
    print("="*70)
    print("💡 LECCIÓN: Usa estructuras de datos correctas")
    print("   Diccionarios para búsquedas = O(1)")
    print("   Pandas para datos tabulares = Optimizado en C")
    print("="*70)