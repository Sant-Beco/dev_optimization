# CÓDIGO ORIGINAL (tiene 4 problemas)
def analizar_produccion(datos_brutos):
    # Problema 1: Referencia compartida
    datos = datos_brutos.copy()
    
    # Problema 2: O(n²) - loop anidado
    lotes_con_alerta = set()
    for registro in datos:
        if registro['mortalidad'] > 5:
            lotes_con_alerta.append(registro['lote'])
    
    # Problema 3: Estructura incorrecta (debería ser dict)
    stats = {}
    for registro in datos:
        if registro['lote'] in lotes_con_alerta:
            if registro['lote'] not in stats:
                stats[registro['lote']]=0
            stats[registro['lote']] += registro['huevos']
    
    return stats