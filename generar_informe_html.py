import pandas as pd
import os
import sys
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

        # Crear HTML
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informe de Resistencia de Concretos</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.4.1/css/buttons.dataTables.min.css">
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
            max-width: 1600px;
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
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
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

        .filtro-grupo input,
        .filtro-grupo select {{
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 0.95em;
            transition: border-color 0.3s;
        }}

        .filtro-grupo input:focus,
        .filtro-grupo select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.1);
        }}

        .botones-filtro {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
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
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
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
            font-size: 0.95em;
        }}

        tbody tr {{
            border-bottom: 1px solid #e9ecef;
            transition: background-color 0.2s;
        }}

        tbody tr:hover {{
            background: #f8f9fa;
        }}

        tbody td {{
            padding: 10px 12px;
            font-size: 0.95em;
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

        .resaltado {{
            font-weight: 600;
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

        .dataTables_filter {{
            display: none;
        }}

        .dataTables_length {{
            display: none;
        }}

        .dataTables_info {{
            color: #666;
            font-size: 0.9em;
        }}

        .paginacion {{
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 5px;
        }}

        .paginacion a,
        .paginacion span {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .paginacion a:hover {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}

        .paginacion .active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
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
                font-size: 0.85em;
            }}

            thead th,
            tbody td {{
                padding: 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Informe de Resistencia de Concretos</h1>
            <p class="fecha-generacion">Generado: {datetime.now().strftime('%d de %B de %Y a las %H:%M:%S')}</p>
        </header>

        <div class="filtros-section">
            <h2>Filtros</h2>
            <div class="filtros-grid">
                <div class="filtro-grupo">
                    <label for="filtro-proyecto">Proyecto</label>
                    <input type="text" id="filtro-proyecto" placeholder="Buscar proyecto...">
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-localizacion">Localización</label>
                    <input type="text" id="filtro-localizacion" placeholder="Buscar localización...">
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-edad">Edad (días)</label>
                    <input type="number" id="filtro-edad" placeholder="Buscar edad...">
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-resistencia-nominal">Resistencia nominal (MPa)</label>
                    <input type="number" id="filtro-resistencia-nominal" placeholder="Buscar resistencia...">
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-resistencia-individual">Resistencia (MPa) Individual</label>
                    <input type="number" id="filtro-resistencia-individual" placeholder="Buscar valor...">
                </div>
                <div class="filtro-grupo">
                    <label for="filtro-dato">Dato</label>
                    <input type="text" id="filtro-dato" placeholder="Buscar dato...">
                </div>
            </div>
            <div class="botones-filtro">
                <button class="btn-filtrar" onclick="aplicarFiltros()">🔍 Aplicar Filtros</button>
                <button class="btn-limpiar" onclick="limpiarFiltros()">🗑️ Limpiar Filtros</button>
            </div>
        </div>

        <div class="tabla-section">
            <table id="tabla-datos" class="display">
                <thead>
                    <tr>
"""

        # Agregar encabezados
        for col in df.columns:
            html_content += f"                        <th>{col}</th>\n"

        html_content += """                    </tr>
                </thead>
                <tbody>
"""

        # Agregar datos
        for idx, row in df.iterrows():
            html_content += "                    <tr>\n"
            for col in df.columns:
                valor = str(row[col]) if row[col] != "" else ""
                # Aplicar colores según el tipo de dato (simplificado)
                clase = ""
                if col in ["Resistencia (MPa) Individual", "Resistencia (%) Individual", "Conteo Elementos"]:
                    clase = 'class="datos-azules"'
                elif col in ["Proyecto", "Cilindro Nº", "Código de mezcla", "Localización", "Toma", "Rotura", "Edad (días)", "Resistencia nominal (MPa)", "Resistencia (%)", "TIPO"]:
                    clase = 'class="datos-verdes"'

                html_content += f'                        <td {clase}>{valor}</td>\n'
            html_content += "                    </tr>\n"

        html_content += """                </tbody>
            </table>
        </div>

        <div id="info-tabla" class="info-tabla">
            <span id="info-texto">Mostrando todos los registros</span>
        </div>

        <footer>
            <p>Sistema de Información de Resistencia de Concretos - INGEURBE</p>
        </footer>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script>
        let table;

        $(document).ready(function() {
            table = $('#tabla-datos').DataTable({
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
                },
                pageLength: 25,
                dom: '<"top"lf>rt<"bottom"ip>',
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    { responsivePriority: 2, targets: -1 }
                ]
            });

            // Ocultar la búsqueda global
            $('.dataTables_filter').hide();
        });

        function aplicarFiltros() {
            const proyecto = document.getElementById('filtro-proyecto').value.toLowerCase();
            const localizacion = document.getElementById('filtro-localizacion').value.toLowerCase();
            const edad = document.getElementById('filtro-edad').value;
            const resistenciaNominal = document.getElementById('filtro-resistencia-nominal').value;
            const resistenciaIndividual = document.getElementById('filtro-resistencia-individual').value;
            const dato = document.getElementById('filtro-dato').value.toLowerCase();

            $.fn.dataTable.ext.search.push(
                function(settings, data, dataIndex) {
                    const proyectoCol = data[0].toLowerCase();
                    const localizacionCol = data[3].toLowerCase();
                    const edadCol = data[6];
                    const resistenciaNominalCol = data[7];
                    const resistenciaIndividualCol = data[9];
                    const datoCol = data[data.length - 1].toLowerCase();

                    if (proyecto && proyectoCol.indexOf(proyecto) === -1) return false;
                    if (localizacion && localizacionCol.indexOf(localizacion) === -1) return false;
                    if (edad && edadCol !== edad) return false;
                    if (resistenciaNominal && resistenciaNominalCol !== resistenciaNominal) return false;
                    if (resistenciaIndividual && resistenciaIndividualCol !== resistenciaIndividual) return false;
                    if (dato && datoCol.indexOf(dato) === -1) return false;

                    return true;
                }
            );

            table.draw();
            actualizarInfo();
        }

        function limpiarFiltros() {
            document.getElementById('filtro-proyecto').value = '';
            document.getElementById('filtro-localizacion').value = '';
            document.getElementById('filtro-edad').value = '';
            document.getElementById('filtro-resistencia-nominal').value = '';
            document.getElementById('filtro-resistencia-individual').value = '';
            document.getElementById('filtro-dato').value = '';

            $.fn.dataTable.ext.search.length = 0;
            table.draw();
            actualizarInfo();
        }

        function actualizarInfo() {
            const info = table.page.info();
            const texto = `Mostrando ${{info.start + 1}} a ${{info.end}} de ${{info.recordsDisplay}} registros`;
            document.getElementById('info-texto').textContent = texto;
        }
    </script>
</body>
</html>
"""

        # Guardar HTML
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"[+] ✓ Informe HTML generado: {ruta_salida}")
        print(f"[+] Registros incluidos: {len(df)}")
        return True

    except Exception as e:
        print(f"[!] Error generando HTML: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    generar_informe_html()
