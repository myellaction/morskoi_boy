import sqlite3 as sq

async def db_connect():
    global db, cur
    db = sq.connect('morskoy_boy.db')
    cur = db.cursor()
    #cur.execute('DROP TABLE IF EXISTS player ')
    cur.execute('CREATE TABLE IF NOT EXISTS player (player_id INTEGER PRIMARY KEY, full_name VARCHAR(50), '
                'username VARCHAR (50), telephone_number VARCHAR(20), avatar VARCHAR(150), '
                'game_size INTEGER, step VARCHAR(20),my_pole VARCHAR(200), pole VARCHAR(200), opponent INTEGER UNIQUE,'
                'status VARCHAR (100) DEFAULT off)')

    db.commit()

async def get_all_users(player_id=None):
    if player_id:
        users = cur.execute('SELECT * FROM player WHERE player_id <> ?', (player_id,)).fetchall()
        return users
    users = cur.execute('SELECT * FROM player').fetchall()
    return users

async def create_user(player_id, full_name, username, telephone_number):
    user = cur.execute('INSERT INTO player (player_id, full_name, username, telephone_number) '
                       'VALUES(?, ?, ?, ?)', (player_id, full_name, username, telephone_number))
    db.commit()
    return user

async def avatar(avatar, player_id):
    user = cur.execute('UPDATE player SET avatar = ? WHERE player_id = ?', (avatar, player_id))
    db.commit()
    return user

async def get_avatar(player_id):
    avatar = cur.execute('SELECT avatar FROM player WHERE player_id = ?', (player_id,)).fetchone()
    if not avatar:
        return False
    return avatar[0]

async def get_user(player_id):
    user = cur.execute('SELECT * FROM player WHERE player_id = ?', (player_id,)).fetchone()
    return user

async def get_opponent(player_id):
    opponent = cur.execute('SELECT opponent FROM player WHERE player_id = ?', (player_id,)).fetchone()
    if opponent:
        return opponent[0]
    return False

async def set_opponent(player_id, opponent_id=None):
    try:
        if opponent_id:
            cur.execute('UPDATE player SET opponent = ? WHERE player_id = ?',
                           (player_id, opponent_id))
        cur.execute('UPDATE player SET opponent = ? WHERE player_id = ?',
                           (opponent_id, player_id))
        db.commit()
    except:
        cur.execute('UPDATE player SET opponent = ? WHERE opponent IN (?, ?)',
                    (None, player_id, opponent_id))
        cur.execute('UPDATE player SET opponent = ? WHERE player_id = ?',
                           (player_id, opponent_id))
        cur.execute('UPDATE player SET opponent = ? WHERE player_id = ?',
                           (opponent_id, player_id))
        db.commit()



async def set_game_size(size, player_id):
    cur.execute('UPDATE player SET game_size = ? WHERE player_id = ?',
                (size, player_id))
    db.commit()

async def get_game_size(player_id):
    size = cur.execute('SELECT game_size FROM player WHERE player_id = ?',
                (player_id,)).fetchone()
    if size:
        return size[0]
    return False


async def set_pole(pole:str, player_id: int, opponent_id:int):
    cur.execute('UPDATE player SET pole = ? WHERE player_id = ?',
                       (pole, opponent_id))
    cur.execute('UPDATE player SET my_pole = ? WHERE player_id = ?',
                (pole, player_id))
    db.commit()


async def get_pole_op(player_id):
    pole = cur.execute('SELECT pole FROM player WHERE player_id = ?',
                       (player_id,)).fetchone()
    if pole:
        return pole[0]
    return False

async def get_pole_my(player_id):
    pole = cur.execute('SELECT my_pole FROM player WHERE player_id = ?',
                       (player_id,)).fetchone()
    if pole:
        return pole[0]
    return False

async def set_status(player_id, status: str):
    cur.execute('UPDATE player SET status = ? WHERE player_id = ?',
                (status, player_id))
    db.commit()

async def get_status(player_id):
    status = cur.execute('SELECT status FROM player WHERE player_id = ?',
                (player_id,)).fetchone()
    return status[0]

async def set_step(player_id, queue):
    cur.execute('UPDATE player SET step = ? WHERE player_id = ?',
                (queue, player_id))
    db.commit()

async def get_step(player_id):
    step = cur.execute('SELECT step FROM player WHERE player_id = ?',
                       (player_id,)).fetchone()
    if not step:
        return step
    return step[0]
