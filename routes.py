import os
from azure_login import login,authorized,authenticate_client_key
from views import home,list_users,carousel,logout_db,validate_login_form,\
    render_login,register,func,video,sql_test

def setup_routes(app):
    app.router.add_static('/static', path=os.path.join(os.getcwd(), 'static'))
    app.router.add_get("/", home, name="Home")
    app.router.add_get("/users", list_users, name="users")
    app.router.add_post("/users", sql_test, name="users")
    app.router.add_get("/video", video, name="video") # to remove
    app.router.add_get("/login", login, name="login")
    app.router.add_get("/func", func, name="func")
    app.router.add_get("/images", carousel, name="carousel")
    app.router.add_get("/logout_db", logout_db, name="logout_db")
    app.router.add_post("/authorized", authorized)
    app.router.add_get("/azure-users", authenticate_client_key, name="azure-users")
    app.router.add_post("/auth", validate_login_form)
    app.router.add_get("/auth", render_login, name="render_login")
    app.router.add_post("/register", register)

