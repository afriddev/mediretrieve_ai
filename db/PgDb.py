import asyncpg as pg
from typing import cast, Any


class PgDb:
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None
        self.asyncpg = cast(Any, pg)

    async def connect(self) -> None:
        self.pool = await self.asyncpg.create_pool(self.db_url)

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    async def get_connection(self):
        if self.pool is None:
            raise RuntimeError(
                "Connection pool is not initialized. Please call connect() first."
            )
        return self.pool.acquire()
