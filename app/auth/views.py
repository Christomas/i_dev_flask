from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user

from . import auth, forms
from .. import models, options


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    flash('您的邮箱还未验证，请检查您的收件箱进行验证。')
    return render_template('auth/unconfirmed.html')


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
            user.email, '验证您的邮箱', 'auth/mail/confirm', user=user,
            url=url_for('auth.confirm', token=token, _external=True))
        flash('注册成功，一封验证邮件已发送到您的注册邮箱，请前往验证。')
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/register.html', title='I DEV 注册', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
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
    user_id = options.load_token(token, key='confirm')
    if user_id is None or user_id != current_user.id:
        flash('链接无效或已过期！')
        return render_template('auth/unconfirmed.html')
    current_user.confirmed = True
    current_user.session.add(current_user)
    flash('您的邮箱已通过验证！')
    return redirect(request.args.get('next') or url_for('main.index'))


@auth.route('/resent_confirmation')
@login_required
def resent_confirmation():
    token = options.dump_token('reconfirm', current_user.id)
    options.send_email(
        current_user.email, '验证您的邮箱', 'auth/mail/confirm', user=current_user,
        url = url_for('auth.reconfirm', token=token, _external=True))
    flash('一封新的验证邮件已发送到您的邮箱，请前往验证。')
    return redirect(url_for('main.index'))


@auth.route('/reconfirm/<token>')
@login_required
def reconfirm(token):
    user_id = options.load_token(token, 'reconfirm')
    if user_id is None or user_id != current_user.id:
        flash('链接无效或已过期！')
        return render_template('auth/unconfirmed.html')
    current_user.confirmed = True
    current_user.session.add(current_user)
    flash('您的邮箱已通过验证。')
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录。')
    return redirect(url_for('main.index'))


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = forms.ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = options.dump_token('reset_password', user.id)
            options.send_email(
                form.email.data, '重置您的密码', 'auth/mail/reset_confirm',
                user = user, url=url_for(
                    'auth.reset_password', token=token, _external=True))
            flash('一封密码重置邮件已发送到您的邮箱，请前往查收。')
            return redirect(url_for('auth.login'))
        flash('您输入的邮箱尚未注册。')
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset_confirm/<token>', methods=['GET', 'POST'])
def reset_confirm(token):
    user_id = options.load_token(token, 'reset_password')
    if user_id is None:
        flash('链接无效或已过期！')
        return redirect(url_for('auth.login'))
    user = models.User.query.get(user_id)
    if user is None:
        flash('链接无效或已过期！')
        return redirect(url_for('auth.lgoin'))
    form = forms.ResetPasswordForm(email=user.email)
    if form.validate_on_submit():
        if user.email != form.email.data:
            flash('看起来您修改了不能改动的部分，请重新输入。')
        user.password = form.password.data
        user.session.add(user)
        flash('密码重置成功，请登录')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_confirm.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
def change_email():
    return '修改邮箱页面'


@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    return '修改密码页面'
