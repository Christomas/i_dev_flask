import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db, models

# 初始化app及管理组件
app = create_app(os.getenv('FLASK_CONFIG', 'default'))
manager = Manager(app)
migrate = Migrate(app, db)


# 自定义shell上下文
def make_shell_context():
    return dict(app=app, db=db, models=models)

# 将自定义上下文自动引入shell命令
manager.add_command('shell', Shell(make_context=make_shell_context))
# 设定数据库迁移命令为db
manager.add_command('db', MigrateCommand)


# 定义test命令
@manager.command
def test():
    """进行单元测试"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
