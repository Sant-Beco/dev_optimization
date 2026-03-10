# Semana 2, Día 1: Referencias y Memoria

## Concepto aprendido:
Python usa referencias para objetos mutables (listas, dicts, DataFrames).
Asignar una variable a otra NO crea copia, solo otra "etiqueta" al mismo objeto.

## Aha moment:
Ahora entiendo por qué a veces mi código modificaba datos que no debía.
Ejemplo: Cuando hacía "backup" de DataFrames antes de limpiar.

## Aplicación inmediata a mi código:
1. En limpiador_granja.py: Agregar .copy() antes de modificar DataFrames
2. En dashboard.py: Asegurar que análisis no modifiquen datos originales
3. En futuros scripts: SIEMPRE copiar antes de modificar

## Challenge completado:
- [x] Predicción Challenge 1: [tu respuesta]
- [x] Código corregido Challenge 2
- [x] Visualizador ejecutado
- [x] Reporte MEMORIA_REFERENCIAS.md generado

## Conexión con mi trabajo:
Cuando proceso datos de 5 lotes simultáneamente, necesito asegurar
que modificar datos de un lote no afecte a los otros.

## Próximo paso:
Día 2: Stack vs Heap visualizado - Cómo Python decide dónde guardar datos