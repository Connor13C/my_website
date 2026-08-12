import datetime
import os
DEBUG = False
SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:{os.environ.get("POSTGRES_PASSWORD")}@db2:5432'
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_TOKEN_LOCATION = ['headers']
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=6)
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
CELERY_BROKER_URL = 'redis://redis2:6379'
RESULT_BACKEND = 'redis://redis2:6379'
