registros = [
    {'lote': 39, 'mortalidad': 3},
    {'lote': 40, 'mortalidad': 7},
    {'lote': 41, 'mortalidad': 2},
    {'lote': 42, 'mortalidad': 9},
]

# Tu código (1 línea):
ordenados = sorted(registros, key=lambda x: x['mortalidad'], reverse=True)

print(ordenados)

por_mortalidad = sorted(registros, key=lambda x: x['mortalidad'], reverse=False)
# [{'lote': 42, 'mortalidad': 9}, ...]