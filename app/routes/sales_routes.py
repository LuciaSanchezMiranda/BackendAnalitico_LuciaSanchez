"""
Endpoint REST - Ventas SQL Server.
Expone el indicador de ventas totales desde SQL Server (AsiaMarket_Transactional).
"""

import logging

from flask import Blueprint, jsonify
from flasgger import swag_from
from app.services.analytics.sales_service import SalesService

sales_bp = Blueprint("sales", __name__)
service = SalesService()
logger = logging.getLogger(__name__)


@sales_bp.route("/analytics/sql/sales-total", methods=["GET"])
def sales_total():
    """
    Obtener el total de ventas desde SQL Server.
    ---
    tags:
      - 📊 Analytics - SQL Server
    summary: Ventas Totales
    description: |
      Retorna la **suma total de ventas** (`SUM(total_amount)`) de la tabla `sales`
      en la base de datos **AsiaMarket_Transactional** de SQL Server.

      ### Decisión empresarial:
      - Permite evaluar el volumen total de ingresos generados.
      - Base para comparar desempeño por período o región.
    produces:
      - application/json
    responses:
      200:
        description: Indicador de ventas totales retornado exitosamente.
        schema:
          type: object
          properties:
            indicator:
              type: string
              example: sales_total
            title:
              type: string
              example: Ventas Totales
            chart_type:
              type: string
              example: card
            data:
              type: number
              example: 6051.00
            sources:
              type: array
              items:
                type: string
              example: ["SQL Server"]
      500:
        description: Error interno al consultar las ventas.
      503:
        description: SQL Server no está disponible o falta configuración.
    """
    try:
        result = service.total_sales()
        return jsonify(result.__dict__)
    except Exception:
        logger.exception("No se pudo consultar el total de ventas")
        return jsonify({
            "status": "error",
            "message": "No se pudo consultar SQL Server; revisa la configuración y disponibilidad.",
        }), 503


@sales_bp.route("/analytics/sql/sales-by-region", methods=["GET"])
def sales_by_region():
    """Obtener el total de ventas agrupado por región.
    ---
    tags:
      - Analytics - SQL Server
    summary: Ventas por región
    description: Suma `total_amount` por región en la tabla `sales`, ordenado de mayor a menor.
    produces:
      - application/json
    responses:
      200:
        description: Totales de ventas por región.
        schema:
          type: object
          properties:
            indicator:
              type: string
              example: sales_by_region
            title:
              type: string
              example: Ventas por Región
            chart_type:
              type: string
              example: bar
            data:
              type: array
              items:
                type: object
                properties:
                  region:
                    type: string
                    example: Lima
                  value:
                    type: number
                    example: 2050.5
            sources:
              type: array
              items:
                type: string
              example: ["SQL Server"]
      503:
        description: SQL Server no está disponible o falta configuración.
    """
    try:
        result = service.sales_by_region()
        return jsonify(result.__dict__)
    except Exception:
        logger.exception("No se pudieron consultar las ventas por región")
        return jsonify({
            "status": "error",
            "message": "No se pudo consultar SQL Server; revisa la configuración y disponibilidad.",
        }), 503


@sales_bp.route("/health/sql", methods=["GET"])
def sql_connection_health():
    """Comprobar la conexión con SQL Server.
    ---
    tags:
      - Analytics - SQL Server
    summary: Estado de conexión SQL Server
    responses:
      200:
        description: Conexión disponible.
      503:
        description: SQL Server no está disponible o falta configuración.
    """
    try:
        SalesService().repository.check_connection()
        return jsonify({"status": "ok", "database": "SQL Server"}), 200
    except Exception:
        logger.exception("No se pudo comprobar la conexión con SQL Server")
        return jsonify({"status": "error", "message": "SQL Server no disponible"}), 503
