from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config

# 定义组件对象
bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.index'


# 定义app创建函数
def create_app(config_name):
    # 初始化app配置
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化组件对象
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
