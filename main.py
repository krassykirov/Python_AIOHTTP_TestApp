import os
from aiohttp import web
import aiohttp_jinja2
import jinja2,fernet,base64
from routes import setup_routes
from aiohttp_session import get_session,session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from typing import Any, Dict

async def username_ctx_processor(request: web.Request) -> Dict[str, Any]:
    session = await get_session(request)
    username = session.get("username")
    return {"username": username}

async def init_app(argv):
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    app = web.Application(middlewares=[session_middleware(EncryptedCookieStorage(secret_key))])
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates")),
                         context_processors=[username_ctx_processor])
    setup_routes(app)
    return app

if __name__ == '__main__':
    app = init_app(None)
    try:
        web.run_app(app,host='localhost',port=8000)
    except Exception as error:
        raise error

