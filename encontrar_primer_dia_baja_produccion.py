import random, time

def encontrar_primer_dia_baja_produccion(registros_ordenados, umbral=8500):

    if not registros_ordenados:
         return None
    

        
    # Búsqueda binaria en fechas
    izquierda = 0
    derecha = len(registros_ordenados) - 1
    comparaciones = 0
        
    while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            huevos_medio = registros_ordenados[medio]['huevos']
            
            if huevos_medio < umbral:
                resultado = registros_ordenados[medio]

                derecha = medio - 1
            
            else:
                izquierda = medio + 1  # Buscar en mitad izquierda
        
    return resultado  


# Test
registros = [
    {'fecha': '2024-001', 'huevos': 9500},
    {'fecha': '2024-002', 'huevos': 9200},
    {'fecha': '2024-003', 'huevos': 8300},  # ← Primera < 8500
    {'fecha': '2024-004', 'huevos': 8100},
]

resultado = encontrar_primer_dia_baja_produccion(registros, umbral=8500)
print(resultado)  # {'fecha': '2024-003', 'huevos': 8300}