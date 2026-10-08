"""
Service Analítico - Ventas.
Transforma los datos obtenidos del repositorio en indicadores empresariales.
"""

from app.repositories.sqlserver.sales_repository import SalesRepository
from app.schemas.analytics_schema import IndicatorResponse


class SalesService:
    def __init__(self):
        self.repository = SalesRepository()

    def total_sales(self):
        result = self.repository.get_total_sales()
        return IndicatorResponse(
            indicator="sales_total",
            title="Ventas Totales",
            chart_type="card",
            data=result,
            sources=["SQL Server"]
        )

    def sales_by_region(self):
        rows = self.repository.get_sales_by_region()
        return IndicatorResponse(
            indicator="sales_by_region",
            title="Ventas por Región",
            chart_type="bar",
            data=[
                {"region": region, "value": round(float(total or 0), 2)}
                for region, total in rows
            ],
            sources=["SQL Server"],
        )
