from sql.sql_general import conn_main, cur_main
from fastapi import APIRouter, Depends
from dependencies import authenticate_admin_token

invites_router = APIRouter()


@invites_router.post('/invites/log_invite', tags=["Invites"])
def log_invite(guild_id: int, date: str, from_user_id: int, to_user_id: int, admin=Depends(authenticate_admin_token)):
    sql = "INSERT INTO INVITES (SERVER_ID, DATE, FROM_USER_ID, TO_USER_ID) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, date, from_user_id, to_user_id)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "Invite was successfully logged."


@invites_router.get('/invites/get_invites_to_user', tags=["Invites"])
def get_invites_to_user(guild_id: int, invite_to_user_id: int, admin=Depends(authenticate_admin_token)) -> list:
    sql = "SELECT * FROM INVITES WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND TO_USER_ID=%s"
    val = (guild_id, invite_to_user_id)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()

    return data


@invites_router.get('/invites/get_user_invites', tags=["Invites"])
async def get_user_invites(guild_id: int, user_id: int, admin=Depends(authenticate_admin_token)) -> list:
    sql = "SELECT * FROM INVITES WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND FROM_USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)
    invites = cur_main.fetchall()
    return invites
