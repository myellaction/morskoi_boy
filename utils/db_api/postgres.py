import asyncpg
from data.config import DB_USER, DB_PASS, DB_NAME, DB_HOST
from asyncpg import Connection

class Database:

    def __init__(self, pool):
        self.pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(user = DB_USER, password=DB_PASS,
                                         host = DB_HOST, database = DB_NAME)
        return cls(pool)

    async def execute(self, command, *args, fetch=False,
                      fetchval=False, fetchrow=False, execute=False):

        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                return result

    async def create_table(self):
        #await self.execute('DROP TABLE IF EXISTS player', execute= True)
        await self.execute("CREATE TABLE IF NOT EXISTS player (player_id BIGINT PRIMARY KEY, full_name VARCHAR(50), "
                "username VARCHAR (50), telephone_number VARCHAR(20), avatar VARCHAR(150), "
                "game_size INTEGER, step VARCHAR(20),my_pole VARCHAR(200), pole VARCHAR(200), opponent BIGINT UNIQUE,"
                "status VARCHAR (100) DEFAULT 'off')", execute = True)

    async def get_all_users(self, user_id=None):
        if user_id:
            users = await self.execute('SELECT * FROM player WHERE player_id <> $1', user_id, fetch=True)
        else:
            users = await self.execute('SELECT * FROM player', fetch = True)
        return users

    async def create_user(self, player_id, full_name, username, telephone_number):
        user = await self.execute('INSERT INTO player (player_id, full_name, username, telephone_number) '
                           'VALUES($1, $2, $3, $4)', player_id, full_name, username, telephone_number, execute = True)
        return user

    async def avatar(self, avatar, player_id):
        user = await self.execute('UPDATE player SET avatar = $1 WHERE player_id = $2', avatar, player_id, execute = True)
        return user

    async def get_avatar(self, player_id):
        avatar = await self.execute('SELECT avatar FROM player WHERE player_id = $1', player_id, fetchrow=True)
        if not avatar:
            return False
        return avatar[0]

    async def get_user(self, player_id):
        user = await self.execute('SELECT * FROM player WHERE player_id = $1', player_id, fetchrow = True)
        return user

    async def get_opponent(self, player_id):
        opponent = await self.execute('SELECT opponent FROM player WHERE player_id = $1', player_id, fetchrow = True)
        if opponent:
            return opponent[0]
        return False

    async def set_opponent(self, player_id, opponent_id=None):
        try:
            if opponent_id:
                await self.execute('UPDATE player SET opponent = $1 WHERE player_id = $2',
                            player_id, opponent_id, execute =True)
            await self.execute('UPDATE player SET opponent = $1 WHERE player_id = $2',
                        opponent_id, player_id, execute = True)
        except:
            await self.execute('UPDATE player SET opponent = $1 WHERE opponent IN ($2, $3)',
                        None, player_id, opponent_id, execute = True)
            await self.execute('UPDATE player SET opponent = $1 WHERE player_id = $2',
                        player_id, opponent_id, execute = True)
            await self.execute('UPDATE player SET opponent = $1 WHERE player_id = $2',
                        opponent_id, player_id, execute = True)

    async def set_game_size(self, size, player_id):
        await self.execute('UPDATE player SET game_size = $1 WHERE player_id = $2',
                    size, player_id, execute = True)

    async def get_game_size(self, player_id):
        size = await self.execute('SELECT game_size FROM player WHERE player_id = $1',
                           player_id, fetchrow = True)
        if size:
            return size[0]
        return False

    async def set_pole(self, pole: str, player_id: int, opponent_id: int):
        await self.execute('UPDATE player SET pole = $1 WHERE player_id = $2',
                    pole, opponent_id, execute = True)
        await self.execute('UPDATE player SET my_pole = $1 WHERE player_id = $2',
                    pole, player_id, execute = True)

    async def get_pole_op(self, player_id):
        pole = await self.execute('SELECT pole FROM player WHERE player_id = $1',
                           player_id, fetchrow =True)
        if pole:
            return pole[0]
        return False

    async def get_pole_my(self, player_id):
        pole = await self.execute('SELECT my_pole FROM player WHERE player_id = $1',
                           player_id, fetchrow =True)
        if pole:
            return pole[0]
        return False

    async def set_status(self, player_id, status: str):
        await self.execute('UPDATE player SET status = $1 WHERE player_id = $2',
                    status, player_id, execute = True)

    async def get_status(self, player_id):
        status = await self.execute('SELECT status FROM player WHERE player_id = $1',
                             player_id, fetchval = True)
        return status

    async def set_step(self, player_id, queue):
        await self.execute('UPDATE player SET step = $1 WHERE player_id = $2',
                    queue, player_id, execute = True)


    async def get_step(self, player_id):
        step = await self.execute('SELECT step FROM player WHERE player_id = $1',
                           player_id, fetchrow = True)
        if not step:
            return step
        return step[0]

