# Configuración de GitHub Pages

## 📋 Descripción

El flujo automatizado genera un archivo `index.html` con el informe filterable de resistencia de concretos. Este archivo se almacena en la raíz del repositorio y está listo para ser desplegado con GitHub Pages.

## ⚙️ Pasos para configurar GitHub Pages

### 1. Acceder a la configuración del repositorio
- Ve a tu repositorio en GitHub
- Haz clic en **Settings** (Configuración)

### 2. Habilitar GitHub Pages
- En el menú izquierdo, busca la sección **Pages** (Páginas)
- En **Source** (Fuente), selecciona:
  - **Branch**: `main`
  - **Folder** (Carpeta): `/ (root)`
- Haz clic en **Save** (Guardar)

### 3. Esperar el despliegue
- GitHub procesará el cambio en unos minutos
- Una vez completado, verás un mensaje: "Your site is published at: https://tu-usuario.github.io/nombre-repo"

## 📊 Características del informe HTML

El informe generado incluye:

### Filtros disponibles:
- **Proyecto**: Filtrar por nombre de proyecto
- **Localización**: Filtrar por ubicación en la estructura
- **Edad (días)**: Filtrar por edad del concreto
- **Resistencia nominal (MPa)**: Filtrar por resistencia de diseño
- **Resistencia (MPa) Individual**: Filtrar por valores individuales
- **Dato**: Filtrar por referencia de dato

### Funcionalidades:
- ✅ Tabla interactiva con paginación
- ✅ Búsqueda y filtrado en tiempo real
- ✅ Colores según tipo de dato:
  - 🟢 Verde claro: Datos primarios
  - 🔵 Azul claro: Datos calculados
- ✅ Responsive (funciona en móvil)
- ✅ Información de registros mostrados
- ✅ Exportación de datos (botones DataTables)

## 🔄 Flujo de actualización

1. **Descargas automáticas** (`descargas-sgs.yml`):
   - Descarga datos de SGS y Concrelab

2. **Transformación** (`transformar.yml`):
   - Procesa y consolida datos
   - Genera `ConsolidadoResistenciasConcretos.xlsx`
   - **Genera `index.html`** ← NUEVO
   - Hace commit en `main`

3. **GitHub Pages**:
   - Detecta cambios en `main`
   - Despliega `index.html` automáticamente
   - URL: `https://tu-usuario.github.io/nombre-repo`

## 📝 Variables de entorno

No se requieren variables adicionales. El workflow usa:
- Token existente: `RESISTENCIA_CONCRETOS_TOKEN`
- Python 3.11 con pandas

## 🐛 Solución de problemas

### El HTML no se actualiza después de los cambios
1. Verifica que el workflow `transformar.yml` se haya ejecutado correctamente
2. Comprueba que `index.html` esté en la rama `main`
3. Espera 1-2 minutos para que GitHub Pages redesplegue

### GitHub Pages no muestra el sitio
1. Asegúrate de que GitHub Pages está habilitado en Settings → Pages
2. Verifica que la rama seleccionada es `main`
3. Comprueba que la carpeta es `/` (root)

### El archivo index.html no se genera
1. Revisa los logs del workflow en GitHub Actions
2. Verifica que `DatosTransformados/ConsolidadoResistenciasConcretos.xlsx` existe
3. Asegúrate de que `generar_informe_html.py` está en la raíz del repositorio

## 📚 Archivos involucrados

- `generar_informe_html.py`: Script que genera el HTML
- `.github/workflows/transformar.yml`: Workflow que ejecuta la generación
- `index.html`: Archivo generado (salida del informe)
- `ConsolidadoResistenciasConcretos.xlsx`: Fuente de datos

## ✨ Próximas mejoras (opcional)

- [ ] Agregar gráficas de tendencias
- [ ] Exportar a PDF
- [ ] Agregar más filtros avanzados
- [ ] Incluir estadísticas descriptivas
- [ ] Generar reportes por proyecto
