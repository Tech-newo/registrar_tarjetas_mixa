# db/supabase_conn.py
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from infrastructure.interfaces import DBConn

class SupabaseConn(DBConn):
    _instance = None  # Variable de clase para el Singleton
    _client: Client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseConn, cls).__new__(cls)
        return cls._instance

    def connect(self) -> Client:
        if self._client is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

            if not url or not key:
                raise ValueError("Faltan variables de entorno SUPABASE_URL o SUPABASE_KEY")

            self._client = create_client(
                url,
                key,
                options=ClientOptions(
                    postgrest_client_timeout=100,
                    storage_client_timeout=100,
                    schema="public",
                )
            )
        return self._client
