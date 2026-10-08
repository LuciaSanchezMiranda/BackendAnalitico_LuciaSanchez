"""Product analytics that combine SQL Server sales and MongoDB products."""

from datetime import date

from app.repositories.mongodb.product_repository import ProductRepository
from app.repositories.sqlserver.sales_repository import SalesRepository
from app.schemas.analytics_schema import IndicatorResponse


class ProductService:
    def __init__(self, sales_repository=None, product_repository=None):
        self.sales_repository = sales_repository or SalesRepository()
        self.product_repository = product_repository or ProductRepository()

    def top_product_month(self, year=None, month=None):
        today = date.today()
        year = today.year if year is None else year
        month = today.month if month is None else month

        month_start = date(year, month, 1)
        next_month_start = (
            date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
        )
        sales_data = self.sales_repository.get_top_product(
            month_start, next_month_start
        )
        if not sales_data:
            return None

        product = self.product_repository.get_product_by_id(sales_data["product_id"])
        if not product:
            return None

        data = {
            "product_id": str(sales_data["product_id"]),
            "product": product.get("name") or product.get("product_name"),
            "category": product.get("category") or product.get("category_name"),
            "quantity": sales_data["quantity"],
            "year": year,
            "month": month,
        }
        return IndicatorResponse(
            indicator="top_product_month",
            title="Producto más vendido del mes",
            chart_type="card",
            data=data,
            sources=["SQL Server", "MongoDB"],
        )
