from os import getenv

SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI", "postgresql://user:password@localhost:5454/app")


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

    SECRET_KEY = getenv('SECRET_KEY', 'das-ist-fantastish-privater-Schlüssel')
    PHONE = getenv('PHONE')
    API_ID = getenv('API_ID')
    DEF_USER = getenv('DEFAULT_USER')
    DEF_PASSWORD = getenv('DEFAULT_PASSWORD')
    SMS_TIMEOUT = 300


class ProductionConfig(Config):
    """"""


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
#"!/usr/bin/env bash"