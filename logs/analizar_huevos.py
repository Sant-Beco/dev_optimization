# analizar_huevos.py
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('LOTE 39 (100)(MOVIMIENTO HUEVO)_LIMPIO.csv', sep=';')

print(df.head())
print(df.info())

# Si tiene columnas de fechas y totales, graficar
# (ajusta según tus columnas reales)
if 'FECHA' in df.columns and 'TOTAL' in df.columns:
    df.plot(x='FECHA', y='TOTAL', kind='line')
    plt.title('Producción de Huevos - Lote 39')
    plt.savefig('produccion_lote39.png')
    print("📊 Gráfico guardado: produccion_lote39.png")