"""Conexión compartida y diferida a MongoDB."""

import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

_client = None


def get_mongodb_database():
    """Return the configured MongoDB database, connecting on first use."""
    global _client

    uri = os.getenv("MONGO_URI")
    database_name = os.getenv("MONGO_DATABASE")
    missing = [
        name for name, value in (
            ("MONGO_URI", uri),
            ("MONGO_DATABASE", database_name),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Faltan variables de conexión MongoDB: " + ", ".join(missing)
        )

    if _client is None:
        timeout_ms = int(os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS", "5000"))
        _client = MongoClient(uri, serverSelectionTimeoutMS=timeout_ms)

    return _client[database_name]
