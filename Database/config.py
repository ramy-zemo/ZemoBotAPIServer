from sql.sql_general import conn_main, cur_main
from dependencies import authenticate_admin_token
from fastapi import APIRouter, Depends

config_router = APIRouter()


@config_router.post('/config/activate_guild', tags=['Config'])
def activate_guild(guild_id: int, admin=Depends(authenticate_admin_token)):
    sql = "UPDATE CONFIG SET ACTIVE = TRUE WHERE GUILD_ID = %s"
    val = (guild_id,)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "Guild successfully activated"


@config_router.post('/config/deactivate_guild', tags=['Config'])
def deactivate_guild(guild_id: int, admin=Depends(authenticate_admin_token)):
    sql = "UPDATE CONFIG SET ACTIVE = FALSE WHERE GUILD_ID = %s"
    val = (guild_id,)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "Guild successfully deactivated"


@config_router.post('/config/change_prefix', tags=['Config'])
def change_prefix(guild_id: int, prefix: str, admin=Depends(authenticate_admin_token)):
    sql = "UPDATE CONFIG SET PREFIX = %s WHERE GUILD_ID = %s"
    val = (prefix, guild_id)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "Prefix successfully changed."


@config_router.post('/config/setup_config', tags=['Config'])
def setup_config(guild_id: int, main_channel_id: int, welcome_channel_id: int, admin=Depends(authenticate_admin_token)):
    sql = "INSERT INTO CONFIG (ACTIVE, GUILD_ID, LANGUAGE, PREFIX, MESSAGE_CHANNEL_ID, WELCOME_CHANNEL_ID) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (True, guild_id, "german", "$", main_channel_id, welcome_channel_id)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "Config successfully created"


@config_router.post('/config/change_msg_welcome_channel', tags=['Config'])
def change_msg_welcome_channel(guild_id: int, main_channel_id: int, welcome_channel_id: int, admin=Depends(authenticate_admin_token)):
    sql = "UPDATE CONFIG SET MESSAGE_CHANNEL_ID=%s, WELCOME_CHANNEL_ID=%s WHERE GUILD_ID=%s"
    val_1 = (main_channel_id, welcome_channel_id, guild_id)

    cur_main.execute(sql, val_1)
    conn_main.commit()

    return "Message welcome channel successfully changed."


@config_router.post('/config/update_twitch_username', tags=['Config'])
def update_twitch_username(guild_id: int, twitch_username: str, admin=Depends(authenticate_admin_token)):
    cur_main.execute('UPDATE CONFIG SET TWITCH_USERNAME = %s WHERE GUILD_ID = %s', (twitch_username, guild_id))
    conn_main.commit()

    return "Twitch username successfully updated."


@config_router.post('/config/change_auto_role', tags=['Config'])
def change_auto_role(guild_id: int, role_id: int, admin=Depends(authenticate_admin_token)):
    sql = "UPDATE CONFIG SET WELCOME_ROLE_ID = %s WHERE GUILD_ID = %s"
    val = (role_id, guild_id)

    cur_main.execute(sql, val)
    conn_main.commit()

    return "Autorole successfully changed."


@config_router.post('/config/change_welcome_message', tags=['Config'])
def change_welcome_message(guild_id: int, welcome_msg: str, admin=Depends(authenticate_admin_token)):
    sql = "UPDATE CONFIG SET WELCOME_MESSAGE=%s WHERE GUILD_ID=%s"
    val = (welcome_msg, guild_id)

    cur_main.execute(sql, val)

    conn_main.commit()

    return "Welcome Message successfully changed."


@config_router.get('/config/get_prefix', tags=['Config'])
def get_prefix(guild_id: int, admin=Depends(authenticate_admin_token)) -> int:
    sql = "SELECT PREFIX FROM CONFIG WHERE GUILD_ID=%s"
    val = (guild_id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchone()
    return data[0] if data else 0


@config_router.get('/config/check_server_status', tags=['Config'])
def check_server_status(guild_id: int, admin=Depends(authenticate_admin_token)) -> bool:
    cur_main.execute('SELECT ACTIVE FROM CONFIG WHERE GUILD_ID = %s', (guild_id,))
    data = cur_main.fetchone()

    return bool(data)


@config_router.get('/config/get_all_twitch_data', tags=['Config'])
def get_all_twitch_data(admin=Depends(authenticate_admin_token)) -> list:
    cur_main.execute('SELECT GUILD_ID, TWITCH_USERNAME FROM CONFIG')
    data = cur_main.fetchall()
    return [entry for entry in data if entry[1]]


@config_router.get('/config/get_twitch_username', tags=['Config'])
def get_twitch_username(guild_id: int, admin=Depends(authenticate_admin_token)) -> str:
    cur_main.execute('SELECT TWITCH_USERNAME FROM CONFIG WHERE GUILD_ID = %s', (guild_id,))
    data = cur_main.fetchone()
    return data[0] if data and data[0] else ""


@config_router.get('/config/get_welcome_role_id', tags=['Config'])
def get_welcome_role_id(guild_id: int, admin=Depends(authenticate_admin_token)) -> int:
    sql = "SELECT WELCOME_ROLE_ID FROM CONFIG WHERE GUILD_ID=%s"
    val = (str(guild_id),)

    cur_main.execute(sql, val)

    data = cur_main.fetchone()

    return data[0] if data else 0


@config_router.get('/config/get_welcome_role_id', tags=['Config'])
def get_welcome_role_id(guild_id: int, admin=Depends(authenticate_admin_token)):
    sql = "SELECT WELCOME_ROLE_ID FROM CONFIG WHERE GUILD_ID=%s"
    val = (guild_id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchone()

    return data[0] if data else 0


@config_router.get('/config/get_welcome_message', tags=['Config'])
def get_welcome_message(guild_id: int, admin=Depends(authenticate_admin_token)) -> str:
    sql = "SELECT WELCOME_MESSAGE FROM CONFIG WHERE GUILD_ID=%s"
    val = (guild_id,)

    cur_main.execute(sql, val)

    data = cur_main.fetchone()

    return data[0] if data and data[0] and data[0] else ""


@config_router.delete('/config/delete_all_configs', tags=['Config'])
def delete_all_configs(admin=Depends(authenticate_admin_token)):
    cur_main.execute("TRUNCATE TABLE config;")
    conn_main.commit()

    return "All configs successfully deleted."
