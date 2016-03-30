from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db, login_manager


# 导致愚蠢的Pycharm补全无效，放弃。想修改原文件……
# class Column(db.Column):
#     """修改默认字段属性为非空。"""
#     def __init__(self, *args, **kwargs):
#         kwargs['nullable'] = kwargs.get('nullable', False)
#         super().__init__(*args, **kwargs)
#
#
# class NullColumn(db.Column):
#     """修改默认字段属性为空。"""
#     def __init__(self, *args, **kwargs):
#         kwargs['nullable'] = kwargs.get('nullable', True)
#         super()._init_(*args, **kwargs)

Column = db.Column # 备用

class Model(db.Model):
    """通用模型类。"""
    __abstract__ = True


class User(UserMixin, Model):
    """用户模型类，继承flask_login的功能。"""
    __tablename__ = 'users'
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(64), unique=True, index=True, nullable=False)
    email = Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('原始密码被加密存储！')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
