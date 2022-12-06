import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def new_user(self, user_id, username):
        query = """INSERT INTO UserInfo (user_id, username, locale) VALUES ($1, $2, $3)
                ON CONFLICT (user_id) DO UPDATE SET username=$2"""
        await self.connector.execute(query, user_id, username, 'en')
