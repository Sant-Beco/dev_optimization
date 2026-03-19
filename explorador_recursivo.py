import os
from pathlib import Path

class ExploradorRecursivo:
    """Demuestra recursión con casos prácticos de granja"""
    
    def __init__(self):
        self.llamadas = []  # Para visualizar
    
    def ejemplo_1_factorial(self, n, nivel=0):
        """Factorial con visualización de llamadas"""
        indent = "  " * nivel
        self.llamadas.append(f"{indent}factorial({n})")
        
        # Caso base
        if n <= 1:
            self.llamadas.append(f"{indent}  → retorna 1")
            return 1
        
        # Caso recursivo
        resultado = n * self.ejemplo_1_factorial(n - 1, nivel + 1)
        self.llamadas.append(f"{indent}  → retorna {n} × factorial({n-1}) = {resultado}")
        
        return resultado
    
    def ejemplo_2_suma_lista(self, lista, nivel=0):
        """Suma elementos de lista recursivamente"""
        indent = "  " * nivel
        
        # Caso base: lista vacía
        if not lista:
            print(f"{indent}Lista vacía → 0")
            return 0
        
        # Caso recursivo
        print(f"{indent}suma({lista}) = {lista[0]} + suma({lista[1:]})")
        
        primer_elemento = lista[0]
        resto = self.ejemplo_2_suma_lista(lista[1:], nivel + 1)
        
        resultado = primer_elemento + resto
        print(f"{indent}  → {primer_elemento} + {resto} = {resultado}")
        
        return resultado
    
    def ejemplo_3_estructura_granja(self, carpeta, nivel=0, archivo_salida=None):
        """Visualiza estructura de carpetas recursivamente"""
        indent = "  " * nivel
        simbolo = "├─ " if nivel > 0 else ""
        
        # Obtener nombre de carpeta
        nombre = os.path.basename(carpeta) or carpeta
        
        # Imprimir y guardar
        linea = f"{indent}{simbolo}{nombre}/"
        print(linea)
        if archivo_salida:
            archivo_salida.write(linea + "\n")
        
        try:
            items = sorted(os.listdir(carpeta))
            
            for item in items:
                ruta = os.path.join(carpeta, item)
                
                if os.path.isdir(ruta):
                    # Caso recursivo: subcarpeta
                    self.ejemplo_3_estructura_granja(ruta, nivel + 1, archivo_salida)
                else:
                    # Caso base: archivo
                    linea = f"{indent}  ├─ {item}"
                    print(linea)
                    if archivo_salida:
                        archivo_salida.write(linea + "\n")
        
        except PermissionError:
            pass
    
    def ejemplo_4_buscar_csv(self, carpeta):
        """Busca todos los CSV recursivamente (caso real)"""
        archivos_csv = []
        
        try:
            for item in os.listdir(carpeta):
                ruta = os.path.join(carpeta, item)
                
                if os.path.isfile(ruta):
                    # Caso base: archivo
                    if ruta.endswith('.csv'):
                        archivos_csv.append(ruta)
                
                elif os.path.isdir(ruta):
                    # Caso recursivo: explorar subcarpeta
                    archivos_csv.extend(self.ejemplo_4_buscar_csv(ruta))
        
        except PermissionError:
            pass
        
        return archivos_csv
    
    def ejemplo_5_calcular_metricas(self, datos, nivel=0):
        """Calcula métricas anidadas (estructura tipo JSON)"""
        
        # Simular datos anidados de granja
        if nivel == 0:
            datos = {
                'lote_39': {
                    'semana_1': {'huevos': 9500, 'mortalidad': 5},
                    'semana_2': {'huevos': 9480, 'mortalidad': 3}
                },
                'lote_40': {
                    'semana_1': {'huevos': 8200, 'mortalidad': 4},
                    'semana_2': {'huevos': 8300, 'mortalidad': 2}
                }
            }
        
        total_huevos = 0
        
        for key, value in datos.items():
            if isinstance(value, dict):
                # Caso recursivo: diccionario anidado
                if 'huevos' in value:
                    # Caso base: encontramos dato
                    total_huevos += value['huevos']
                else:
                    # Seguir explorando
                    total_huevos += self.ejemplo_5_calcular_metricas(value, nivel + 1)
        
        return total_huevos
    
    def demostrar_todos(self):
        """Ejecuta todos los ejemplos"""
        print("\n🔄 RECURSIÓN: Código que se llama a sí mismo")
        print("="*70)
        
        # Ejemplo 1: Factorial
        print("\n📚 EJEMPLO 1: Factorial (clásico)")
        print("-"*70)
        self.llamadas = []
        resultado = self.ejemplo_1_factorial(5)
        print("\nLlamadas realizadas:")
        for llamada in self.llamadas:
            print(llamada)
        print(f"\nResultado final: factorial(5) = {resultado}")
        
        input("\nPresiona ENTER para siguiente ejemplo...")
        
        # Ejemplo 2: Suma lista
        print("\n📚 EJEMPLO 2: Sumar lista recursivamente")
        print("-"*70)
        produccion = [9500, 9480, 9520, 9495]
        print(f"Lista: {produccion}\n")
        total = self.ejemplo_2_suma_lista(produccion)
        print(f"\nTotal: {total} huevos")
        
        input("\nPresiona ENTER para siguiente ejemplo...")
        
        # Ejemplo 3: Estructura de carpetas
        print("\n📚 EJEMPLO 3: Explorar carpetas (caso real)")
        print("-"*70)
        print("Estructura actual:")
        carpeta_actual = os.getcwd()
        
        with open('estructura_carpetas.txt', 'w', encoding='utf-8') as f:
            self.ejemplo_3_estructura_granja(carpeta_actual, archivo_salida=f)
        
        print("\n💾 Guardado en: estructura_carpetas.txt")
        
        # Ejemplo 4: Buscar CSVs
        print("\n📚 EJEMPLO 4: Buscar todos los CSV")
        print("-"*70)
        csvs = self.ejemplo_4_buscar_csv(carpeta_actual)
        print(f"CSVs encontrados: {len(csvs)}")
        for csv in csvs[:5]:  # Mostrar primeros 5
            print(f"  • {os.path.basename(csv)}")
        if len(csvs) > 5:
            print(f"  ... y {len(csvs) - 5} más")
        
        print("\n" + "="*70)
        print("✅ Demostración completada")
        print("\n💡 LECCIÓN: Recursión simplifica problemas anidados")
        print("   Carpetas, árboles, JSON → Recursión natural")
        print("="*70)


if __name__ == "__main__":
    explorador = ExploradorRecursivo()
    explorador.demostrar_todos()