"""
Repository SQL Server - Ventas.
Se encarga únicamente de comunicarse con la base de datos SQL Server.
"""

from app.database.sqlserver import get_sqlserver_connection


class SalesRepository:
    def get_top_product(self, month_start, next_month_start):
        """Find the product with the most units sold during a month."""
        query = """
            SELECT TOP (1)
                sd.product_id,
                SUM(sd.quantity) AS total_quantity
            FROM sales_detail AS sd
            INNER JOIN sales AS s ON s.sale_id = sd.sale_id
            WHERE s.sale_date >= ? AND s.sale_date < ?
            GROUP BY sd.product_id
            ORDER BY SUM(sd.quantity) DESC, sd.product_id ASC
        """
        with get_sqlserver_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, month_start, next_month_start)
            result = cursor.fetchone()
            if not result:
                return None
            return {"product_id": result[0], "quantity": int(result[1])}

    def get_total_sales(self):
        query = "SELECT SUM(total_amount) FROM sales"
        with get_sqlserver_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0]

    def get_sales_by_region(self):
        query = """
            SELECT COALESCE(region, 'Sin región') AS region,
                   SUM(total_amount) AS total_sales
            FROM sales
            GROUP BY region
            ORDER BY total_sales DESC
        """
        with get_sqlserver_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def check_connection(self):
        with get_sqlserver_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            return cursor.fetchone()[0] == 1
