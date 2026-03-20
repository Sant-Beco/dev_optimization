def contar_lotes(estructura):
    """
    Cuenta recursivamente todos los lotes en estructura anidada.
    
    Lógica:
    1. Contador empieza en cero
    2. Para cada elemento:
       - Si es lote → sumar 1
       - Si es carpeta → explorar recursivamente
    3. Retornar total
    """
    contador = 0
    
    for clave, valor in estructura.items():
        if clave.startswith('lote_'):
            contador += 1
        elif isinstance(valor, dict):
            contador += contar_lotes(valor)  # RECURSIÓN
    
    return contador


# Datos de prueba
granja = {
    '2024': {
        'Enero': {'lote_39': {}, 'lote_40': {}},
        'Febrero': {'lote_41': {}, 'lote_42': {}, 'lote_43': {}}
    },
    '2023': {
        'Diciembre': {'lote_38': {}}
    }
}

# Ejecutar
total = contar_lotes(granja)
print(f"✅ Total de lotes: {total}")

# Verificar
assert total == 6, f"Error: esperaba 6, obtuve {total}"
print("✅ Test pasado!")