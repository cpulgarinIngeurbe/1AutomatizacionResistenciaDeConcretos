import pandas as pd
import os
import sys
import json
from datetime import datetime

# Configurar codificación UTF-8 para stdout
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generar_informe_html():
    """Genera un informe HTML filterable a partir del ConsolidadoResistenciasConcretos.xlsx"""

    ruta_consolidado = "DatosTransformados/ConsolidadoResistenciasConcretos.xlsx"
    ruta_salida = "index.html"

    if not os.path.exists(ruta_consolidado):
        print(f"[!] Archivo no encontrado: {ruta_consolidado}")
        return False

    try:
        print(f"[*] Leyendo archivo: {ruta_consolidado}")
        df = pd.read_excel(ruta_consolidado)
        print(f"[+] Datos cargados. Forma: {df.shape}")

        # Reemplazar NaN con vacío para HTML
        df = df.fillna("")

        # Campos para filtros
        campos_filtro = [
            "Proyecto",
            "Localización",
            "Edad (días)",
            "Resistencia nominal (MPa)",
            "Resistencia (MPa) Individual",
            "Dato"
        ]

        # Obtener valores únicos para los selects
        filtros_unicos = {}
        for campo in campos_filtro:
            if campo in df.columns:
                valores = sorted([str(v) for v in df[campo].unique() if v != ""])
                filtros_unicos[campo] = valores

        # Convertir datos a JSON para JavaScript
        datos_json = df.to_json(orient='records', default_handler=str)

        # Crear HTML
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe de Resistencia de Concretos</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1800px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 30px;
        }}

        header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
        }}

        h1 {{
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .fecha-generacion {{
            color: #666;
            font-size: 0.9em;
            margin-top: 10px;
        }}

        .filtros-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
            border: 1px solid #e9ecef;
        }}

        .filtros-section h2 {{
            color: #667eea;
            font-size: 1.2em;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }}

        .filtros-section h2::before {{
            content: "🔍";
            margin-right: 10px;
        }}

        .filtros-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }}

        .filtro-grupo {{
            display: flex;
            flex-direction: column;
        }}

        .filtro-grupo label {{
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
            font-size: 0.95em;
        }}

        .filtro-grupo select {{
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 0.95em;
            transition: border-color 0.3s;
            background-color: white;
            cursor: pointer;
        }}

        .filtro-grupo select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.1);
        }}

        .botones-filtro {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        button {{
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.95em;
        }}

        .btn-filtrar {{
            background: #667eea;
            color: white;
        }}

        .btn-filtrar:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}

        .btn-limpiar {{
            background: #e9ecef;
            color: #333;
        }}

        .btn-limpiar:hover {{
            background: #dee2e6;
        }}

        .tabla-section {{
            overflow-x: auto;
            margin-top: 20px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        thead {{
            background: #1F4788;
            color: white;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        thead th {{
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #1F4788;
            font-size: 0.9em;
        }}

        tbody tr {{
            border-bottom: 1px solid #e9ecef;
            transition: background-color 0.2s;
        }}

        tbody tr:hover {{
            background: #f0f0f0;
        }}

        tbody td {{
            padding: 10px 12px;
            font-size: 0.9em;
        }}

        tbody tr:nth-child(even) {{
            background: #f8f9fa;
        }}

        .datos-verdes {{
            background: #90EE90 !important;
        }}

        .datos-azules {{
            background: #ADD8E6 !important;
        }}

        .info-tabla {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
            color: #666;
            font-size: 0.9em;
        }}

        .paginacion {{
            display: flex;
            justify-content: center;
            gap: 5px;
            margin-top: 20px;
        }}

        .paginacion button {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            background: white;
            color: #333;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .paginacion button:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}

        .paginacion button.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}

        .paginacion button:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}

        .no-resultados {{
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 1.1em;
        }}

        footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
            color: #666;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}

            h1 {{
                font-size: 1.8em;
            }}

            .filtros-grid {{
                grid-template-columns: 1fr;
            }}

            table {{
                font-size: 0.8em;
            }}

            thead th,
            tbody td {{
                padding: 6px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Informe de Resistencia de Concretos</h1>
            <p class="fecha-generacion">Generado: {datetime.now().strftime('%d de %B de %Y a las %H:%M:%S')}</p>
        </header>

        <div class="filtros-section">
            <h2>Filtros</h2>
            <div class="filtros-grid">
                <div class="filtro-grupo">
                    <label for="filtro-proyecto">Proyecto</label>
                    <select id="filtro-proyecto">
                        <option value="">-- Todos --</option>
"""

        # Agregar opciones para Proyecto
        for valor in filtros_unicos.get("Proyecto", []):
            html_content += f'                        <option value="{valor}">{valor}</option>\n'

        html_content += """                    </select>
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-localizacion">Localización</label>
                    <select id="filtro-localizacion">
                        <option value="">-- Todos --</option>
"""

        # Agregar opciones para Localización
        for valor in filtros_unicos.get("Localización", []):
            html_content += f'                        <option value="{valor}">{valor}</option>\n'

        html_content += """                    </select>
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-edad">Edad (días)</label>
                    <select id="filtro-edad">
                        <option value="">-- Todos --</option>
"""

        # Agregar opciones para Edad
        for valor in filtros_unicos.get("Edad (días)", []):
            html_content += f'                        <option value="{valor}">{valor}</option>\n'

        html_content += """                    </select>
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-resistencia-nominal">Resistencia nominal (MPa)</label>
                    <select id="filtro-resistencia-nominal">
                        <option value="">-- Todos --</option>
"""

        # Agregar opciones para Resistencia nominal
        for valor in filtros_unicos.get("Resistencia nominal (MPa)", []):
            html_content += f'                        <option value="{valor}">{valor}</option>\n'

        html_content += """                    </select>
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-resistencia-individual">Resistencia (MPa) Individual</label>
                    <select id="filtro-resistencia-individual">
                        <option value="">-- Todos --</option>
"""

        # Agregar opciones para Resistencia Individual
        for valor in filtros_unicos.get("Resistencia (MPa) Individual", [])[:100]:  # Limitar a 100 opciones
            html_content += f'                        <option value="{valor}">{valor}</option>\n'

        html_content += """                    </select>
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-dato">Dato</label>
                    <select id="filtro-dato">
                        <option value="">-- Todos --</option>
"""

        # Agregar opciones para Dato
        for valor in filtros_unicos.get("Dato", []):
            html_content += f'                        <option value="{valor}">{valor}</option>\n'

        html_content += """                    </select>
                </div>
            </div>
            <div class="botones-filtro">
                <button class="btn-filtrar" onclick="aplicarFiltros()">Aplicar Filtros</button>
                <button class="btn-limpiar" onclick="limpiarFiltros()">Limpiar Filtros</button>
            </div>
        </div>

        <div id="info-tabla" class="info-tabla">
            <span id="info-texto">Cargando datos...</span>
        </div>

        <div class="tabla-section">
            <table id="tabla-datos">
                <thead>
                    <tr>
"""

        # Agregar encabezados
        for col in df.columns:
            html_content += f"                        <th>{col}</th>\n"

        html_content += """                    </tr>
                </thead>
                <tbody id="tabla-body">
                </tbody>
            </table>
        </div>

        <div class="paginacion" id="paginacion"></div>

        <footer>
            <p>Sistema de Información de Resistencia de Concretos - INGEURBE</p>
        </footer>
    </div>

    <script>
        // Datos globales
        const todosDatos = {datos_json};
        let datosFiltrados = todosDatos;
        const registrosPorPagina = 50;
        let paginaActual = 1;

        // Índices de columnas para colores
        const columnasVerdes = {json.dumps([i for i, col in enumerate(df.columns) if col in ['Resistencia (%)', 'Proyecto', 'TIPO', 'Cilindro Nº', 'Código de mezcla', 'Localización', 'Toma', 'Rotura', 'Edad (días)', 'Resistencia nominal (MPa)']])};
        const columnasAzules = {json.dumps([i for i, col in enumerate(df.columns) if col in ['Resistencia (MPa) Individual', 'Resistencia (%) Individual', 'Conteo Elementos']])};
        const nombresColumnas = {json.dumps(df.columns.tolist())};

        // Inicializar tabla
        document.addEventListener('DOMContentLoaded', function() {{
            mostrarPagina(1);
            configurarPaginacion();
        }});

        function aplicarFiltros() {{
            const filtros = {{
                proyecto: document.getElementById('filtro-proyecto').value,
                localizacion: document.getElementById('filtro-localizacion').value,
                edad: document.getElementById('filtro-edad').value,
                resistenciaNominal: document.getElementById('filtro-resistencia-nominal').value,
                resistenciaIndividual: document.getElementById('filtro-resistencia-individual').value,
                dato: document.getElementById('filtro-dato').value
            }};

            datosFiltrados = todosDatos.filter(row => {{
                if (filtros.proyecto && String(row['Proyecto']) !== filtros.proyecto) return false;
                if (filtros.localizacion && String(row['Localización']) !== filtros.localizacion) return false;
                if (filtros.edad && String(row['Edad (días)']) !== filtros.edad) return false;
                if (filtros.resistenciaNominal && String(row['Resistencia nominal (MPa)']) !== filtros.resistenciaNominal) return false;
                if (filtros.resistenciaIndividual && String(row['Resistencia (MPa) Individual']) !== filtros.resistenciaIndividual) return false;
                if (filtros.dato && String(row['Dato']) !== filtros.dato) return false;
                return true;
            }});

            paginaActual = 1;
            mostrarPagina(1);
            configurarPaginacion();
        }}

        function limpiarFiltros() {{
            document.getElementById('filtro-proyecto').value = '';
            document.getElementById('filtro-localizacion').value = '';
            document.getElementById('filtro-edad').value = '';
            document.getElementById('filtro-resistencia-nominal').value = '';
            document.getElementById('filtro-resistencia-individual').value = '';
            document.getElementById('filtro-dato').value = '';

            datosFiltrados = todosDatos;
            paginaActual = 1;
            mostrarPagina(1);
            configurarPaginacion();
        }}

        function mostrarPagina(numero) {{
            paginaActual = numero;
            const inicio = (numero - 1) * registrosPorPagina;
            const fin = inicio + registrosPorPagina;
            const registrosPagina = datosFiltrados.slice(inicio, fin);

            const tbody = document.getElementById('tabla-body');
            tbody.innerHTML = '';

            if (registrosPagina.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="' + nombresColumnas.length + '" class="no-resultados">No se encontraron registros</td></tr>';
                actualizarInfo();
                return;
            }}

            registrosPagina.forEach(row => {{
                const tr = document.createElement('tr');
                nombresColumnas.forEach((col, idx) => {{
                    const td = document.createElement('td');
                    const valor = row[col] !== null && row[col] !== undefined ? String(row[col]) : '';
                    td.textContent = valor;

                    if (columnasVerdes.includes(idx)) {{
                        td.className = 'datos-verdes';
                    }} else if (columnasAzules.includes(idx)) {{
                        td.className = 'datos-azules';
                    }}

                    tr.appendChild(td);
                }});
                tbody.appendChild(tr);
            }});

            actualizarInfo();
        }}

        function configurarPaginacion() {{
            const totalPaginas = Math.ceil(datosFiltrados.length / registrosPorPagina);
            const paginacionDiv = document.getElementById('paginacion');
            paginacionDiv.innerHTML = '';

            if (totalPaginas <= 1) return;

            // Botón anterior
            const btnAnterior = document.createElement('button');
            btnAnterior.textContent = '← Anterior';
            btnAnterior.disabled = paginaActual === 1;
            btnAnterior.onclick = () => {{
                if (paginaActual > 1) mostrarPagina(paginaActual - 1);
            }};
            paginacionDiv.appendChild(btnAnterior);

            // Números de página
            const inicio = Math.max(1, paginaActual - 2);
            const fin = Math.min(totalPaginas, paginaActual + 2);

            if (inicio > 1) {{
                const btn1 = document.createElement('button');
                btn1.textContent = '1';
                btn1.onclick = () => mostrarPagina(1);
                paginacionDiv.appendChild(btn1);

                if (inicio > 2) {{
                    const puntos = document.createElement('span');
                    puntos.textContent = '...';
                    paginacionDiv.appendChild(puntos);
                }}
            }}

            for (let i = inicio; i <= fin; i++) {{
                const btn = document.createElement('button');
                btn.textContent = i;
                if (i === paginaActual) btn.className = 'active';
                btn.onclick = () => mostrarPagina(i);
                paginacionDiv.appendChild(btn);
            }}

            if (fin < totalPaginas) {{
                if (fin < totalPaginas - 1) {{
                    const puntos = document.createElement('span');
                    puntos.textContent = '...';
                    paginacionDiv.appendChild(puntos);
                }}

                const btnUltima = document.createElement('button');
                btnUltima.textContent = totalPaginas;
                btnUltima.onclick = () => mostrarPagina(totalPaginas);
                paginacionDiv.appendChild(btnUltima);
            }}

            // Botón siguiente
            const btnSiguiente = document.createElement('button');
            btnSiguiente.textContent = 'Siguiente →';
            btnSiguiente.disabled = paginaActual === totalPaginas;
            btnSiguiente.onclick = () => {{
                if (paginaActual < totalPaginas) mostrarPagina(paginaActual + 1);
            }};
            paginacionDiv.appendChild(btnSiguiente);
        }}

        function actualizarInfo() {{
            const inicio = (paginaActual - 1) * registrosPorPagina + 1;
            const fin = Math.min(paginaActual * registrosPorPagina, datosFiltrados.length);
            const texto = `Mostrando ${{inicio}} a ${{fin}} de ${{datosFiltrados.length}} registros (Total: ${{todosDatos.length}})`;
            document.getElementById('info-texto').textContent = texto;
        }}
    </script>
</body>
</html>
"""

        # Guardar HTML
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[+] Informe HTML generado: {ruta_salida}")
        print(f"[+] Registros incluidos: {len(df)}")
        print(f"[+] Filtros disponibles: {len(filtros_unicos)}")
        return True

    except Exception as e:
        print(f"[!] Error generando HTML: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generar_informe_html()
