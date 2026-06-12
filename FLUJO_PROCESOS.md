# Secuencia Lógica de Procesos - Sistema de Informes de Resistencia

## 📊 Diagrama de Flujo Completo

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INICIO DEL CICLO                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 1️⃣  DESCARGAS-SGS.yml                                                   │
│ ─────────────────────────────────────────────────────────────────────   │
│ • Trigger: Manual (workflow_dispatch)                                   │
│ • Acción: Descarga datos de SGS (web scraping con Playwright)          │
│ • Salida: datos/PROYECTO_SGS_YYYYMMDD_HHMMSS.xlsx                      │
│ • Archivos generados: CSV/XLSX descargados de plataforma SGS           │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2️⃣  TRANSFORMAR.yml (Concrelab + SGS + JOIN + Teóricas)                │
│ ─────────────────────────────────────────────────────────────────────   │
│ • Trigger: Manual (workflow_dispatch) O automático después descarga     │
│ • Entradas: datos/*.xlsx + ConsolidadoResistenciaTeoricas.xlsx         │
│ • Procesa:                                                               │
│   FASE 1 - Transformación:                                              │
│   - Lee archivos Concrelab y SGS                                        │
│   - Normaliza columnas                                                   │
│   - Agrega TIPO (MURO, PLACA, etc.)                                     │
│   - Calcula PK, Resistencia Promedio, Conteo, Promedio Móvil          │
│   - Aplica formateo condicional                                         │
│   FASE 2 - JOIN:                                                        │
│   - Lee datos teóricos                                                  │
│   - Une por PK (clave primaria)                                         │
│   - Agrega columna "Dato" del consolidado teórico                       │
│   - Calcula "Cumplimiento norma b" = Dato - Resistencia Promedio      │
│   - Si Dato está vacío → "NoValido"                                     │
│   - Color-code: AZUL si coincide, ROJO si no encuentra match           │
│ • Salida:                                                                │
│   - DatosTransformados/PROYECTO_Concrelab.xlsx                          │
│   - DatosTransformados/PROYECTO_SGS.xlsx                                │
│   - DatosTransformados/ConsolidadoResistenciasConcretos.xlsx (enriquecido)
│ • Commit: datos/ DatosTransformados/                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3️⃣  ENRIQUECER-CONSOLIDADO-TEORICAS.yml                                │
│ ─────────────────────────────────────────────────────────────────────   │
│ • Trigger: Manual (workflow_dispatch)                                   │
│ • Entrada: ConsolidadoResistenciaTeoricas.xlsx                          │
│ • Acción: Agrega columna PK con formato estandarizado                   │
│ • Salida: ConsolidadoResistenciaTeoricas.xlsx (enriquecido con PK)     │
│ • Commit: ConsolidadoResistenciaTeoricas.xlsx                           │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 5️⃣  GENERAR-INFORME.yml (NUEVO)                                        │
│ ─────────────────────────────────────────────────────────────────────   │
│ • Trigger:                                                               │
│   - Manual: workflow_dispatch                                           │
│   - Automático: después de transformar.yml (workflow_run)               │
│ • Entrada: DatosTransformados/ConsolidadoResistenciasConcretos.xlsx    │
│ • Acción:                                                                │
│   - Lee consolidado                                                      │
│   - Extrae valores únicos para cada filtro                              │
│   - Convierte datos a JSON                                              │
│   - Genera index.html interactivo con:                                  │
│     ✓ Selects poblados dinámicamente                                    │
│     ✓ Tabla con 5798 registros                                          │
│     ✓ Colores: verde (primarios), azul (calculados)                    │
│     ✓ Paginación (50 registros/página)                                  │
│     ✓ Filtros funcionales                                               │
│ • Salida: index.html (1MB)                                              │
│ • Commit: index.html                                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 6️⃣  GITHUB PAGES (Automático)                                          │
│ ─────────────────────────────────────────────────────────────────────   │
│ • Trigger: Cambios en index.html en rama main                           │
│ • Acción: Detecta y despliega automáticamente                           │
│ • URL: https://usuario.github.io/nombre-repo/                          │
│ • Tiempo: 1-2 minutos                                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    ✅ INFORME DISPONIBLE                                │
│              Usuarios acceden y usan filtros                            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Secuencia Recomendada de Ejecución Manual

### **Opción 1: Flujo Completo (Desde el inicio)**

```
1. Ejecutar: descargas-sgs.yml
   ↓ (esperar 5-10 min)
   
2. Ejecutar: transformar.yml (incluye JOIN + enriquecimiento)
   ↓ (esperar 3-4 min)
   
3. Ejecutar: generar-informe.yml (OPCIONAL - se ejecuta automático)
   ↓ (esperar 1 min)
   
4. Acceder a: https://usuario.github.io/nombre-repo/
   ✅ Informe disponible con datos actualizados
```

### **Opción 2: Flujo Rápido (Solo si datos ya existen)**

```
1. Ejecutar: transformar.yml (incluye JOIN + enriquecimiento)
   ↓ (automático → generar-informe.yml)
   
2. Esperar 3-4 minutos
   
3. Acceder a: https://usuario.github.io/nombre-repo/
   ✅ Informe actualizado
```

### **Opción 3: Solo Informe (Sin cambiar datos)**

```
1. Ejecutar: generar-informe.yml
   ↓ (1 min)
   
2. Acceder a informe
   ✅ (útil si hay cambios en el código de generación)
```

---

## 📋 Dependencias entre Workflows

```
descargas-sgs.yml
       │
       └──→ transformar.yml (manual - incluye JOIN integrado)
              │
              ├──→ enriquecer-consolidado-teoricas.yml (manual)
              │
              └──→ generar-informe.yml (automático + manual)
                     │
                     └──→ GitHub Pages (automático)
                            │
                            └──→ index.html DISPONIBLE
```

---

## 🎯 Qué Datos Contiene Cada Archivo

### **Entrada a descargas-sgs.yml:**
- Credenciales y URLs (desde secrets)
- Nombres de proyectos

### **Salida de transformar.yml:**
- `ConsolidadoResistenciasConcretos.xlsx` (5798 registros)
  - Proyecto, Cilindro Nº, Código de mezcla, Localización
  - Toma, Rotura, Edad (días), Resistencia nominal
  - Resistencia (MPa) Individual, % Individual
  - Resistencia Promedio, Conteo, Promedio móvil
  - TIPO, PK

### **Salida de join-por-pk.yml:**
- `ConsolidadoResistenciasConcretos.xlsx` + columna **Dato**

### **Salida de generar-informe.yml:**
- `index.html` (tabla filterable con 6 selects)
  - Proyecto
  - Localización
  - Edad (días)
  - Resistencia nominal (MPa)
  - Resistencia Individual (MPa)
  - Dato

---

## ⚡ Cambios Realizados

### **Combinación de Workflows**

- ✅ `transformar.yml` ahora integra la lógica de `join-por-pk.yml`
- ✅ Un único workflow maneja: Transformación + JOIN + Enriquecimiento
- ✅ Se eliminó `join-por-pk.yml` por redundancia
- ✅ Nueva columna "Cumplimiento norma b" = Dato - Resistencia Promedio
- ✅ Si Dato está vacío, muestra "NoValido"

---

## 📌 Matriz de Responsabilidades

| Workflow | Entrada | Proceso | Salida | Trigger |
|----------|---------|---------|--------|---------|
| descargas-sgs | URLs + credenciales | Web scraping | datos/*.xlsx | Manual |
| transformar | datos/*.xlsx + Teóricas | Transformación + JOIN + enriquecimiento | Consolidado con Dato + Cumplimiento norma b | Manual |
| enriquecer | Datos teóricos | Agrega PK | ConsolidadoResistenciaTeoricas.xlsx | Manual |
| generar-informe | Consolidado | Genera HTML | index.html | Auto + Manual |
| GitHub Pages | index.html | Despliega | URL pública | Auto |

---

## 💡 Recomendaciones Finales

### **1. Automatización completa (Ideal)**
Convertir todos los workflows a desencadenarse automáticamente:
```
descargas-sgs (manual) → transformar (auto) → enriquecer (auto) 
  → join (auto) → generar-informe (auto) → GitHub Pages (auto)
```

### **2. Separación de responsabilidades (Actual)**
- Cada workflow hace UNA cosa
- Triggers manuales = control total
- generar-informe.yml es independiente = flexible

### **3. Monitoreo**
- Revisar logs de cada workflow
- Verificar que ConsolidadoResistenciasConcretos.xlsx tenga columna "Dato"
- Si falta "Dato" → no ejecutaste join-por-pk.yml

---

## 🚀 Próximos Pasos Sugeridos

1. **¿Deseas que todos los workflows se ejecuten automáticamente en cadena?**
2. **¿Necesitas agregar notificaciones cuando se completa cada paso?**
3. **¿Quieres un dashboard que muestre el estado de cada workflow?**
4. **¿Deseas cambiar la frecuencia de descargas (por ejemplo, diaria)?**
