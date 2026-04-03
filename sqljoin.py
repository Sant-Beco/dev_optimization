import sqlite3

class SQLJoinsDemo:
    """Demuestra JOINs con ejemplos reales"""
    
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')  # BD en memoria (rápido)
        self.cursor = self.conn.cursor()
        self.setup()
    
    def setup(self):
        """Crear datos de ejemplo"""
        # Tabla lotes
        self.cursor.execute('''
            CREATE TABLE lotes (
                id INTEGER PRIMARY KEY,
                numero INTEGER,
                raza TEXT
            )
        ''')
        
        # Tabla producción
        self.cursor.execute('''
            CREATE TABLE produccion (
                id INTEGER PRIMARY KEY,
                fecha TEXT,
                lote_id INTEGER,
                huevos INTEGER,
                mortalidad INTEGER
            )
        ''')
        
        # Insertar datos
        lotes = [(1, 39, 'Hy-Line'), (2, 40, 'Lohmann'), (3, 41, 'Hy-Line')]
        self.cursor.executemany('INSERT INTO lotes VALUES (?,?,?)', lotes)
        
        produccion = [
            (1, '2024-03-01', 1, 9500, 2),
            (2, '2024-03-01', 2, 8200, 5),
            (3, '2024-03-01', 3, 9300, 1),
            (4, '2024-03-02', 1, 9480, 3),
            (5, '2024-03-02', 2, 8100, 7),
        ]
        self.cursor.executemany('INSERT INTO produccion VALUES (?,?,?,?,?)', produccion)
        self.conn.commit()
    
    def ejemplo_1_inner_join(self):
        """INNER JOIN: Solo filas que coinciden en ambas tablas"""
        print("\n1️⃣ INNER JOIN - Producción con info de lotes")
        print("="*60)
        
        query = '''
            SELECT 
                p.fecha,
                l.numero AS lote,
                l.raza,
                p.huevos,
                p.mortalidad
            FROM produccion p
            INNER JOIN lotes l ON p.lote_id = l.id
            ORDER BY p.fecha, l.numero
        '''
        
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        
        print(f"{'Fecha':12} | {'Lote':5} | {'Raza':10} | {'Huevos':>7} | {'Muertes':>7}")
        print("-"*60)
        for fecha, lote, raza, huevos, mort in resultados:
            print(f"{fecha:12} | {lote:>5} | {raza:10} | {huevos:>7} | {mort:>7}")
    
    def ejemplo_2_agregacion(self):
        """JOIN + GROUP BY: Resumen por lote"""
        print("\n2️⃣ JOIN + AGREGACIÓN - Totales por lote")
        print("="*60)
        
        query = '''
            SELECT 
                l.numero AS lote,
                l.raza,
                COUNT(*) AS dias,
                SUM(p.huevos) AS total_huevos,
                AVG(p.huevos) AS promedio,
                SUM(p.mortalidad) AS total_muertes
            FROM produccion p
            JOIN lotes l ON p.lote_id = l.id
            GROUP BY l.numero, l.raza
            ORDER BY total_huevos DESC
        '''
        
        self.cursor.execute(query)
        
        print(f"{'Lote':5} | {'Raza':10} | {'Días':>5} | {'Total':>8} | {'Prom':>7} | {'Muertes':>7}")
        print("-"*60)
        for lote, raza, dias, total, prom, muertes in self.cursor.fetchall():
            print(f"{lote:>5} | {raza:10} | {dias:>5} | {total:>8,} | {prom:>7.0f} | {muertes:>7}")
    
    def ejemplo_3_filtros(self):
        """JOIN + WHERE: Lotes con problemas"""
        print("\n3️⃣ JOIN + FILTROS - Alertas de mortalidad")
        print("="*60)
        
        query = '''
            SELECT 
                l.numero AS lote,
                l.raza,
                p.fecha,
                p.mortalidad
            FROM produccion p
            JOIN lotes l ON p.lote_id = l.id
            WHERE p.mortalidad > 4
            ORDER BY p.mortalidad DESC
        '''
        
        self.cursor.execute(query)
        resultados = self.cursor.fetchall()
        
        if resultados:
            print("🚨 ALERTAS:")
            for lote, raza, fecha, mort in resultados:
                nivel = "🔴 CRÍTICO" if mort >= 7 else "🟡 ADVERTENCIA"
                print(f"  {nivel}: Lote {lote} ({raza}) - {fecha} - {mort} muertes")
        else:
            print("✅ Sin alertas")
    
    def ejemplo_4_ranking(self):
        """Caso real: Mejor lote del día"""
        print("\n4️⃣ CASO REAL - Mejor lote por día")
        print("="*60)
        
        query = '''
            SELECT 
                p.fecha,
                l.numero AS lote,
                l.raza,
                p.huevos
            FROM produccion p
            JOIN lotes l ON p.lote_id = l.id
            WHERE p.huevos = (
                SELECT MAX(huevos) 
                FROM produccion 
                WHERE fecha = p.fecha
            )
        '''
        
        self.cursor.execute(query)
        
        print(f"{'Fecha':12} | {'🥇 Lote':7} | {'Raza':10} | {'Huevos':>8}")
        print("-"*50)
        for fecha, lote, raza, huevos in self.cursor.fetchall():
            print(f"{fecha:12} | {lote:>7} | {raza:10} | {huevos:>8,}")
    
    def ejecutar_demo(self):
        """Ejecutar todos los ejemplos"""
        print("\n🔗 SQL JOINS EN ACCIÓN")
        self.ejemplo_1_inner_join()
        self.ejemplo_2_agregacion()
        self.ejemplo_3_filtros()
        self.ejemplo_4_ranking()
        print("\n" + "="*60)
        print("✅ Demo completada")
        self.conn.close()


# Ejecutar
demo = SQLJoinsDemo()
demo.ejecutar_demo()


query = """SELECT 
    l.raza,
    SUM(p.huevos) AS total
FROM produccion p
JOIN lotes l ON p.lote_id = l.id
GROUP BY l.raza
ORDER BY total ASC
LIMIT 1;
"""