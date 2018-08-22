"""
Created by Baobaobao123
Thank you 
"""
import datetime
import os

from werkzeug.utils import secure_filename

from app import db, app
from app.home.forms import RegisterForm, LoginForm, UserdetailForm
from . import home
from flask import render_template, redirect, url_for, flash, session, request
from app.models import User, Userlog
from werkzeug.security import generate_password_hash
from functools import wraps
import uuid
__author__ = 'Baobaobao123'


# 登陆装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@home.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user is None:
            flash("用户不存在", "err")
            return redirect(url_for("home.login"))
        if not user.check_pwd(data["pwd"]):
            flash("密码错误", "err")
            return redirect(url_for("home.login"))
        session["user"] = user.name
        session["user_id"] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template("home/login.html", form=form)


@home.route("/logout/")
def logout():
    session.pop("user", None)
    session.pop("user.id", None)
    return redirect(url_for("home.login"))

#会员注册
@home.route("/regist/", methods=["GET", "POST"])
def regist():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            pwd=generate_password_hash(data["pwd"]),
            uuid=uuid.uuid4().hex,
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功", "ok")
    else:
        flash("注册失败", "err")
    return render_template("home/regist.html", form=form)

# 会员修改资料
@home.route("/user/", methods=["GET", "POST"])
@user_login_req
def user():
    form = UserdetailForm()
    user = User.query.get(int(session["user_id"]))
    form.face.validators = []
    if request.method == "GET":
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form
        if form.validate_on_submit():
            data = form.data
            name_count = User.query.filter_by(name=data["name"]).count()
            if data["name"] != user.name and name_count == 1:
                flash("昵称已经存在", 'err')
                return redirect(url_for("home.user"))

            email_count = User.query.filter_by(email=data["email"]).count()
            if data["email"] != user.email and email_count == 1:
                flash("邮箱已经存在", 'err')
                return redirect(url_for("home.user"))

            phone_count = User.query.filter_by(phone=data["phone"]).count()
            if data["phone"] != user.phone and phone_count == 1:
                flash("手机号码已经存在", 'err')
                return redirect(url_for("home.user"))

            user.name = data["name"]
            user.email = data["email"]
            user.phone = data["phone"]
            user.info = data["info"]
            db.session.add(user)
            db.session.commit()
            flash("修改成功", "ok")

            file_face = secure_filename(form.face.data.filename)  # 为什么同样的logo可以调用filename
            if not os.path.exists(app.config["FC_DIR"]):
                os.makedirs(app.config["FC_DIR"])
                os.chmod(app.config["FC_DIR"], "rw")
            user.face = change_filename(file_face)
            form.face.data.save(app.config["FC_DIR"] + user.face)
            return redirect(url_for("home.user"))
    return render_template("home/user.html", form=form, user=user)

@home.route("/pwd/")
@user_login_req
def pwd():
    return render_template("home/pwd.html")


@home.route("/comments/")
@user_login_req
def comments():
    return render_template("home/comments.html")


@home.route("/loginlog/")
@user_login_req
def loginlog():
    return render_template("home/loginlog.html")


@home.route("/moviecol/")
@user_login_req
def moviecol():
    return render_template("home/moviecol.html")


@home.route("/")
def index():
    return render_template("home/index.html")


@home.route("/animation/")
def animation():
    return render_template("home/animation.html")


@home.route("/search/")
def search():
    return render_template("home/search.html")


@home.route("/play/")
def play():
    return render_template("home/play.html")


