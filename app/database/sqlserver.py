"""
Conexión a SQL Server mediante pyodbc.
Este archivo únicamente administra la conexión entre Python y SQL Server.
"""

import os
import re
import logging
import pyodbc
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def get_sqlserver_connection():
    """Open a SQL Server connection using the environment configuration."""
    required = ("SQL_SERVER", "SQL_DATABASE")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise RuntimeError(
            "Faltan variables de conexión SQL Server: " + ", ".join(missing)
        )

    trusted_connection = os.getenv("SQL_TRUSTED_CONNECTION", "false").lower() in {
        "1", "true", "yes", "si", "sí"
    }
    configured_driver = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")
    installed_drivers = pyodbc.drivers()
    driver = configured_driver
    if driver not in installed_drivers:
        sql_drivers = [
            name for name in installed_drivers
            if re.fullmatch(r"ODBC Driver \d+ for SQL Server", name)
        ]
        if not sql_drivers:
            raise RuntimeError(
                f"El controlador SQL Server '{configured_driver}' no está instalado "
                "y no se encontró otro controlador ODBC compatible."
            )
        driver = max(sql_drivers, key=lambda name: int(re.search(r"\d+", name).group()))
        logger.warning(
            "El controlador configurado '%s' no está instalado; se usará '%s'.",
            configured_driver,
            driver,
        )

    parts = [
        f"DRIVER={{{driver}}}",
        f"SERVER={os.environ['SQL_SERVER']}",
        f"DATABASE={os.environ['SQL_DATABASE']}",
        "TrustServerCertificate=yes",
    ]

    if trusted_connection:
        parts.append("Trusted_Connection=yes")
    else:
        user = os.getenv("SQL_USER")
        password = os.getenv("SQL_PASSWORD")
        if not user or not password:
            raise RuntimeError(
                "Configura SQL_USER y SQL_PASSWORD, o activa "
                "SQL_TRUSTED_CONNECTION=true."
            )
        parts.extend((f"UID={user}", f"PWD={password}"))

    timeout = int(os.getenv("SQL_CONNECTION_TIMEOUT", "5"))
    return pyodbc.connect(";".join(parts) + ";", timeout=timeout)
