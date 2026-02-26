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