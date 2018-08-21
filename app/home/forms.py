"""
Created by Baobaobao123
Thank you 
"""
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
from app.models import User
__author__ = 'Baobaobao123'


class RegisterForm(FlaskForm):
    """会员注册表单"""
    name = StringField(
        label="昵称",
        validators=[
            DataRequired('请输入昵称')
        ],
        description='昵称',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称！",

        },
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码！",

        },
    )

    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入密码"),
            EqualTo('pwd', message="两次密码输入不一致")
        ],
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码！",

        },
    )

    email = StringField(
        label="邮箱",
        validators=[
            DataRequired('请输入邮箱'),
            Email("邮箱格式不正确")
        ],
        description='邮箱',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱！",

        },
    )

    phone = StringField(
        label="手机",
        validators=[
            DataRequired('请输入手机'),
            Regexp("1[3458]\\d{9}", message="手机号码不正确")
        ],
        description='手机',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机！",

        },
    )

    submit = SubmitField(
        '注册',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",

        },
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("昵称已经存在!")

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email=email).count()
        if user == 1:
            raise ValidationError("邮箱已经存在!")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user == 1:
            raise ValidationError("手机号码已经存在!")



class LoginForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired(message='')
        ],
        description='账号',
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入账号！",

        },
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码！",
        },
    )

    submit = SubmitField(
        '登陆',
        render_kw={
            "class": "btn btn-lg btn-primary btn-block",

        },
    )
