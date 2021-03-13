import os
from aiohttp import web
import aiohttp_jinja2
import jinja2
from routes import setup_routes
from aiohttp_session import get_session,session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from typing import Any, Dict

async def init_app(argv):
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates")))
    setup_routes(app)
    return app

if __name__ == '__main__':
    app = init_app(None)
    try:
        web.run_app(app)
    except Exception as error:
        raise error

