"""REST endpoints for product indicators."""

import logging

from flask import Blueprint, jsonify, request

from app.services.analytics.product_service import ProductService

products_bp = Blueprint("products", __name__)
product_service = ProductService()
logger = logging.getLogger(__name__)


@products_bp.route("/analytics/top-product", methods=["GET"])
def top_product_month():
    """Return the best-selling product for a month, combining SQL Server and MongoDB.
    ---
    tags:
      - Analytics - Products
    summary: Producto más vendido del mes
    description: |
      Obtiene desde SQL Server el producto con más unidades vendidas en el mes indicado
      y completa su nombre y categoría desde MongoDB. Si no se indican parámetros,
      consulta el mes actual. Se pueden enviar `year` y `month` para consultar otro mes.
    parameters:
      - name: year
        in: query
        type: integer
        required: false
        description: Año de la consulta (por defecto, el año actual).
        example: 2026
      - name: month
        in: query
        type: integer
        required: false
        description: Mes entre 1 y 12 (por defecto, el mes actual).
        example: 3
    produces:
      - application/json
    responses:
      200:
        description: Indicador integrado obtenido correctamente.
        schema:
          type: object
          properties:
            indicator:
              type: string
              example: top_product_month
            title:
              type: string
              example: Producto más vendido del mes
            chart_type:
              type: string
              example: card
            data:
              type: object
              properties:
                product_id:
                  type: string
                  example: P004
                product:
                  type: string
                  example: Raspberry Plant
                category:
                  type: string
                  example: Berries
                quantity:
                  type: integer
                  example: 8
                year:
                  type: integer
                  example: 2026
                month:
                  type: integer
                  example: 3
            sources:
              type: array
              items:
                type: string
              example: ["SQL Server", "MongoDB"]
      400:
        description: El año o el mes tiene un formato o valor inválido.
      404:
        description: No se encontraron ventas o datos maestros del producto en ese mes.
      503:
        description: SQL Server o MongoDB no están disponibles o no tienen configuración.
    """
    try:
        year_arg = request.args.get("year")
        month_arg = request.args.get("month")
        year = int(year_arg) if year_arg is not None else None
        month = int(month_arg) if month_arg is not None else None
        if year is not None and not 1 <= year <= 9999:
            raise ValueError("year fuera de rango")
        if month is not None and not 1 <= month <= 12:
            raise ValueError("month fuera de rango")
    except ValueError:
        return jsonify({"message": "year debe ser un año válido y month debe estar entre 1 y 12."}), 400

    try:
        result = product_service.top_product_month(year=year, month=month)
    except Exception:
        logger.exception("No se pudo obtener el producto más vendido del mes")
        return jsonify({
            "status": "error",
            "message": "No se pudo consultar SQL Server o MongoDB; revisa la configuración y disponibilidad.",
        }), 503

    if not result:
        return jsonify({"message": "No se encontró información para el mes indicado."}), 404
    return jsonify(result.__dict__)
