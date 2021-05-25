from sql.sql_general import conn_main, cur_main
from dependencies import authenticate_admin_token
from fastapi import APIRouter, Depends

messages_router = APIRouter()


@messages_router.post('/messages/log_message', tags=['Messages'])
def log_message(guild_id: int, date: str, user_id: int, message: str, admin=Depends(authenticate_admin_token)):
    sql = "INSERT INTO MESSAGE (SERVER_ID, DATE, USER_ID, MESSAGE) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, date, user_id, message)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "Message successfully logged"


@messages_router.get('/messages/get_user_messages', tags=['Messages'])
def get_user_messages(user_id: int, admin=Depends(authenticate_admin_token)) -> list:
    cur_main.execute("SELECT * from MESSAGE WHERE USER_ID=%s", (user_id,))
    data = cur_main.fetchall()
    return data
