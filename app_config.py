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

mqtt_params {
    "host": "",
    "port": 1883,
    "keepalive": 60,
    "username": "",
    "password": "",
}

log_level = logging.DEBUG
log_dir:str = "./_log"
