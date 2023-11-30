import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path

from flask import request
import psycopg2

import app_config



######################
# Logging Operation #
######################


__log_init = False
__logger:Logger = logging.getLogger('auravilla_admin')


def ensure_directory(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        __logger.info(f"Directory '{dir_path}' created successfully.")


def _init_logging(log_dir:str, log_level=logging.DEBUG):
    formatter = logging.Formatter(
        '%(levelname)1.1s %(asctime)s %(module)15s:%(lineno)03d %(funcName)15s) %(message)s',
        datefmt='%H:%M:%S')
    
    ensure_directory(log_dir)
    # Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = os.path.join(log_dir, "auravilla_admin.log")
    file_handler = TimedRotatingFileHandler(log_path, when="d")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger("auravilla_admin")
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)    
    logger.setLevel(log_level)

    return logger


def get_logger():
    global __log_init
    global __logger
    if not __log_init:
        __logger = _init_logging(log_dir=app_config.log_dir, log_level=app_config.log_level)
        __log_init = True
        
    return __logger



######################
# Database Operation #
######################


def create_connection():
    try:
        conn = psycopg2.connect(**app_config.db_params)
        return conn
    except psycopg2.Error as ex:
        __logger.exception(ex)
        return None


def execute_command(command, params):
    __logger.debug(f"command: {command}\nparams:{params}")

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(command, params)
        conn.commit()
    except Exception as ex:
        __logger.exception(ex)
    finally:
        if conn:
            cursor.close()
            conn.close()


def insert_and_fetch_id(command, params):
    # __logger.debug(f"command: {command}\nparams:{params}")
    identity_id = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(command, params)
        conn.commit()
        identity_id = cursor.fetchone()[0]
    except Exception as ex:
        __logger.exception(ex)
    finally:
        if conn:
            cursor.close()
            conn.close()

    return identity_id


# command_params: [(command, params), (command, params)...]
def execute_commands(command_params:list):
    # logger.debug(f"command_params: {command_params}")
    try:
        conn = create_connection()
        cursor = conn.cursor()
        for pair in command_params:
            command, params = pair[0], pair[1]
            # print(f"command: {command}, params: {params}")
            cursor.execute(command, params)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        __logger.exception(ex)
    finally:
        if conn:
            cursor.close()
            conn.close()
  

def execute_query(query, params):
    conn = create_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
    except Exception as ex:
        __logger.exception(ex)
        rows = []
    finally:
        cursor.close()
        conn.close()
        
    return rows
  

def execute_query_as_dict_list(query, params=None):
    conn = create_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()

        col_names = [desc[0] for desc in cur.description]
        data_as_dict_list = []
        for row in rows:
            data_as_dict_list.append({col_names[i]: row[i] for i in range(len(col_names))})
            
    except Exception as ex:
        __logger.exception(ex)
        data_as_dict_list = []
        
    finally:
        cur.close()
        conn.close()
        
    return data_as_dict_list



######################
#  Domain Operation  #
######################


# def is_human_voice() -> bool:
#     import librosa
#     import numpy as np
#     from sklearn.ensemble import RandomForestClassifier  # Example classifier
    
#     def extract_features(audio_path):
#         y, sr = librosa.load(audio_path)
#         mfccs = librosa.feature.mfcc(y=y, sr=sr)
#         return np.mean(mfccs.T,axis=0)


def parse_int(value_str:str, default_value=None):
    value = default_value
    if value_str:
        try:
            value_int = int(value_str)
            value = value_int
        except ValueError:
            pass
    
    return value
    