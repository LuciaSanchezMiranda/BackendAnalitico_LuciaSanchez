"""
Schema de respuesta analítica estándar.
Define la estructura de datos que retorna la API al frontend.
"""

from dataclasses import dataclass
from typing import Any, List


@dataclass
class IndicatorResponse:
    """Estructura estándar para indicadores analíticos
    consumidos por el frontend."""
    indicator: str
    title: str
    chart_type: str
    data: Any
    sources: List[str]
