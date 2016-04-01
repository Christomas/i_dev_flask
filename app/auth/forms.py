from flask_wtf import Form

from wtforms import(
    StringField, PasswordField, SubmitField, BooleanField)
from wtforms.validators import(
    ValidationError, DataRequired, Length, Email, Regexp, EqualTo)

from ..models import User


class RegisterForm(Form):
    username = StringField(
        '用户名：', validators=[
            DataRequired(), Length(1, 64, message='用户名最多可以有64个字符或21个汉字。'),
            Regexp(r'^\w+$', message='用户名只能由字母、数字、下划线或汉字组成。')])
    email = StringField(
        '邮箱：', validators=[
            DataRequired(), Length(1, 64), Email(message='请输入有效的邮箱地址。')])
    password = PasswordField(
        '密码：', validators=[
            DataRequired(), EqualTo('password2', message='输入的两次密码不一致。')])
    password2 = PasswordField('确认密码：', validators=[DataRequired()])
    submit = SubmitField('提交注册信息')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用。')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经被注册。')


class LoginForm(Form):
    email = StringField(
        '邮箱：', validators=[
            DataRequired(), Length(1, 64), Email(message='请输入有效的邮箱地址。')])
    password = PasswordField('密码：', validators=[DataRequired()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')


class ResetPasswordRequestForm(Form):
    email = StringField(
        '邮箱', validators=[
            DataRequired(), Length(1, 64), Email(message='请输入有效的邮箱地址。')])
    submit = SubmitField('提交')


class ResetPasswordForm(Form):
    email = StringField(
        '邮箱：', validators=[
            DataRequired(), Length(1, 64), Email(message='请输入有效的邮箱地址')],
        render_kw=dict(readonly=True))
    password = PasswordField(
        '新密码：', validators=[
            DataRequired(), EqualTo('password2', message='输入的两次密码不一致。')])
    password2 = PasswordField('确认新密码：', validators=[DataRequired()])
    submit = SubmitField('确认变更密码')
