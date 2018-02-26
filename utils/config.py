# config.py
class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    MONGO_URI = 'mongodb://127.0.0.1:27017'


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = 'mongodb://127.0.0.1:27017'


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = 'mongodb://127.0.0.1:27017'
