from sql.sql_general import conn_main, cur_main
from fastapi import APIRouter
from dependencies import authenticate_admin_token
from fastapi import Depends, Request


admin_commands_router = APIRouter()


@admin_commands_router.post('/admin_commands/create_admin_command', tags=["Admin commands"])
async def create_admin_command(command: str, parameters: str, description: str, admin=Depends(authenticate_admin_token)):
    sql = "INSERT INTO ADMIN_COMMANDS (COMMAND, PARAMETERS, DESCRIPTION) VALUES (%s, %s, %s)"
    val = (command, parameters, description)

    cur_main.execute(sql, val)
    conn_main.commit()

    return f"Successfully created Admin command {command}."


@admin_commands_router.post("/testing/{password}", tags=["A Testing"])
async def testing(password, request: Request):
    return "test"
    print(password)
    print("----------------")
    print(request.headers)
    print(await request.body())


@admin_commands_router.get('/admin_commands/get_all_admin_commands', tags=["Admin commands"])
async def get_all_admin_commands(admin=Depends(authenticate_admin_token)):
    cur_main.execute("SELECT COMMAND FROM ADMIN_COMMANDS")
    data = [commands[0] for commands in cur_main.fetchall()]

    return data


@admin_commands_router.delete('/admin_commands/delete_admin_command', tags=["Admin commands"])
async def delete_admin_command(command: str, admin=Depends(authenticate_admin_token)):
    sql = "DELETE FROM ADMIN_COMMANDS WHERE COMMAND=%s"
    val = (command,)

    cur_main.execute(sql, val)
    conn_main.commit()

    return f"Successfully deleted Admin command {command}."
