import sys
from datetime import datetime

class VisualizadorMemoria:
    """
    Demuestra visualmente cómo Python maneja referencias y copias.
    Útil para entender bugs en procesamiento de DataFrames.
    """
    
    def __init__(self):
        self.log = []
    
    def mostrar_id(self, nombre, objeto):
        """Muestra la dirección de memoria de un objeto"""
        direccion = id(objeto)
        tamaño = sys.getsizeof(objeto)
        tipo = type(objeto).__name__
        
        print(f"  {nombre:15} | ID: {direccion:18} | Tipo: {tipo:10} | Tamaño: {tamaño:6} bytes")
        
        self.log.append({
            'nombre': nombre,
            'id': direccion,
            'tipo': tipo,
            'tamaño': tamaño,
            'valor': str(objeto)[:50]
        })
        
        return direccion
    
    def ejemplo_1_referencias(self):
        """Ejemplo 1: Referencias vs Copias en listas"""
        print("\n" + "="*70)
        print("📝 EJEMPLO 1: Referencias en Listas (el problema común)")
        print("="*70)
        
        print("\n🔹 Paso 1: Crear lista original")
        print("   Código: produccion_dia1 = [100, 95, 102]")
        produccion_dia1 = [100, 95, 102]
        id1 = self.mostrar_id('produccion_dia1', produccion_dia1)
        
        print("\n🔹 Paso 2: Asignar a otra variable (¿crea copia?)")
        print("   Código: produccion_backup = produccion_dia1")
        produccion_backup = produccion_dia1
        id2 = self.mostrar_id('produccion_backup', produccion_backup)
        
        if id1 == id2:
            print("\n   ⚠️  MISMO ID → ¡SON LA MISMA LISTA EN MEMORIA!")
        
        print("\n🔹 Paso 3: Modificar 'backup'")
        print("   Código: produccion_backup.append(98)")
        produccion_backup.append(98)
        
        print("\n   Resultado:")
        print(f"   produccion_dia1   = {produccion_dia1}")
        print(f"   produccion_backup = {produccion_backup}")
        print("\n   💥 PROBLEMA: Modificar 'backup' cambió el 'original'")
        
        print("\n🔹 Paso 4: Crear COPIA REAL")
        print("   Código: produccion_copia = produccion_dia1.copy()")
        produccion_copia = produccion_dia1.copy()
        id3 = self.mostrar_id('produccion_copia', produccion_copia)
        
        if id3 != id1:
            print("\n   ✅ DIFERENTE ID → ES UNA COPIA INDEPENDIENTE")
        
        print("\n🔹 Paso 5: Modificar la copia")
        produccion_copia.append(105)
        
        print("\n   Resultado:")
        print(f"   produccion_dia1   = {produccion_dia1}")
        print(f"   produccion_copia  = {produccion_copia}")
        print("\n   ✅ ÉXITO: La copia es independiente")
    
    def ejemplo_2_diccionarios(self):
        """Ejemplo 2: Referencias en diccionarios (como tus CSVs)"""
        print("\n" + "="*70)
        print("📝 EJEMPLO 2: Diccionarios - Datos de Granja")
        print("="*70)
        
        print("\n🔹 Crear datos del lote 39")
        lote_39 = {
            'nombre': 'LOTE 39',
            'aves': 10000,
            'mortalidad': [5, 3, 4, 2],  # Lista dentro de dict
            'produccion': 9500
        }
        
        print(f"   lote_39 = {lote_39}")
        id_lote39 = self.mostrar_id('lote_39', lote_39)
        id_mortalidad = self.mostrar_id('  mortalidad', lote_39['mortalidad'])
        
        print("\n🔹 Simular 'backup' antes de análisis")
        print("   Código: lote_39_backup = lote_39")
        lote_39_backup = lote_39
        
        print("\n🔹 Modificar datos en 'backup'")
        print("   Código: lote_39_backup['mortalidad'].append(6)")
        lote_39_backup['mortalidad'].append(6)
        
        print("\n   Resultado:")
        print(f"   lote_39 mortalidad        = {lote_39['mortalidad']}")
        print(f"   lote_39_backup mortalidad = {lote_39_backup['mortalidad']}")
        print("\n   💥 PROBLEMA GRAVE: Modificaste el original sin querer")
        
        print("\n🔹 Solución: copy vs deepcopy")
        import copy
        
        lote_39_shallow = lote_39.copy()  # Copia superficial
        lote_39_deep = copy.deepcopy(lote_39)  # Copia profunda
        
        print("\n   Modificar en shallow copy:")
        lote_39_shallow['mortalidad'].append(7)
        print(f"   lote_39 mortalidad = {lote_39['mortalidad']}")
        print("   💥 Shallow copy NO copia listas internas")
        
        print("\n   Modificar en deep copy:")
        lote_39_deep['mortalidad'].append(8)
        print(f"   lote_39 mortalidad      = {lote_39['mortalidad']}")
        print(f"   lote_39_deep mortalidad = {lote_39_deep['mortalidad']}")
        print("   ✅ Deep copy SÍ es totalmente independiente")
    
    def ejemplo_3_inmutables(self):
        """Ejemplo 3: Tipos inmutables NO tienen este problema"""
        print("\n" + "="*70)
        print("📝 EJEMPLO 3: Tipos Inmutables (int, str)")
        print("="*70)
        
        print("\n🔹 Números (inmutables)")
        aves_dia1 = 10000
        aves_backup = aves_dia1
        
        id_dia1 = self.mostrar_id('aves_dia1', aves_dia1)
        id_backup = self.mostrar_id('aves_backup', aves_backup)
        
        print("\n   Modificar backup:")
        print("   Código: aves_backup = 9995")
        aves_backup = 9995
        
        id_backup_nuevo = self.mostrar_id('aves_backup', aves_backup)
        
        print(f"\n   aves_dia1   = {aves_dia1}")
        print(f"   aves_backup = {aves_backup}")
        print("\n   ✅ Los int son INMUTABLES: crear nuevo valor = nueva dirección")
    
    def caso_real_pandas(self):
        """Ejemplo 4: El caso real con pandas DataFrames"""
        print("\n" + "="*70)
        print("📝 EJEMPLO 4: TU CASO REAL - DataFrames de Pandas")
        print("="*70)
        
        print("\n⚠️  Sin pandas instalado, simulamos con diccionario:")
        
        # Simular DataFrame con dict
        df_produccion = {
            'FECHA': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'HUEVOS': [9500, 9480, 9520],
            'MORTALIDAD': [5, 3, 4]
        }
        
        print("\n🔹 DataFrame original:")
        for key in df_produccion:
            print(f"   {key}: {df_produccion[key]}")
        
        print("\n   Código PELIGROSO:")
        print("   df_analisis = df_produccion")
        df_analisis = df_produccion
        
        print("\n   Código: df_analisis['HUEVOS'][0] = 0  # Simular error")
        df_analisis['HUEVOS'][0] = 0
        
        print("\n   Resultado:")
        print(f"   df_produccion HUEVOS = {df_produccion['HUEVOS']}")
        print(f"   df_analisis HUEVOS   = {df_analisis['HUEVOS']}")
        print("\n   💥 CORROMPISTE LOS DATOS ORIGINALES")
        
        print("\n   SOLUCIÓN en pandas:")
        print("   df_analisis = df_produccion.copy()  # ✅")
        print("   O mejor aún:")
        print("   df_analisis = df_produccion.copy(deep=True)  # ✅✅")
    
    def generar_reporte(self):
        """Genera reporte en markdown"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        reporte = f"""# Reporte: Análisis de Memoria en Python

