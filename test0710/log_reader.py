# log_reader.py

'''
他のpythonファイルから、json ファイルの値を取り出すには、下記のように実行する.

# log_reader モジュールの read_log 関数を呼び出してログデータを取得
log_data = log_reader.read_log()

# ログデータを取り出す
for entry in log_data:
    print(entry)
    
'''

import os
import json
import datetime

def read_log():
    # 読み込みたいファイルを指定
    LOG_DIR = os.path.abspath("log")
    log_path = LOG_DIR + "/" + str(datetime.date.today()) + "_logger"
    i = 0
    log_file = log_path + "/" + str(i).zfill(3) + '.json'

    # 指定されたファイルが存在しない場合の処理
    if not os.path.exists(log_file):
        print("No such file.")
        return

    # ログデータの読み込み
    with open(log_file, mode='r', encoding='utf-8') as f:
        log_data = json.load(f)
        # ログデータの表示と
        for entry in log_data:
            # print(entry)
            return entry

if __name__ == "__main__":
    read_log()
