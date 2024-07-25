# log_writer.py
import os
import logging
import datetime
import numpy as np
import sys
import json
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO

# ログファイルを作成
def create_logger_log_file():
    # ログディレクトリの絶対パスを取得
    LOG_DIR = os.path.abspath("log")
    # ログディレクトリが存在しない場合、作成
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # 今日の日付をもとにしたログディレクトリのパスを作成
    log_path = LOG_DIR + "/" + str(datetime.date.today()) + "_logger"
    i = 0
    while True:
        # JSONファイルのパスを作成
        log_file = log_path + "/" + str(i).zfill(3) + '.json'
        log_file_r = "/" + str(datetime.date.today()) + "_logger" + "/" + str(i).zfill(3) + '.json'
        
        # ファイルが存在する場合の処理　
        if os.path.exists(log_file):
            # 次のファイル名を試す
            print(log_file + " already exists")
            i += 1
            continue
        
        # ファイルが存在しない場合の処理
        else:
            try:
                # 空のJSONリストを作成
                with open(log_file, mode="w") as f:
                    json.dump([], f)  
                    pass
            
            # ファイルが存在しないエラーが発生した場合の処理
            except FileNotFoundError:
                # ディレクトリを作成して再試行
                os.mkdir(log_path)
                with open(log_file, mode="w") as f:
                    json.dump([], f)
                    pass
            return str(log_file), str(log_file_r)

# ログメッセージのフォーマットを定義
def log_format(message=np.nan, distance=np.nan,
               relative_altitude=np.nan, absolute_altitude=np.nan, latitude=np.nan, longitude=np.nan):
    return {
        "Timeinfo": str(datetime.datetime.now()),  
        "Level": "INFO",  
        "Message": message,  
        "Distance": distance,  
        "Relative Altitude": relative_altitude,  
        "Absolute Altitude": absolute_altitude,  
        "Latitude": latitude,  
        "Longitude": longitude  
    }

# ロガーを設定
def set_logger():
    from logging import (getLogger, StreamHandler, FileHandler, Formatter,
                         DEBUG, INFO, WARNING, ERROR)

    # INFOレベルのロガーを設定
    logger_info = getLogger("sub1")
    logger_info.setLevel(INFO)

    # DEBUGレベルのロガーを設定
    logger_debug = getLogger("sub2")
    logger_debug.setLevel(DEBUG)

    # ログのフォーマットを定義
    handler_format = Formatter('%(asctime)s.%(msecs)-3d,' +
                               ' [%(levelname)-4s],' +
                               '%(message)s',
                               datefmt='%Y-%m-%d %H:%M:%S')

    # 標準出力へのハンドラを設定
    sh = StreamHandler(sys.stdout)
    sh.setLevel(INFO)
    sh.setFormatter(handler_format)

    # ログファイルへのハンドラを設定
    log_file, log_file_r = create_logger_log_file()

    # JSONファイルにログを記録するカスタムハンドラを作成
    class JsonFileHandler(FileHandler):
        def emit(self, record):
            log_entry = self.format(record)
            log_data = json.loads(log_entry)
            with open(self.baseFilename, mode='r+', encoding='utf-8') as f:
                file_data = json.load(f)
                file_data.append(log_data)
                f.seek(0)
                json.dump(file_data, f, indent=4)

    '''
    補足：
    ハンドラが処理するログレベルは上で定義した INFOとDEBUG.
    指定したログレベル以上のログメッセージがハンドラによって処理される.
    '''
    # INFOレベルのファイルハンドラを追加
    log = JsonFileHandler(log_file, 'a', encoding='utf-8')
    log.setLevel(INFO)
    log.setFormatter(handler_format)

    # DEBUGレベルのファイルハンドラを追加
    debug = JsonFileHandler(log_file, 'a', encoding='utf-8')
    debug.setLevel(DEBUG)
    debug.setFormatter(handler_format)

    # ハンドラをロガーに追加
    logger_info.addHandler(sh)
    logger_info.addHandler(log)
    logger_debug.addHandler(debug)

    return logger_info, logger_debug, log_file_r

# ロガーを設定して取得
logger_info, logger_debug, log_file_r = set_logger()

# ログを記録
logger_info.info(log_format(message="Test", distance=10.5, relative_altitude=100, absolute_altitude=500, latitude=35.6895, longitude=139.6917))
