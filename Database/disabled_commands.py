from sql.sql_general import conn_main, cur_main
from fastapi import APIRouter, Depends
from dependencies import authenticate_admin_token


disabled_commands_router = APIRouter()


@disabled_commands_router.post('/disabled_commands/disable_command', tags=["Disabled commands"])
def disable_command(guild_id: int, command: int, admin=Depends(authenticate_admin_token)):
    cur_main.execute("SELECT ID FROM COMMANDS WHERE COMMAND=%s", (command,))
    command_in_db = cur_main.fetchone()

    if command_in_db:
        sql = "INSERT INTO DISABLED_COMMANDS (SERVER_ID, COMMAND_ID) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s)"
        val = (guild_id, command_in_db[0])

        cur_main.execute(sql, val)
        conn_main.commit()


@disabled_commands_router.post('/disabled_commands/enable_command', tags=["Disabled commands"])
def enable_command(guild_id: int, command: str, admin=Depends(authenticate_admin_token)):
    sql = "DELETE FROM DISABLED_COMMANDS WHERE COMMAND_ID=(SELECT ID FROM COMMANDS WHERE COMMAND=%s) AND SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)"
    val = (command, guild_id)

    cur_main.execute(sql, val)
    conn_main.commit()


@disabled_commands_router.get('/disabled_commands/check_command_status_for_guild', tags=["Disabled commands"])
def check_command_status_for_guild(guild_id: int, command: str, admin=Depends(authenticate_admin_token)):
    sql = "SELECT ID FROM COMMANDS WHERE COMMAND=%s"
    val = (command,)

    cur_main.execute(sql, val)
    data = cur_main.fetchone()

    if data and data[0]:
        sql_ = "SELECT * FROM DISABLED_COMMANDS WHERE COMMAND_ID=%s AND SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)"
        val_ = (command, guild_id)

        cur_main.execute(sql_, val_)
        data_ = cur_main.fetchone()
        return not data_

    else:
        return False


@disabled_commands_router.get('/disabled_commands/get_all_disabled_commands_from_guild', tags=["Disabled commands"])
def get_all_disabled_commands_from_guild(guild_id: int, admin=Depends(authenticate_admin_token)) -> list:
    cur_main.execute("SELECT COMMAND_ID FROM DISABLED_COMMANDS WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)", (guild_id,))
    command_ids = cur_main.fetchall()
    data = []

    for command_id in command_ids:
        cur_main.execute("SELECT COMMAND FROM COMMANDS WHERE ID=%s", command_id)
        data.append(cur_main.fetchone()[0])

    return data
