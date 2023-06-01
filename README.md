# Linux Version

## Requeriments 
* Kitty como Shell, debido a que se utiliza el comando 
`kitty +kitten icat image.jpg` para interpretar imágenes por consola

* Librerias en python
`psycopg2, signal, os, sys, re, time networkx, matplotlib.pyplot`

(Se recomienda leer la documentación de los terceros)

## Paso a paso para ejectuar el programa
1. Tener el servicio `PostgreSQL` corriendo por el puerto 5432

2. Cree una Base de Datos, con el nombre a su elección

3. Ejecute el comando ./test_backup.sql

4. Indique en el programa `HabitabilityBuilding.py` Su `User` y `Password` con el cual se establece la conexión a la base de datos



