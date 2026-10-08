"""
Backend Analítico - BerryControl
Punto de entrada principal de la aplicación Flask.
"""

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
import os

from app.routes.sales_routes import sales_bp
from app.routes.product_routes import products_bp

app = Flask(__name__)

# Permitir consumo desde frontend y aplicaciones móviles
CORS(app)

app.json.ensure_ascii = False
app.json.sort_keys = False

# Swagger con flasgger - ruta por defecto /apidocs
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "BerryControl - Backend Analítico",
        "description": "API analítica orientada a la toma de decisiones empresariales. "
                       "Conecta con SQL Server (AsiaMarket_Transactional).",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {
            "name": "Analytics - SQL Server",
            "description": "Indicadores analíticos obtenidos desde SQL Server",
        },
        {
            "name": "Analytics - Products",
            "description": "Indicadores de productos integrados desde SQL Server y MongoDB",
        },
    ],
})

# Registrar Blueprints
app.register_blueprint(sales_bp)
app.register_blueprint(products_bp)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=True
    )
