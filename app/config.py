import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Базовий клас конфігурації."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-fallback-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    """Конфігурація для розробки."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '../instance/data.sqlite') # Шлях до instance/data.sqlite

class TestingConfig(Config):
    """Конфігурація для тестування."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False # Вимикаємо CSRF (для тестів)

class ProductionConfig(Config):
    """Конфігурація для продакшену."""
    DEBUG = False
    TESTING = False
    pass

config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}