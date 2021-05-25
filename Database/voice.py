from sql.sql_general import conn_main, cur_main
from dependencies import authenticate_admin_token
from fastapi import APIRouter, Depends

voice_router = APIRouter()


@voice_router.post('/voice/add_user_voice_time', tags=['Voice'])
def add_user_voice_time(guild_id: int, user_id: int, minutes: int, admin=Depends(authenticate_admin_token)):
    sql = "INSERT INTO VOICE (SERVER_ID, USER_ID, MINUTES) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s)"
    val = (guild_id, user_id, minutes)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "User Voice Time added successfully."


@voice_router.get('/voice/get_user_voice_time', tags=['Voice'])
def get_user_voice_time(user_id: int, admin=Depends(authenticate_admin_token)) -> int:
    cur_main.execute("SELECT SUM(MINUTES) from VOICE WHERE USER_ID=%s", (user_id,))
    data = cur_main.fetchone()
    return data[0] if data and data[0] else 0
