'''The best module.'''

import os
from tempfile import mkstemp


flask_environment = os.getenv('FLASK_ENV')

if flask_environment == 'development':
    db_path = os.getenv('DB_PATH')
    if not db_path:
        _, db_path = mkstemp()
        os.environ['DB_PATH'] = db_path
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
else:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:heihei@db-service:5432/postgres'

SQLALCHEMY_TRACK_MODIFICATIONS = True
