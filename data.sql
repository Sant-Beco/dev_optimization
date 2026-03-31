-- 1. CREAR tabla
CREATE TABLE produccion (
    id INTEGER PRIMARY KEY,
    fecha TEXT,
    lote INTEGER,
    huevos INTEGER
);

-- 2. INSERTAR datos
INSERT INTO produccion VALUES (1, '2024-01-01', 39, 9500);

-- 3. CONSULTAR datos
SELECT * FROM produccion WHERE lote = 39;

-- 4. ACTUALIZAR datos
UPDATE produccion SET huevos = 9600 WHERE id = 1;