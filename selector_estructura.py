import time
from collections import defaultdict

class SelectorEstructura:
    """Demuestra cuándo usar cada estructura de datos"""
    
    def __init__(self):
        # Datos simulados de granja
        self.datos_produccion = self.generar_datos()
    
    def generar_datos(self):
        """Simula 30 días × 5 lotes"""
        datos = []
        for dia in range(1, 31):
            for lote in [39, 40, 41, 42, 43]:
                datos.append({
                    'dia': dia,
                    'lote': lote,
                    'huevos': 9000 + (lote * 100) + (dia * 10),
                    'mortalidad': (dia % 7)
                })
        return datos
    
    def caso_1_lista_vs_dict(self):
        """Caso 1: Buscar producción de un lote específico"""
        print("\n" + "="*70)
        print("CASO 1: Buscar producción del Lote 39")
        print("="*70)
        
        # ❌ OPCIÓN A: Lista (O(n))
        print("\n❌ Con LISTA (buscar linealmente):")
        
        produccion_lista = []
        for registro in self.datos_produccion:
            produccion_lista.append((registro['lote'], registro['huevos']))
        
        inicio = time.time()
        resultados = []
        for lote, huevos in produccion_lista:
            if lote == 39:
                resultados.append(huevos)
        tiempo_lista = time.time() - inicio
        
        print(f"   Tiempo: {tiempo_lista:.6f}s")
        print(f"   Operaciones: {len(produccion_lista)} comparaciones")
        
        # ✅ OPCIÓN B: Diccionario (O(1))
        print("\n✅ Con DICCIONARIO (lookup directo):")
        
        produccion_dict = defaultdict(list)
        for registro in self.datos_produccion:
            produccion_dict[registro['lote']].append(registro['huevos'])
        
        inicio = time.time()
        resultados = produccion_dict[39]
        tiempo_dict = time.time() - inicio
        
        print(f"   Tiempo: {tiempo_dict:.6f}s")
        print(f"   Operaciones: 1 lookup")
        
        mejora = tiempo_lista / tiempo_dict if tiempo_dict > 0 else float('inf')
        print(f"\n   🚀 Mejora: {mejora:.0f}x más rápido")
        print(f"   Conclusión: Para búsquedas por clave → DICCIONARIO")
    
    def caso_2_duplicados(self):
        """Caso 2: Encontrar lotes únicos con alertas"""
        print("\n" + "="*70)
        print("CASO 2: Lotes únicos con mortalidad >3")
        print("="*70)
        
        # ❌ OPCIÓN A: Lista con verificación manual
        print("\n❌ Con LISTA:")
        
        inicio = time.time()
        lotes_alerta_lista = []
        for registro in self.datos_produccion:
            if registro['mortalidad'] > 3:
                if registro['lote'] not in lotes_alerta_lista:
                    lotes_alerta_lista.append(registro['lote'])
        tiempo_lista = time.time() - inicio
        
        print(f"   Resultado: {sorted(lotes_alerta_lista)}")
        print(f"   Tiempo: {tiempo_lista:.6f}s")
        
        # ✅ OPCIÓN B: Set (elimina duplicados automáticamente)
        print("\n✅ Con SET:")
        
        inicio = time.time()
        lotes_alerta_set = set()
        for registro in self.datos_produccion:
            if registro['mortalidad'] > 3:
                lotes_alerta_set.add(registro['lote'])
        tiempo_set = time.time() - inicio
        
        print(f"   Resultado: {sorted(lotes_alerta_set)}")
        print(f"   Tiempo: {tiempo_set:.6f}s")
        
        mejora = tiempo_lista / tiempo_set if tiempo_set > 0 else float('inf')
        print(f"\n   🚀 Mejora: {mejora:.0f}x más rápido")
        print(f"   Conclusión: Para valores únicos → SET")
    
    def caso_3_operaciones_conjuntos(self):
        """Caso 3: Lotes con múltiples condiciones"""
        print("\n" + "="*70)
        print("CASO 3: Análisis de múltiples condiciones")
        print("="*70)
        
        # Lotes con diferentes alertas
        alta_produccion = set()
        alta_mortalidad = set()
        
        for registro in self.datos_produccion:
            if registro['huevos'] > 9500:
                alta_produccion.add(registro['lote'])
            if registro['mortalidad'] > 4:
                alta_mortalidad.add(registro['lote'])
        
        print(f"\n   Lotes alta producción: {sorted(alta_produccion)}")
        print(f"   Lotes alta mortalidad: {sorted(alta_mortalidad)}")
        
        # ✅ Operaciones de conjuntos
        print("\n   📊 Análisis con operaciones de conjuntos:")
        
        # Intersección: Ambas condiciones
        criticos = alta_produccion & alta_mortalidad
        print(f"   • Críticos (alta prod + mortalidad): {sorted(criticos)}")
        
        # Diferencia: Solo alta producción
        buenos = alta_produccion - alta_mortalidad
        print(f"   • Buenos (alta prod, baja mortalidad): {sorted(buenos)}")
        
        # Unión: Cualquier alerta
        vigilar = alta_produccion | alta_mortalidad
        print(f"   • Total a vigilar: {sorted(vigilar)}")
        
        print(f"\n   Conclusión: Sets para análisis de condiciones → POTENTE")
    
    def guia_decision(self):
        """Guía para elegir estructura"""
        print("\n" + "="*70)
        print("🎯 GUÍA DE DECISIÓN")
        print("="*70)
        
        decisiones = [
            ("¿Necesitas orden cronológico/secuencial?", "list", "Producción por día"),
            ("¿Buscas por ID/clave única?", "dict", "Datos por lote"),
            ("¿Necesitas eliminar duplicados?", "set", "Lotes únicos"),
            ("¿Datos que nunca cambian?", "tuple", "Coordenadas GPS"),
            ("¿Contar ocurrencias?", "dict (Counter)", "Huevos por categoría"),
        ]
        
        for pregunta, estructura, ejemplo in decisiones:
            print(f"\n   {pregunta}")
            print(f"   → Usa: {estructura}")
            print(f"   → Ejemplo: {ejemplo}")
    
    def ejecutar_todos(self):
        """Ejecuta todos los casos"""
        print("\n📊 SELECTOR DE ESTRUCTURA DE DATOS")
        print("Casos prácticos con datos de granja avícola\n")
        
        self.caso_1_lista_vs_dict()
        input("\nPresiona ENTER para Caso 2...")
        
        self.caso_2_duplicados()
        input("\nPresiona ENTER para Caso 3...")
        
        self.caso_3_operaciones_conjuntos()
        
        self.guia_decision()
        
        print("\n" + "="*70)
        print("✅ Demostración completada")
        print("="*70)


if __name__ == "__main__":
    selector = SelectorEstructura()
    selector.ejecutar_todos()