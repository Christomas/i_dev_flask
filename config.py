import os

DB_NAME = 'idev'


# 基本配置
class Config:
    # 安全密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some secret phrase.'
    # 通用数据库配置
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 空的配置初始化方法
    def init_app(self):
        pass


# 开发配置
class DevelopmentConfig(Config):
    # 开启调试
    DEBUG = True
    # 开发数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_URL') + DB_NAME + '_dev'


# 测试配置
class TestingConfig(Config):
    # 开启测试
    TESTING = True
    # 测试数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_URL') + DB_NAME + '_test'


# 成品配置
class ProductionConfig(Config):
    # 成品数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('MYSQL_URL') + DB_NAME


# 可供引入的配置字典
config = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,

    # 设定默认值为开发配置
    default=DevelopmentConfig
)
