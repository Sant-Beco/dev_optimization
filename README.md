# Proyectos de Optimización y Análisis

## Día 1: Organizador de Archivos
- **Problema resuelto:** Descargas desorganizadas
- **Tecnología:** Python + shutil
- **Próximos pasos:** Ejecutarlo automáticamente cada noche

## Aprendido hoy:
- [ ] Git init, add, commit
- [ ] Estructura básica Python
- [ ] Manipulación de archivos con pathlib

## Día 2: Script Profesional con Logs

### Mejoras implementadas:
- ✅ Clase OrganizadorArchivos (código reutilizable)
- ✅ Sistema de logs persistente
- ✅ Manejo de errores (try/except)
- ✅ Reportes en JSON
- ✅ Prevención de sobrescritura de archivos

### Resultados:
- Día 1: 109 archivos organizados
- Día 2: Sistema con trazabilidad completa

### Aprendido:
- Programación orientada a objetos básica
- Logging profesional
- Manejo de excepciones
- Serialización JSON

## Día 5: Subcategorización Jerárquica

### Problema resuelto:
- 208 documentos genéricos → 5 subcategorías específicas
- Mejor navegabilidad y búsqueda

### Estructura implementada:
```
Documentos/
  ├── PDFs/
  ├── Excel/
  ├── Word/
  ├── Presentaciones/
  └── Textos/
```

### Mejoras vs Día 4:
- Organización de 2 niveles (Categoría → Subcategoría)
- Detección inteligente por extensión
- Modo dry-run para pruebas seguras

### Próxima optimización:
- Organizar por fecha de creación
- Detección de contenido (facturas, reportes)

## Día 6: Limpieza y Análisis de CSV

### Problema resuelto:
- Procesar CSVs sucios del mundo real
- Detectar y limpiar automáticamente: fechas, precios, porcentajes
- Eliminar duplicados y manejar nulos

### Capacidades del limpiador:
- ✅ Detección automática de encoding
- ✅ Normalización de nombres de columnas
- ✅ Eliminación de duplicados
- ✅ Limpieza de precios: "$1,234.56" → 1234.56
- ✅ Conversión de fechas a formato estándar
- ✅ Manejo inteligente de nulos
- ✅ Generación de estadísticas descriptivas
- ✅ Reporte de cambios realizados

### Aprendido:
- ETL (Extract, Transform, Load)
- Pandas: dropna(), drop_duplicates(), to_datetime()
- Regex para limpieza de strings
- Detección automática de tipos de datos

### Resultado:
CSV limpio listo para análisis o importar a Excel/SQL

## Día 7: CSV Complejo + Cierre Semana 1

### Problema real resuelto:
CSV de granja avícola con estructura compleja:
- 1 columna con 150+ campos separados por `;`
- Headers múltiples mezclados
- 137 filas duplicadas (30% de ruido)

### Solución:
Limpiador especializado que:
- ✅ Detecta delimitador automáticamente
- ✅ Prueba múltiples configuraciones de carga
- ✅ Interactivo (usuario decide qué limpiar)
- ✅ Detecta columnas inútiles (95%+ nulos, 1 valor único)
- ✅ Genera reporte de cambios

### Resultado:
456 filas caóticas → 319 filas estructuradas
1 columna → [X] columnas bien definidas

### Aprendido:
- CSV parsing avanzado (sep, skiprows, encoding)
- Detección automática de estructura
- Pipeline interactivo
- Análisis de calidad de datos

---

## 🏆 RESUMEN SEMANA 1

### Logros:
- ✅ 7 días consecutivos
- ✅ 4 scripts de automatización
- ✅ 1 dashboard visual
- ✅ 211+ archivos organizados
- ✅ CSV real de producción limpiado
- ✅ 10+ commits en GitHub

### Habilidades desbloqueadas:
1. Git + GitHub workflow
2. Python scripting
3. POO básica
4. Pandas (básico → intermedio)
5. Matplotlib visualización
6. CLI con argparse
7. Manejo de archivos complejos
8. CSV parsing avanzado

### Proyectos completados:
1. Organizador de archivos v1-v3
2. Dashboard con 3 gráficos
3. Limpiador universal CSV
4. Limpiador especializado granja

### Próxima semana (Semana 2):
- Fundamentos computacionales (CPU, memoria, Big O)
- Tests con pytest
- Git avanzado (branches, PRs)
- SQL básico

### Reflexión:
*"En 7 días pasé de 0 a tener herramientas que uso diariamente.
El enfoque de 'aprender haciendo' funciona. Cada script resuelve
un problema real de mi trabajo."*