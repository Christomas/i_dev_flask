from flask import render_template

from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('message.html', message='这个页面曾经存在，但现在却不翼而飞了……'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    print(e)
    return render_template('message.html', message='服务器离家出走了，各方加大警力搜寻中……'), 500