**Generado:** {timestamp}

## Conceptos Clave

### Referencias vs Copias

**Variables mutables (list, dict, DataFrame):**
- Asignación simple (`y = x`) crea **referencia** al mismo objeto
- Modificar uno afecta al otro
- **Solución:** Usar `.copy()` o `copy.deepcopy()`

**Variables inmutables (int, str, tuple):**
- Asignación crea nuevo objeto automáticamente
- No hay problema de referencias compartidas

## Objetos Analizados

| Variable | ID Memoria | Tipo | Tamaño |
|----------|------------|------|--------|
"""
        
        for item in self.log:
            reporte += f"| {item['nombre']:15} | {item['id']:18} | {item['tipo']:10} | {item['tamaño']:6} bytes |\n"
        
        reporte += f"""

## Reglas para tu Código de Granja

1. **Siempre** usar `.copy()` antes de modificar DataFrames
2. Para estructuras anidadas (listas dentro de dicts), usar `copy.deepcopy()`
3. Verificar IDs con `id(objeto)` cuando tengas dudas
4. En pandas: preferir `df.copy(deep=True)` para seguridad

## Ejemplo Real de Bug Evitado
```python
# ❌ MAL: Referencia compartida
df_lote39 = df_original
df_lote39['MORTALIDAD'] += 1  # Modifica original también

# ✅ BIEN: Copia independiente
df_lote39 = df_original.copy()
df_lote39['MORTALIDAD'] += 1  # Solo modifica la copia
```

---
*Generado por visualizador_memoria.py*
"""
        
        with open('MEMORIA_REFERENCIAS.md', 'w', encoding='utf-8') as f:
            f.write(reporte)
        
        print("\n📄 Reporte guardado: MEMORIA_REFERENCIAS.md")
    
    def ejecutar_todos(self):
        """Ejecuta todos los ejemplos"""
        print("\n🧠 VISUALIZADOR DE MEMORIA EN PYTHON")
        print("Cómo evitar bugs en procesamiento de datos de granja\n")
        
        input("Presiona ENTER para ver Ejemplo 1 (Referencias en listas)...")
        self.ejemplo_1_referencias()
        
        input("\nPresiona ENTER para ver Ejemplo 2 (Diccionarios)...")
        self.ejemplo_2_diccionarios()
        
        input("\nPresiona ENTER para ver Ejemplo 3 (Inmutables)...")
        self.ejemplo_3_inmutables()
        
        input("\nPresiona ENTER para ver Ejemplo 4 (Tu caso real)...")
        self.caso_real_pandas()
        
        print("\n" + "="*70)
        self.generar_reporte()
        print("="*70)


if __name__ == "__main__":
    visualizador = VisualizadorMemoria()
    visualizador.ejecutar_todos()
    
    print("\n✅ Ejecución completada")
    print("\n💡 Próxima vez que proceses CSVs de producción:")
    print("   SIEMPRE usa .copy() antes de modificar datos")