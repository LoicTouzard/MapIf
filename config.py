import os

SQLITE = 1
POSTGRE = 2
DATABASE = int(os.environ.get('DATABASE')) if os.environ.get('DATABASE') else SQLITE

POSTGRE_USER = os.environ.get('POSTGRE_USER') or 'gtfs_user'
POSTGRE_PASS = os.environ.get('POSTGRE_PASS') or 'mypass'
POSTGRE_HOST = os.environ.get('POSTGRE_HOST') or 'localhost'

SECRET_KEY = os.environ.get('SECRET_KEY') or 'coucou-hibou'

LOG_PERF = True
PRINT_PERF = True
