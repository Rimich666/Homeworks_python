from os import getenv

SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI", "postgresql://user:password@localhost:5454/app")


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SECRET_KEY = getenv('SECRET_KEY', 'das-ist-fantastish-privater-Schlüssel')
    PHONE = getenv('PHONE', '79272117466')
    API_ID = getenv('API_ID', "ADBBA8A6-5136-9B60-F45A-AD869ACD9BE8")


class ProductionConfig(Config):
    """"""


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
#"!/usr/bin/env bash"