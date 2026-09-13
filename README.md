# CURSOS-ONLINE
Programación-software

## Base de datos

Para crear las tablas y cargar los datos de prueba:

```powershell
python -m src.database.init_db
python -m src.database.seed
```

El seeder es idempotente: puede ejecutarse varias veces sin duplicar sus
registros. Carga roles, usuarios, cursos, módulos, lecciones, reseñas,
facturas, pagos, certificados, inscripciones, progresos y evaluaciones.
[Ver presentación en video del proyecto](https://drive.google.com/drive/folders/1ZEeYPr1taLtDN9tkX0QebVh41MyrmcdM?usp=drive_link)
