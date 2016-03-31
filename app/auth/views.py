from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user

from . import auth, forms
from .. import models, options


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        user = models.User()
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        user.session.add(user)
        user.session.commit()
        token = options.dump_token('confirm', user.id)
        options.send_email(
            user.email, '验证您的邮箱', 'auth/mail/confirm',
            user=user, token=token)
        flash('注册成功，一封验证邮件已发送到您的注册邮箱，请前往验证。')
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/register.html', title='I DEV 注册', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('您已登录。')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('该邮箱未注册或密码错误！')
    return render_template('auth/login.html', title='I DEV 登录', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    return '验证页面'


@auth.route('/reconfirm', methods=['GET', 'POST'])
@login_required
def reconfirm():
    return '重新发送验证码页面'


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录。')
    return redirect(url_for('main.index'))
