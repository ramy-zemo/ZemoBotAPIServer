from sql.sql_general import conn_main, cur_main
from fastapi import APIRouter, Depends
from dependencies import authenticate_admin_token

level_router = APIRouter()


@level_router.post('/level/add_user_xp', tags=['Level'])
def add_user_xp(guild_id: int, user_id: int, xp: int, override_current_xp: bool = False, admin=Depends(authenticate_admin_token)):
    sql = "SELECT xp FROM LEVEL WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)

    if cur_main.fetchall():
        if override_current_xp:
            cur_main.execute(
                "UPDATE LEVEL SET XP=%s WHERE USER_ID=%s AND SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)",
                (xp, user_id, guild_id))

        else:
            cur_main.execute(
                "UPDATE LEVEL SET XP=(XP + %s) WHERE USER_ID=%s AND SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)",
                (xp, user_id, guild_id))
    else:
        sql = "INSERT INTO LEVEL (SERVER_ID, USER_ID, XP) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s)"
        val = (guild_id, user_id, xp)

        cur_main.execute(sql, val)

    conn_main.commit()

    return "XP successfully added."


@level_router.get('/level/get_server_ranks', tags=['Level'])
def get_server_ranks(guild_id: int, admin=Depends(authenticate_admin_token)) -> list:
    sql = "SELECT (SELECT GUILD_ID FROM CONFIG WHERE ID=SERVER_ID), USER_ID, XP FROM LEVEL WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) ORDER BY XP DESC"
    val = (guild_id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()

    return data


@level_router.get('/level/get_xp_from_user', tags=['Level'])
def get_xp_from_user(guild_id: int, user_id: int, admin=Depends(authenticate_admin_token)) -> int:
    sql = "SELECT XP FROM LEVEL WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND USER_ID=%s"
    val = (guild_id, user_id)
    cur_main.execute(sql, val)
    data = cur_main.fetchone()

    return data[0] if data else 0
