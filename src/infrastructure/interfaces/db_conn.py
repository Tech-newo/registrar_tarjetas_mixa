# db/base.py
from abc import ABC, abstractmethod
from supabase import Client

class DBConn(ABC):
    @abstractmethod
    def connect(self) -> Client:
        pass
