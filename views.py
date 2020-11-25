import datetime
from aiohttp import web
import aiohttp_jinja2
from helper_db import db_connect
from auth import generate_password_hash,check_password_hash
from aiohttp_session import get_session,new_session

@aiohttp_jinja2.template('index.html')
async def home(request):
    return

@aiohttp_jinja2.template('one.html')
async def one(request):
    return

@aiohttp_jinja2.template('video.html')
async def video(request):
    return

@aiohttp_jinja2.template('register.html')
async def render_register(request):
    return

@aiohttp_jinja2.template('login.html')
async def render_login(request):
    return

@aiohttp_jinja2.template('function.html')
async def func(request):
    return

async def register(request):
    if request.method == "POST":
        data = await request.post()
        assert 'firstname' in data and 'lastname' in data and 'email' in data
        try:
            async with request.app['db'].acquire() as conn:
                print(request.app['db'])
                user_exist = await conn.fetch("SELECT * FROM USERS WHERE email = $1", data['email'])
                register_error = f"User with that email already exists!"
                if user_exist:
                    return aiohttp_jinja2.render_template("login.html", request, context={'reg_error':register_error})
                pwdhash = generate_password_hash(data['plain_pass'])
                await conn.execute("INSERT INTO USERS(firstname, lastname, email,pwdhash) VALUES($1,$2,$3,$4)",
                                   data['firstname'], data['lastname'], data['email'],pwdhash)
                text = f"{data['email']} account have been created!"
                await conn.close()
                return aiohttp_jinja2.render_template("login.html", request, context= {'registred_user':text})

        except Exception as error:
            return aiohttp_jinja2.render_template("login.html", request, context={'error': error})

async def validate_login_form(request):
    if request.method == "POST":
        try:
            data = await request.post()
            assert 'email' in data and 'plain_pass' in data
            email = data['email']
            plain_pass = data['plain_pass']
            async with request.app['db'].acquire() as conn:
                user = await conn.fetch("SELECT * FROM USERS WHERE email = $1", email)

                if not user:
                    return aiohttp_jinja2.render_template("login.html", request,
                                                          context={'error': "Invalid Username or password"})
            check_password = check_password_hash(plain_pass,user[0]['pwdhash'])
            if user and check_password:
                session = await new_session(request)
                session['username'] = email
                session['last_visit'] = str(datetime.datetime.now())
                return aiohttp_jinja2.render_template("login.html", request,
                                                      context={'user': email, 'username': session['username']})
            else:
                return aiohttp_jinja2.render_template("login.html", request,
                                                  context={'error': "Invalid Username or password"})
        except Exception as error:
            return aiohttp_jinja2.render_template("login.html", request, context={'error': error})

@aiohttp_jinja2.template('sql.html')
async def list_users(request):
    con = await db_connect()
    cursor = con.cursor()
    cursor.execute("SELECT email FROM USERS")
    rows = str(cursor.fetchall())
    rows = rows.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(',', '').split()
    users = ''.join(rows).replace("'", ' ').split()
    return aiohttp_jinja2.render_template("sql.html", request, context={'users': users})

@aiohttp_jinja2.template('carou.html')
async def carousel(request):
    return

async def logout_db(request):
    session = await get_session(request)
    session["username"] = None
    session.invalidate()
    return web.HTTPFound('/')


# https://docs.aiohttp.org/en/v0.15.3/web.html#file-uploads
# @aiohttp_jinja2.template('function.html')
# async def upload(request):
#     data = await request.post()
#     filename = data['image'].filename
#     input_file = data['image'].file
#     print(input_file)
#     content = input_file.read()
#     with open(filename, 'wb') as f:
#         f.write(content)
#     return web.HTTPFound('/func')
#     path = '/static/images/'
#     file = filename
#     with open(os.path.join(path, file), 'w') as f:
#         f.write("New file created")
