import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

# Configuración de estilo
plt.style.use('ggplot')  # Estilo profesional
plt.rcParams['figure.figsize'] = (12, 8)  # Tamaño de gráficos

class DashboardOrganizador:
    """Analiza y visualiza los reportes de organización"""
    
    def __init__(self):
        self.reportes_path = Path("logs")
        self.datos = []
        self.df = None
    
    def cargar_datos(self):
        """Carga todos los reportes JSON"""
        print("📂 Cargando reportes históricos...\n")
        
        archivos = list(self.reportes_path.glob("reporte_*.json"))
        
        if not archivos:
            print("❌ No se encontraron reportes")
            return False
        
        for archivo in archivos:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extraer datos relevantes
                reporte = {
                    'fecha': data.get('timestamp', ''),
                    'archivos': data.get('archivos_procesados', 0),
                    'movidos': data.get('archivos_movidos', 0),
                    'errores': data.get('errores', 0),
                    'modo': data.get('modo', 'ejecucion')
                }
                
                # Agregar categorías
                for cat, cant in data.get('por_categoria', {}).items():
                    reporte[cat] = cant
                
                self.datos.append(reporte)
        
        # Crear DataFrame
        self.df = pd.DataFrame(self.datos)
        print(f"✅ Cargados {len(self.datos)} reportes\n")
        return True
    
    def resumen_general(self):
        """Muestra estadísticas generales"""
        print("="*60)
        print("📊 RESUMEN GENERAL")
        print("="*60)
        
        total_archivos = self.df['archivos'].sum()
        total_errores = self.df['errores'].sum()
        tasa_exito = ((total_archivos - total_errores) / total_archivos * 100) if total_archivos > 0 else 0
        
        print(f"Total archivos procesados: {total_archivos}")
        print(f"Total errores: {total_errores}")
        print(f"Tasa de éxito: {tasa_exito:.1f}%")
        print(f"Ejecuciones realizadas: {len(self.df)}")
        print(f"Promedio por ejecución: {total_archivos/len(self.df):.1f} archivos")
        print()
    
    def grafico_categorias(self):
        """Gráfico de barras: distribución por categorías"""
        print("📊 Generando gráfico de categorías...")
        
        # Columnas de categorías
        categorias_cols = ['Imagenes', 'Documentos', 'Videos', 'Audio', 
                          'Comprimidos', 'Codigo', 'Otros']
        
        # Sumar todas las categorías
        totales = {}
        for col in categorias_cols:
            if col in self.df.columns:
                total = self.df[col].sum()
                if total > 0:  # Solo categorías con datos
                    totales[col] = total
        
        # Crear gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categorias = list(totales.keys())
        valores = list(totales.values())
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
        
        bars = ax.bar(categorias, valores, color=colores[:len(categorias)])
        
        # Etiquetas en las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Categoría', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cantidad de Archivos', fontsize=12, fontweight='bold')
        ax.set_title('Distribución de Archivos por Categoría', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Guardar
        plt.savefig('dashboard_categorias.png', dpi=300, bbox_inches='tight')
        print("✅ Guardado: dashboard_categorias.png\n")
        plt.close()
    
    def grafico_pastel(self):
        """Gráfico circular: porcentaje por categoría"""
        print("📊 Generando gráfico circular...")
        
        categorias_cols = ['Imagenes', 'Documentos', 'Videos', 'Audio', 
                          'Comprimidos', 'Codigo', 'Otros']
        
        totales = {}
        for col in categorias_cols:
            if col in self.df.columns:
                total = self.df[col].sum()
                if total > 0:
                    totales[col] = total
        
        # Crear gráfico
        fig, ax = plt.subplots(figsize=(10, 8))
        
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
        
        wedges, texts, autotexts = ax.pie(
            totales.values(),
            labels=totales.keys(),
            autopct='%1.1f%%',
            startangle=90,
            colors=colores[:len(totales)],
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )
        
        # Mejorar texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
        
        ax.set_title('Proporción de Archivos por Tipo', fontsize=14, fontweight='bold', pad=20)
        
        plt.savefig('dashboard_proporcion.png', dpi=300, bbox_inches='tight')
        print("✅ Guardado: dashboard_proporcion.png\n")
        plt.close()
    
    def grafico_timeline(self):
        """Gráfico de línea: archivos procesados en el tiempo"""
        print("📊 Generando timeline...")
        
        if len(self.df) < 2:
            print("⚠️  Se necesitan al menos 2 ejecuciones para timeline\n")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Ordenar por fecha
        df_sorted = self.df.sort_values('fecha')
        
        # Crear eje X simplificado
        x = range(len(df_sorted))
        y = df_sorted['archivos'].values
        
        ax.plot(x, y, marker='o', linewidth=2, markersize=8, color='#4ECDC4')
        ax.fill_between(x, y, alpha=0.3, color='#4ECDC4')
        
        # Etiquetas
        for i, (xi, yi) in enumerate(zip(x, y)):
            ax.text(xi, yi + 2, str(int(yi)), ha='center', fontweight='bold')
        
        ax.set_xlabel('Ejecución', fontsize=12, fontweight='bold')
        ax.set_ylabel('Archivos Procesados', fontsize=12, fontweight='bold')
        ax.set_title('Evolución de Archivos Procesados', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f'#{i+1}' for i in x])
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('dashboard_timeline.png', dpi=300, bbox_inches='tight')
        print("✅ Guardado: dashboard_timeline.png\n")
        plt.close()
    
    def generar_reporte_html(self):
        """Genera reporte HTML con todos los gráficos"""
        print("📄 Generando reporte HTML...")
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Organizador de Archivos</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #2d3748;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #718096;
            margin-bottom: 30px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .chart {{
            margin: 30px 0;
            text-align: center;
        }}
        .chart img {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #718096;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Dashboard de Organización</h1>
        <p class="subtitle">Análisis de {len(self.df)} ejecuciones | Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Total Archivos</div>
                <div class="stat-number">{self.df['archivos'].sum()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Ejecuciones</div>
                <div class="stat-number">{len(self.df)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Tasa de Éxito</div>
                <div class="stat-number">{((self.df['archivos'].sum() - self.df['errores'].sum()) / self.df['archivos'].sum() * 100):.1f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Promedio/Ejecución</div>
                <div class="stat-number">{self.df['archivos'].mean():.0f}</div>
            </div>
        </div>
        
        <div class="chart">
            <h2>Distribución por Categorías</h2>
            <img src="dashboard_categorias.png" alt="Categorías">
        </div>
        
        <div class="chart">
            <h2>Proporción de Tipos</h2>
            <img src="dashboard_proporcion.png" alt="Proporción">
        </div>
        
        <div class="chart">
            <h2>Timeline de Procesamiento</h2>
            <img src="dashboard_timeline.png" alt="Timeline">
        </div>
        
        <div class="footer">
            🚀 Generado automáticamente por dashboard.py
        </div>
    </div>
</body>
</html>
"""
        
        with open('dashboard.html', 'w', encoding='utf-8') as f:
            f.write(html)
        
        print("✅ Guardado: dashboard.html\n")
    
    def generar_completo(self):
        """Genera todos los gráficos y reportes"""
        if not self.cargar_datos():
            return
        
        self.resumen_general()
        self.grafico_categorias()
        self.grafico_pastel()
        self.grafico_timeline()
        self.generar_reporte_html()
        
        print("="*60)
        print("✅ DASHBOARD GENERADO EXITOSAMENTE")
        print("="*60)
        print("\n📁 Archivos creados:")
        print("  • dashboard_categorias.png")
        print("  • dashboard_proporcion.png")
        print("  • dashboard_timeline.png")
        print("  • dashboard.html")
        print("\n💡 Abre 'dashboard.html' en tu navegador para ver el reporte completo\n")


if __name__ == "__main__":
    dashboard = DashboardOrganizador()
    dashboard.generar_completo()