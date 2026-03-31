import sqlite3
from datetime import datetime
import random

class BaseDatosGranja:
    """Primera base de datos real para tu granja"""
    
    def __init__(self, nombre_db='granja.db'):
        """Conectar a base de datos (la crea si no existe)"""
        self.conexion = sqlite3.connect(nombre_db)
        self.cursor = self.conexion.cursor()
        print(f"✅ Conectado a {nombre_db}")
    
    def crear_tablas(self):
        """Crear estructura de tablas"""
        print("\n🔨 Creando tablas...")
        
        # Tabla de lotes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS lotes (
                id INTEGER PRIMARY KEY,
                numero INTEGER UNIQUE,
                raza TEXT,
                fecha_inicio TEXT,
                aves_inicial INTEGER
            )
        ''')
        
        # Tabla de producción diaria
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produccion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                lote_id INTEGER,
                huevos INTEGER,
                mortalidad INTEGER,
                saldo_aves INTEGER,
                FOREIGN KEY (lote_id) REFERENCES lotes(id)
            )
        ''')
        
        self.conexion.commit()
        print("✅ Tablas creadas: lotes, produccion")
    
    def insertar_lotes(self):
        """Insertar datos iniciales de lotes"""
        print("\n📝 Insertando lotes...")
        
        lotes_data = [
            (39, 'Hy-Line', '2023-01-15', 10000),
            (40, 'Lohmann', '2023-02-01', 10000),
            (41, 'Hy-Line', '2023-03-10', 10000),
            (42, 'Lohmann', '2023-04-05', 10000),
            (43, 'Hy-Line', '2023-05-12', 10000),
        ]
        
        for numero, raza, fecha, aves in lotes_data:
            try:
                self.cursor.execute('''
                    INSERT INTO lotes (numero, raza, fecha_inicio, aves_inicial)
                    VALUES (?, ?, ?, ?)
                ''', (numero, raza, fecha, aves))
            except sqlite3.IntegrityError:
                pass  # Lote ya existe
        
        self.conexion.commit()
        print(f"✅ {len(lotes_data)} lotes insertados")
    
    def insertar_produccion_semana(self):
        """Simular 7 días de producción para todos los lotes"""
        print("\n📊 Insertando producción semanal...")
        
        registros = 0
        for dia in range(1, 8):
            fecha = f"2024-03-{dia:02d}"
            
            for lote_numero in [39, 40, 41, 42, 43]:
                # Obtener ID del lote
                self.cursor.execute('SELECT id FROM lotes WHERE numero = ?', (lote_numero,))
                lote_id = self.cursor.fetchone()[0]
                
                # Simular datos
                huevos = random.randint(8500, 9500)
                mortalidad = random.randint(0, 5)
                saldo = 10000 - (dia * mortalidad)
                
                self.cursor.execute('''
                    INSERT INTO produccion (fecha, lote_id, huevos, mortalidad, saldo_aves)
                    VALUES (?, ?, ?, ?, ?)
                ''', (fecha, lote_id, huevos, mortalidad, saldo))
                
                registros += 1
        
        self.conexion.commit()
        print(f"✅ {registros} registros de producción insertados")
    
    def consultar_produccion_lote(self, lote_numero):
        """Consulta SQL básica"""
        print(f"\n🔍 Producción del Lote {lote_numero}:")
        
        self.cursor.execute('''
            SELECT p.fecha, p.huevos, p.mortalidad, p.saldo_aves
            FROM produccion p
            JOIN lotes l ON p.lote_id = l.id
            WHERE l.numero = ?
            ORDER BY p.fecha
        ''', (lote_numero,))
        
        resultados = self.cursor.fetchall()
        
        print(f"{'Fecha':12} | {'Huevos':>8} | {'Mortalidad':>10} | {'Saldo':>8}")
        print("-" * 50)
        
        for fecha, huevos, mort, saldo in resultados:
            print(f"{fecha:12} | {huevos:>8} | {mort:>10} | {saldo:>8}")
        
        return resultados
    
    def ranking_produccion(self):
        """Ranking de lotes por producción total"""
        print("\n🏆 RANKING DE LOTES (Semana):")
        
        self.cursor.execute('''
            SELECT 
                l.numero,
                l.raza,
                SUM(p.huevos) as total_huevos,
                AVG(p.huevos) as promedio_diario,
                SUM(p.mortalidad) as total_mortalidad
            FROM produccion p
            JOIN lotes l ON p.lote_id = l.id
            GROUP BY l.numero
            ORDER BY total_huevos DESC
        ''')
        
        resultados = self.cursor.fetchall()
        
        print(f"{'#':3} | {'Lote':6} | {'Raza':10} | {'Total':>10} | {'Prom/día':>10} | {'Muertes':>8}")
        print("-" * 65)
        
        for i, (numero, raza, total, promedio, muertes) in enumerate(resultados, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            print(f"{emoji} {i} | {numero:>6} | {raza:10} | {total:>10,} | {promedio:>10.0f} | {muertes:>8}")
    
    def lotes_con_alerta(self):
        """Lotes con mortalidad alta (>4)"""
        print("\n🚨 ALERTAS (Mortalidad >4):")
        
        self.cursor.execute('''
            SELECT 
                l.numero,
                p.fecha,
                p.mortalidad,
                p.saldo_aves
            FROM produccion p
            JOIN lotes l ON p.lote_id = l.id
            WHERE p.mortalidad > 4
            ORDER BY p.mortalidad DESC
        ''')
        
        resultados = self.cursor.fetchall()
        
        if resultados:
            for numero, fecha, mort, saldo in resultados:
                print(f"  🔴 Lote {numero} ({fecha}): {mort} muertes, quedan {saldo:,} aves")
        else:
            print("  ✅ Sin alertas")
    
    def cerrar(self):
        """Cerrar conexión"""
        self.conexion.close()
        print("\n✅ Conexión cerrada")


# ============================================
# DEMOSTRACIÓN COMPLETA
# ============================================

def demo_completa():
    """Demo de base de datos en acción"""
    
    print("\n" + "="*70)
    print("🗄️  BASE DE DATOS GRANJA AVÍCOLA")
    print("="*70)
    
    # 1. Conectar y crear
    db = BaseDatosGranja('granja.db')
    db.crear_tablas()
    
    # 2. Insertar datos
    db.insertar_lotes()
    db.insertar_produccion_semana()
    
    # 3. Consultas
    db.consultar_produccion_lote(39)
    
    input("\nPresiona ENTER para ver ranking...")
    db.ranking_produccion()
    
    input("\nPresiona ENTER para ver alertas...")
    db.lotes_con_alerta()
    
    # 4. Cerrar
    db.cerrar()
    
    print("\n" + "="*70)
    print("💾 Base de datos guardada en: granja.db")
    print("💡 Puedes abrirla con cualquier visor SQLite")
    print("="*70)


if __name__ == "__main__":
    demo_completa()