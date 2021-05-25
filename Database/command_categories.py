from fastapi import APIRouter, Depends
from dependencies import authenticate_admin_token
from sql.sql_general import cur_main


command_categories_router = APIRouter()


@command_categories_router.get('/command_categories/get_all_guild_categories', tags=["Command categories"])
def get_all_guild_categories(guild_id: int, admin=Depends(authenticate_admin_token)):
    cur_main.execute("SELECT CATEGORY FROM COMMAND_CATEGORIES WHERE ID IN (SELECT CATEGORY_ID FROM COMMANDS WHERE ID NOT IN (SELECT COMMAND_ID FROM DISABLED_COMMANDS WHERE ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)))", (guild_id,))

    return [x[0] for x in cur_main.fetchall() if x[0]]
