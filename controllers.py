from fastapi import FastAPI, Depends, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from auth import auth

import db
from models import User, Task
from mycalendar import MyCalendar
from datetime import datetime, timedelta

import re

pattern = re.compile(r"\w{4,20}")
pattern_pw = re.compile(r"\w{6,20}")
pattern_mail = re.compile(r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")

app = FastAPI(
    title="FastAPIでつくるtoDoアプリケーション",
    description="FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．",
    version="0.9 beta",
)
security = HTTPBasic()

templates = Jinja2Templates(directory="templates")
jinja_env = templates.env


def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def admin(request: Request, credentials: HTTPBasicCredentials = Depends(security)):

    username = auth(credentials)

    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    db.session.close()

    today = datetime.now()
    next_w = today + timedelta(days=7)

    cal_prev = MyCalendar(
        username, {t.deadline.strftime("%Y%m%d"): t.done for t in task}
    ).formatyear(today.year - 1, 4)
    cal_now = MyCalendar(
        username, {t.deadline.strftime("%Y%m%d"): t.done for t in task}
    ).formatyear(today.year, 4)
    cal_next = MyCalendar(
        username, {t.deadline.strftime("%Y%m%d"): t.done for t in task}
    ).formatyear(today.year + 1, 4)

    task_all = [t for t in task]
    links = [t.deadline.strftime("/todo/" + username + "/%Y/%m/%d") for t in task_all]
    task = [t for t in task if today <= t.deadline <= next_w]

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "user": user,
            "task_all": task_all,
            "task": task,
            "links": links,
            "calender_prev": cal_prev,
            "calender_now": cal_now,
            "calender_next": cal_next,
        },
    )


async def register(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse(
            "register.html", {"request": request, "username": "", "error": []}
        )

    if request.method == "POST":
        data = await request.form()
        username = data.get("username")
        password = data.get("password")
        password_tmp = data.get("password_tmp")
        mail = data.get("mail")

        error = []

        tmp_user = db.session.query(User).filter(User.username == username).first()

        if tmp_user is not None:
            error.append("同じユーザ名のユーザが存在します。")
        if password != password_tmp:
            error.append("入力したパスワードが一致しません。")
        if pattern.match(username) is None:
            error.append("ユーザ名は4~20文字の半角英数字にしてください。")
        if pattern_pw.match(password) is None:
            error.append("パスワードは6~20文字の半角英数字にしてください。")
        if pattern_mail.match(mail) is None:
            error.append("正しくメールアドレスを入力してください。")

        if error:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "username": username, "error": error},
            )

        user = User(username, password, mail)
        db.session.add(user)
        db.session.commit()
        db.session.close()

        return templates.TemplateResponse(
            "complete.html", {"request": request, "username": username}
        )


def detail(
    request: Request,
    username,
    year,
    month,
    day,
    credentials: HTTPBasicCredentials = Depends(security),
):
    username_tmp = auth(credentials)

    if username_tmp != username:
        return RedirectResponse("/")

    """ ここから追記 """
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()
    db.session.close()

    theday = "{}{}{}".format(year, month.zfill(2), day.zfill(2))
    task = [t for t in task if t.deadline.strftime("%Y%m%d") == theday]

    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "username": username,
            "task": task,
            "year": year,
            "month": month,
            "day": day,
        },
    )


async def done(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    username = auth(credentials)
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()

    data = await request.form()
    t_dones = data.getlist("done[]")

    for t in task:
        if str(t.id) in t_dones:
            t.done = True

    db.session.commit()
    db.session.close()

    return RedirectResponse("/admin")


async def add(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    username = auth(credentials)
    user = db.session.query(User).filter(User.username == username).first()

    data = await request.form()
    year = int(data["year"])
    month = int(data["month"])
    day = int(data["day"])
    hour = int(data["hour"])
    minute = int(data["minute"])

    deadline = datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    task = Task(user.id, data["content"], deadline)
    db.session.add(task)
    db.session.commit()
    db.session.close()

    return RedirectResponse("/admin")


def delete(
    request: Request, t_id, credentials: HTTPBasicCredentials = Depends(security)
):
    username = auth(credentials)
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.id == t_id).first()

    if task.user_id != user.id:
        return RedirectResponse("/admin")

    db.session.delete(task)
    db.session.commit()
    db.session.close()

    return RedirectResponse("/admin")


def get(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    username = auth(credentials)
    user = db.session.query(User).filter(User.username == username).first()
    task = db.session.query(Task).filter(Task.user_id == user.id).all()

    db.session.close()

    task = [
        {
            "id": t.id,
            "content": t.content,
            "deadline": t.deadline.strftime("%Y-%m-%d %H:%M:%S"),
            "published": t.date.strftime("%Y-%m-%d %H:%M:%S"),
            "done": t.done,
        }
        for t in task
    ]

    return task


async def insert(
    request: Request,
    content: str = Form(...),
    deadline: str = Form(...),
    credentials: HTTPBasicCredentials = Depends(security),
):
    username = auth(credentials)
    user = db.session.query(User).filter(User.username == username).first()
    task = Task(user.id, content, datetime.strptime(deadline, "%Y-%m-%d_%H:%M:%S"))

    db.session.add(task)
    db.session.commit()

    task = db.session.query(Task).all()[-1]
    db.session.close()

    return {
        "id": task.id,
        "content": task.content,
        "deadline": task.deadline.strftime("%Y-%m-%d %H:%M:%S"),
        "published": task.date.strftime("%Y-%m-%d %H:%M:%S"),
        "done": task.done,
    }
