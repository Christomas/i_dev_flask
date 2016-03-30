from flask import render_template

from . import auth, forms


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template(
        'single_form.html', title='I DEV 注册', caption='请填写注册信息', form=form)
