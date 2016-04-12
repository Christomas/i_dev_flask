from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user

from . import auth, forms
from .. import models, options


# @auth.route(
#     '/send_confirmation/<user>/<key>/<subject>/<msg>/<confirm>/<redirect>')
# def send_confirmation(user, key, subject, msg, confirm, redirect):
#     token = options.dump_token(key, user.id)
#     options.send_email(user.email, subject, 'auth/mail/confirm', user=user,
#                        url=url_for(confirm, token=token, _external=True))
#     flash(msg)
#     return redirect(url_for(redirect))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        flash('您的邮箱还未验证，请检查您的收件箱进行验证。')
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
@auth.route('/unconfirmed/<resend>')
@login_required
def unconfirmed(resend=None):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if resend:
        token = options.dump_token('reconfirm', current_user.id)
        options.send_email(
            current_user.email, '验证邮箱', 'auth/mail/confirm', user=current_user,
            url=url_for('auth.reconfirm', token=token, _external=True))
        flash('一封新的验证邮件已发送到您的邮箱，请前往验证。')
    return render_template(
        'auth/unconfirmed.html',
        url=url_for('auth.unconfirmed', resend=True))


@auth.route('/reconfirm/<token>')
@login_required
def reconfirm(token):
    if current_user.confirmed:
        flash('您的邮箱已通过验证。')
        return redirect(url_for('main.index'))
    user_id = options.load_token(token, 'reconfirm')
    if user_id == current_user.id:
        current_user.confirmed = True
        current_user.session.add(current_user)
        flash('您的邮箱已通过验证。')
        return redirect(url_for('main.index'))
    flash('链接无效或已过期。')
    return redirect(url_for('auth.unconfirmed'))


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
            user.email, '验证邮箱', 'auth/mail/confirm', user=user,
            url=url_for('auth.confirm', token=token, _external=True))
        flash('注册成功，一封验证邮件已发送到您的注册邮箱，请前往验证。')
        return redirect(url_for('auth.unconfirmed'))
    return render_template(
        'auth/register.html', form=form)


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
    return render_template('auth/login.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    user_id = options.load_token(token, key='confirm')
    if user_id != current_user.id:
        flash('链接无效或已过期！')
        return redirect(url_for('auth.unconfirmed'))
    current_user.confirmed = True
    current_user.session.add(current_user)
    flash('您的邮箱已通过验证！')
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
                user.email, '重置密码', 'auth/mail/reset_password', user=user,
                url=url_for('auth.reset_confirm', token=token, _external=True))
            flash('一封密码重置邮件已发送到您的邮箱，请前往查收。')
            return redirect(url_for('auth.login'))
        flash('您输入的邮箱尚未注册。')
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset_confirm/<token>', methods=['GET', 'POST'])
def reset_confirm(token):
    user_id = options.load_token(token, 'reset_password')
    if user_id is None:
        flash('链接无效或已过期！请再次点击重置密码，将重新发送邮件。')
        return redirect(url_for('auth.login'))
    user = models.User.query.get(user_id)
    if user is None:
        flash('链接无效或已过期！请再次点击重置密码，将重新发送邮件。')
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


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = forms.ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            current_user.password = form.new_password.data
            current_user.session.add(current_user)
            logout_user()
            flash('密码修改成功，请重新登录。')
            return redirect(url_for('auth.login'))
        flash('原密码输入错误！')
    return render_template('auth/change_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    form = forms.ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            current_user.email = form.email.data
            current_user.confirmed = False
            current_user.session.add(current_user)
            token = options.dump_token('change_mail', current_user.id)
            options.send_email(
                current_user.email, '验证邮箱', 'auth/mail/confirm',
                user=current_user,
                url=url_for('auth.new_confirm', token=token, _external=True))
            flash('邮箱修改成功，一封新验证邮件已发送到您的新邮箱。')
            return redirect(url_for('auth.unconfirmed'))
        flash('密码错误！')
    return render_template('auth/change_email.html', form=form)


@auth.route('/confirm_new_email/<token>')
@login_required
def new_confirm(token):
    user_id = options.load_token(token, 'change_email')
    if user_id is None or user_id != current_user.id:
        flash('链接无效或已过期！')
        return redirect(url_for('auth.unconfirmed'))
    flash('您的新邮箱已经通过验证。')
    return redirect(url_for('main.index'))
