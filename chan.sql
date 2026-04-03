-- Tu SQL aquí:
SELECT 
    l.raza,
    SUM(p.huevos) AS total
FROM produccion p
JOIN lotes l ON p.lote_id = l.id
GROUP BY l.raza
ORDER BY total ASC
LIMIT 1;

-- Resultado: Hy-Line, 28,280