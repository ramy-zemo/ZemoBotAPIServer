from sql.sql_general import conn_main, cur_main
from dependencies import authenticate_admin_token
from fastapi import APIRouter, Depends

trashtalk_router = APIRouter()


@trashtalk_router.post('/trashtalk/add_trashtalk', tags=['Trashtalk'])
def add_trashtalk(guild_id: int, added_on: str, added_by_user_id: int, message: str, admin=Depends(authenticate_admin_token)):
    sql = "INSERT INTO TRASHTALK (SERVER_ID, ADDED_ON, ADDED_BY_USER_ID, MESSAGE) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, added_on, added_by_user_id, message)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "Added trashtalk successfully."


@trashtalk_router.get('/trashtalk/get_trashtalk', tags=['Trashtalk'])
def get_trashtalk(guild_id: int, admin=Depends(authenticate_admin_token)) -> list:
    sql = "SELECT MESSAGE FROM TRASHTALK WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)"
    val = (guild_id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()

    return [entry[0] for entry in data if entry[0]]
