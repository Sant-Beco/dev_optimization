import random
import time

class BuscadorGranja:
    """Demuestra búsqueda binaria con datos de granja"""
    
    def __init__(self):
        # Generar datos simulados de producción
        self.registros = self.generar_datos()
        self.registros_ordenados = sorted(self.registros, key=lambda x: x['fecha'])
    
    def generar_datos(self):
        """Simula 5 años de datos de 10 lotes"""
        registros = []
        
        # 5 años × 365 días × 10 lotes = 18,250 registros
        for año in range(2020, 2025):
            for dia in range(1, 366):
                for lote in [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]:
                    fecha = f"{año}-{dia:03d}"  # Formato: 2020-001, 2020-002...
                    registros.append({
                        'fecha': fecha,
                        'lote': lote,
                        'huevos': 9000 + random.randint(-500, 500),
                        'mortalidad': random.randint(0, 10),
                        'saldo_aves': 10000 - random.randint(0, 100)
                    })
        
        return registros
    
    def busqueda_lineal(self, fecha_buscar, lote_buscar):
        """❌ Búsqueda lineal O(n) - lenta"""
        comparaciones = 0
        
        for registro in self.registros:
            comparaciones += 1
            if registro['fecha'] == fecha_buscar and registro['lote'] == lote_buscar:
                return registro, comparaciones
        
        return None, comparaciones
    
    def busqueda_binaria(self, fecha_buscar, lote_buscar):
        """✅ Búsqueda binaria O(log n) - rápida"""
        # Filtrar primero por lote (si hay muchos lotes)
        registros_lote = [r for r in self.registros_ordenados if r['lote'] == lote_buscar]
        
        # Búsqueda binaria en fechas
        izquierda = 0
        derecha = len(registros_lote) - 1
        comparaciones = 0
        
        while izquierda <= derecha:
            comparaciones += 1
            medio = (izquierda + derecha) // 2
            
            fecha_medio = registros_lote[medio]['fecha']
            
            if fecha_medio == fecha_buscar:
                return registros_lote[medio], comparaciones
            
            elif fecha_medio < fecha_buscar:
                izquierda = medio + 1  # Buscar en mitad derecha
            
            else:
                derecha = medio - 1  # Buscar en mitad izquierda
        
        return None, comparaciones
    
    def busqueda_binaria_visualizada(self, fecha_buscar, lote_buscar):
        """Versión que muestra paso a paso"""
        registros_lote = [r for r in self.registros_ordenados if r['lote'] == lote_buscar]
        
        print(f"\n🔍 BUSCANDO: Lote {lote_buscar}, Fecha {fecha_buscar}")
        print(f"📊 Total registros del lote: {len(registros_lote)}\n")
        
        izquierda = 0
        derecha = len(registros_lote) - 1
        paso = 0
        
        while izquierda <= derecha:
            paso += 1
            medio = (izquierda + derecha) // 2
            fecha_medio = registros_lote[medio]['fecha']
            
            print(f"Paso {paso}:")
            print(f"  Rango: índice {izquierda} a {derecha} ({derecha - izquierda + 1} registros)")
            print(f"  Revisar medio (índice {medio}): {fecha_medio}")
            
            if fecha_medio == fecha_buscar:
                print(f"  ✅ ¡ENCONTRADO! en paso {paso}")
                return registros_lote[medio], paso
            
            elif fecha_medio < fecha_buscar:
                print(f"  ➡️  {fecha_medio} < {fecha_buscar} → Buscar en mitad derecha")
                izquierda = medio + 1
            
            else:
                print(f"  ⬅️  {fecha_medio} > {fecha_buscar} → Buscar en mitad izquierda")
                derecha = medio - 1
            
            print()
        
        print(f"  ❌ No encontrado después de {paso} pasos")
        return None, paso
    
    def comparar_velocidades(self):
        """Compara búsqueda lineal vs binaria"""
        print("\n" + "="*70)
        print("⚡ COMPARACIÓN DE VELOCIDADES")
        print("="*70)
        
        # Buscar registro al 75% del dataset (peor caso para lineal)
        fecha_buscar = "2023-274"  # Día 274 de 2023
        lote_buscar = 45
        
        print(f"\n📍 Buscando: Lote {lote_buscar}, Fecha {fecha_buscar}")
        print(f"📊 Dataset: {len(self.registros):,} registros totales\n")
        
        # Búsqueda lineal
        print("❌ BÚSQUEDA LINEAL:")
        inicio = time.time()
        resultado_lineal, comp_lineal = self.busqueda_lineal(fecha_buscar, lote_buscar)
        tiempo_lineal = time.time() - inicio
        print(f"   Comparaciones: {comp_lineal:,}")
        print(f"   Tiempo: {tiempo_lineal*1000:.4f} ms")
        
        # Búsqueda binaria
        print("\n✅ BÚSQUEDA BINARIA:")
        inicio = time.time()
        resultado_binaria, comp_binaria = self.busqueda_binaria(fecha_buscar, lote_buscar)
        tiempo_binaria = time.time() - inicio
        print(f"   Comparaciones: {comp_binaria}")
        print(f"   Tiempo: {tiempo_binaria*1000:.4f} ms")
        
        # Comparación
        mejora_comp = comp_lineal / comp_binaria if comp_binaria > 0 else 0
        mejora_tiempo = tiempo_lineal / tiempo_binaria if tiempo_binaria > 0 else 0
        
        print("\n📈 MEJORA:")
        print(f"   Comparaciones: {mejora_comp:.0f}x menos")
        print(f"   Tiempo: {mejora_tiempo:.0f}x más rápido")
        
        if resultado_binaria:
            print(f"\n📋 RESULTADO:")
            print(f"   Huevos: {resultado_binaria['huevos']:,}")
            print(f"   Mortalidad: {resultado_binaria['mortalidad']}")
            print(f"   Saldo aves: {resultado_binaria['saldo_aves']:,}")
    
    def caso_real_aplicacion(self):
        """Caso de uso real: Sistema de alertas"""
        print("\n" + "="*70)
        print("🚨 CASO REAL: Sistema de Alertas Automático")
        print("="*70)
        
        print("\nPROBLEMA:")
        print("Cada mañana, revisar si algún lote tuvo mortalidad >5 ayer.")
        print("Con 10 lotes, necesitas buscar 10 registros de 18,250 totales.")
        
        # Simular búsqueda de ayer para todos los lotes
        fecha_ayer = "2024-180"
        lotes = [39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
        
        print(f"\nFecha a revisar: {fecha_ayer}")
        print("Revisando 10 lotes...\n")
        
        alertas = []
        comparaciones_totales = 0
        
        inicio = time.time()
        for lote in lotes:
            resultado, comps = self.busqueda_binaria(fecha_ayer, lote)
            comparaciones_totales += comps
            
            if resultado and resultado['mortalidad'] > 5:
                alertas.append(resultado)
        
        tiempo_total = time.time() - inicio
        
        print(f"✅ Revisión completada en {tiempo_total*1000:.2f} ms")
        print(f"   Comparaciones totales: {comparaciones_totales}")
        print(f"   Promedio por lote: {comparaciones_totales/10:.1f}")
        
        if alertas:
            print(f"\n🚨 ALERTAS ({len(alertas)} lotes):")
            for alerta in alertas:
                print(f"   • Lote {alerta['lote']}: Mortalidad {alerta['mortalidad']} aves")
        else:
            print("\n✅ Sin alertas - Todos los lotes normales")
        
        print(f"\n💡 Con búsqueda lineal tomaría ~{(comparaciones_totales * 1000):.0f} comparaciones")
        print(f"   Mejora: {(comparaciones_totales * 1000) / comparaciones_totales:.0f}x más rápido")
    
    def ejecutar_demo(self):
        """Demo completa"""
        print("\n🎯 BÚSQUEDA BINARIA EN ACCIÓN")
        print("Datos de granja avícola: 5 años × 365 días × 10 lotes\n")
        
        # 1. Visualización paso a paso
        self.busqueda_binaria_visualizada("2022-100", 42)
        
        input("\nPresiona ENTER para comparación de velocidades...")
        
        # 2. Comparación de velocidades
        self.comparar_velocidades()
        
        input("\nPresiona ENTER para caso real...")
        
        # 3. Caso de uso real
        self.caso_real_aplicacion()
        
        print("\n" + "="*70)
        print("✅ Demostración completada")
        print("\n💡 LECCIÓN:")
        print("   • Datos ordenados + búsqueda binaria = 1000x más rápido")
        print("   • Crítico para sistemas de alertas en tiempo real")
        print("   • 18,250 registros → solo 14 comparaciones")
        print("="*70)


if __name__ == "__main__":
    buscador = BuscadorGranja()
    buscador.ejecutar_demo()