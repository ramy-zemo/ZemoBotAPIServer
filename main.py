import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.openapi.utils import get_openapi
from User import User
from dotenv import load_dotenv
from config import ICON_URL
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html

from Database.admin_commands import admin_commands_router
from Database.command_categories import command_categories_router
from Database.commands import commands_router
from Database.config import config_router
from Database.disabled_commands import disabled_commands_router
from Database.invites import invites_router
from Database.level import level_router
from Database.message import messages_router
from Database.trashtalk import trashtalk_router
from Database.trashtalk_log import trashtalk_log_router
from Database.voice import voice_router

app = FastAPI(docs_url=None, redoc_url=None, title="ZemoBot API")
app.mount('/static', StaticFiles(directory="static"), name="static")

load_dotenv()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title='ZemoBot API',
        version='0.0.1',
        description='This is an API for using the services of the ZemoBot',
        routes=app.routes
    )
    openapi_schema['info']['x-logo'] = {
        'url': ICON_URL
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redocc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


app.openapi = custom_openapi
app.include_router(User.router)

app.include_router(admin_commands_router)
app.include_router(command_categories_router)
app.include_router(commands_router)
app.include_router(disabled_commands_router)
app.include_router(invites_router)
app.include_router(level_router)
app.include_router(messages_router)
app.include_router(config_router)
app.include_router(trashtalk_router)
app.include_router(trashtalk_log_router)
app.include_router(voice_router)


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['User.User']},
    generate_schemas=True,
    add_exception_handlers=True
)

if __name__ == '__main__':
    os.system('uvicorn main:app --reload')
