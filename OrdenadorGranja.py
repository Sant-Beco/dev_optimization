import random
import time

class OrdenadorGranja:
    """Demuestra ordenamiento con datos de granja"""
    
    def generar_datos_desordenados(self, n=100):
        """Simula registros desordenados"""
        registros = []
        for i in range(n):
            registros.append({
                'lote': random.choice([39, 40, 41, 42, 43]),
                'fecha': f"2024-{random.randint(1, 365):03d}",
                'huevos': random.randint(8000, 10000),
                'mortalidad': random.randint(0, 10)
            })
        return registros
    
    def demo_ordenamiento(self):
        """Demo rápida de ordenamiento"""
        print("\n🔄 ORDENAMIENTO DE REGISTROS")
        print("="*60)
        
        # Generar datos
        registros = self.generar_datos_desordenados(1000)
        
        print(f"\n📊 {len(registros)} registros desordenados")
        print("\nPrimeros 3 (desordenados):")
        for r in registros[:3]:
            print(f"  Lote {r['lote']}, {r['fecha']}, {r['huevos']} huevos")
        
        # Ordenar por fecha
        print("\n🔄 Ordenando por fecha...")
        inicio = time.time()
        registros_ordenados = sorted(registros, key=lambda x: x['fecha'])
        tiempo = time.time() - inicio
        
        print(f"✅ Ordenado en {tiempo*1000:.2f} ms")
        print("\nPrimeros 3 (ordenados por fecha):")
        for r in registros_ordenados[:3]:
            print(f"  Lote {r['lote']}, {r['fecha']}, {r['huevos']} huevos")
        
        # Ordenar por producción (descendente)
        print("\n🔄 Ordenando por producción (mayor a menor)...")
        por_produccion = sorted(registros, key=lambda x: x['huevos'], reverse=True)
        
        print("\nTop 3 lotes productores:")
        for i, r in enumerate(por_produccion[:3], 1):
            print(f"  {i}. Lote {r['lote']}, {r['fecha']}: {r['huevos']} huevos")
        
        # Ordenar por múltiples criterios
        print("\n🔄 Ordenando por lote, luego fecha...")
        por_lote_fecha = sorted(registros, key=lambda x: (x['lote'], x['fecha']))
        
        print("\nPrimeros 5 (agrupados por lote):")
        for r in por_lote_fecha[:5]:
            print(f"  Lote {r['lote']}, {r['fecha']}, {r['huevos']} huevos")
        
        print("\n" + "="*60)
        print("💡 LECCIÓN: Python sorted() es O(n log n) - muy rápido")
        print("="*60)
    
    def caso_real_ranking(self):
        """Caso real: Ranking de lotes"""
        print("\n🏆 CASO REAL: Ranking de Lotes por Producción")
        print("="*60)
        
        # Simular producción semanal por lote
        datos = self.generar_datos_desordenados(70)  # 7 días × 10 lotes
        
        # Agrupar por lote y sumar
        produccion_por_lote = {}
        for registro in datos:
            lote = registro['lote']
            if lote not in produccion_por_lote:
                produccion_por_lote[lote] = {'total': 0, 'dias': 0}
            produccion_por_lote[lote]['total'] += registro['huevos']
            produccion_por_lote[lote]['dias'] += 1
        
        # Convertir a lista y ordenar
        ranking = []
        for lote, stats in produccion_por_lote.items():
            promedio = stats['total'] / stats['dias']
            ranking.append({
                'lote': lote,
                'total': stats['total'],
                'promedio': promedio
            })
        
        # Ordenar por total descendente
        ranking_ordenado = sorted(ranking, key=lambda x: x['total'], reverse=True)
        
        print("\n🥇 RANKING SEMANAL:")
        for i, lote_stats in enumerate(ranking_ordenado, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            print(f"{emoji} {i}. Lote {lote_stats['lote']}: "
                  f"{lote_stats['total']:,} huevos "
                  f"(promedio: {lote_stats['promedio']:.0f}/día)")
        
        print()


# Ejecutar demo
ordenador = OrdenadorGranja()
ordenador.demo_ordenamiento()

print("\n" + "="*60)
ordenador.caso_real_ranking()