from sql.sql_general import conn_main, cur_main
from dependencies import authenticate_admin_token
from fastapi import APIRouter, Depends

trashtalk_log_router = APIRouter()


@trashtalk_log_router.post('/trashtalk_log/reset_user_trashtalk', tags=['Trashtalk log'])
def reset_user_trashtalk(guild_id: int, user_id: int, admin=Depends(authenticate_admin_token)):
    sql = "DELETE FROM TRASHTALK_LOG WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND FROM_USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "User Trashtalk successfully reseted."


@trashtalk_log_router.post('/trashtalk_log/log_trashtalk', tags=['Trashtalk log'])
def log_trashtalk(guild_id: int, datum: str, from_user_id: int, to_user_id: int, admin=Depends(authenticate_admin_token)):
    sql = "INSERT INTO TRASHTALK_LOG (SERVER_ID, DATE, FROM_USER_ID, TO_USER_ID) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, datum, from_user_id, to_user_id)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "Trashtalk successfully logged."


@trashtalk_log_router.get('/trashtalk_log/get_user_trashtalk', tags=['Trashtalk log'])
def get_user_trashtalk(guild_id: int, user_id: int, admin=Depends(authenticate_admin_token)) -> list:
    sql = "SELECT * FROM TRASHTALK_LOG WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND FROM_USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()
    return data
