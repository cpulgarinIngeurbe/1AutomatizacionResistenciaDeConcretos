# Proyecto Resistencia Concretos

Versión: Lunes - 09 de junio

Descarga masiva automatizada de reportes de resistencia de concretos desde Concrelab y SGS.

## Configuración

### Secrets Requeridos
Para cada proyecto, configurar en: Settings → Secrets and variables → Actions

**Formato:**

- `{ProyectoNombre}_SGS_Usuario` + `{ProyectoNombre}_SGS_Contraseña` (para SGS)
- `{ProyectoNombre}_Concrelab_Usuario` + `{ProyectoNombre}_Concrelab_Contraseña` (para Concrelab)
- `GH_TOKEN` (token de GitHub)

## Archivos
Los archivos se descargan en `datos/` con formato:

- `{Proyecto}_SGS_YYYYMMDD_HHMMSS.xlsx`
- `{Proyecto}_Concrelab_YYYYMMDD_HHMMSS.xlsx`
