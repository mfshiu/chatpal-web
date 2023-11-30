import logging


DEBUG = True
app_ip = "0.0.0.0"
app_port = 5002

db_params = {
    'dbname': 'chatpal',
    'user': 'postgres',
    'password': '!Qazxsw2',
    'host': 'auravilla.gigoo.co',
    'port': '5432'
}

log_level = logging.DEBUG
log_dir:str = "./_log"
