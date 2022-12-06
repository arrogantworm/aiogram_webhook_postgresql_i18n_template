import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def new_user(self, user_id, username):
        query = """INSERT INTO UserInfo (user_id, username) VALUES ($1, $2)
                ON CONFLICT (user_id) DO UPDATE SET username=$2"""
        await self.connector.execute(query, user_id, username)

    async def get_locale(self, user_id):
        query = """SELECT locale FROM UserInfo WHERE user_id = $1"""
        locale = await self.connector.fetchrow(query, (user_id,))
        print(locale['locale'])
        return locale['locale']

    async def set_locale(self, user_id, locale):
        query = """UPDATE UserInfo SET VALUES locale=$2 WHERE user_id = $1"""
        await self.connector.execute(user_id, locale)
