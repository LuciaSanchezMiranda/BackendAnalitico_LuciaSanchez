# BerryControl - Backend Analítico

API Flask para indicadores integrados con SQL Server y MongoDB.

## Ejecutar el backend

Configura las variables `SQL_DRIVER`, `SQL_SERVER`, `SQL_DATABASE`, `SQL_USER`,
`SQL_PASSWORD`, `MONGO_URI` y `MONGO_DATABASE` en `.env`. Para autenticación
integrada de Windows puedes usar `SQL_TRUSTED_CONNECTION=true` en lugar del
usuario y contraseña de SQL Server. No publiques el archivo `.env`.

```powershell
$env:PORT='5002'
.\venv\Scripts\python.exe -m app.main
```

Swagger: <http://127.0.0.1:5002/apidocs/>

## Indicador: producto más vendido del mes

`GET /analytics/top-product` consulta las unidades vendidas en SQL Server y
completa el nombre y la categoría desde MongoDB. Sin parámetros usa el mes y
año actuales; puedes indicar otro periodo mediante `year` y `month`.

Ejemplo con los datos disponibles en la base configurada:

```text
GET http://127.0.0.1:5002/analytics/top-product?year=2026&month=3
```

La respuesta contiene el identificador, nombre, categoría y unidades vendidas,
y declara ambas fuentes en `sources`. Swagger permite ejecutar la misma
consulta seleccionando `year=2026` y `month=3`. El conjunto SQL actual no tiene
ventas en octubre de 2026, por lo que la consulta predeterminada responde 404;
marzo de 2026 sí contiene registros.

El repositorio de productos admite tanto `products` con `product_id`, `name` y
`category` como la estructura existente `product` con `_id`, `product_name` y
`category_name`. Para el conjunto actual también adapta el código SQL `P004` al
identificador maestro MongoDB `PL-0004`.

## Guion breve para grabar el entregable

1. Muestra `sales_repository.py` para explicar el filtro del mes y la suma de
   `sales_detail.quantity`.
2. Muestra `product_repository.py` y `mongodb.py` para explicar la búsqueda del
   maestro de productos en MongoDB.
3. Muestra `product_service.py` y `product_routes.py` para seguir la integración
   y la documentación del endpoint.
4. Ejecuta el backend y abre Swagger. Ejecuta el endpoint con `year=2026` y
   `month=3`; muestra el JSON con `Raspberry Plant`, `Berries`, `quantity: 10` y
   `sources: ["SQL Server", "MongoDB"]`.
