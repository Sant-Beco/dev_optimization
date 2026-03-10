# Reporte: Análisis de Memoria en Python

**Generado:** 2026-03-09 19:39:41

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
| produccion_dia1 |      1942020726272 | list       |     88 bytes |
| produccion_backup |      1942020726272 | list       |     88 bytes |
| produccion_copia |      1942020726336 | list       |     88 bytes |
| lote_39         |      1942020725376 | dict       |    184 bytes |
|   mortalidad    |      1942020726336 | list       |     88 bytes |
| aves_dia1       |      1942018108432 | int        |     28 bytes |
| aves_backup     |      1942018108432 | int        |     28 bytes |
| aves_backup     |      1942018112528 | int        |     28 bytes |


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
