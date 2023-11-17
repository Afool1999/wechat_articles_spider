# coding: utf-8
import os
from pprint import pprint
from wechatarticles import PublicAccountsWeb
from pymysql import Connection
from pymysql.converters import escape_string
import time
import multiprocessing
import random as rd
import json

rd.seed(int(time.time()))

def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        config = json.load(f)   # 加载我们的数据
    p = config['p']
    token = config['token']
    cookie = config['cookie']
    referer = config['referer']
    key_words = config['key_words']
    nicknames = config["nicknames"]
    update_freq = config["update_freq"]
    max_time = config["max_time"]
    min_time = config["min_time"]
    return p, token, cookie, referer, key_words, nicknames, update_freq, max_time, min_time

def worker_function(stop_event):
    process_id = os.getpid()
    print(f"Worker process {process_id} started.")

    p, token, cookie, referer, key_words, nicknames, update_freq, max_time, min_time = load_json('config.json')



    total_nicks = len(nicknames)
    mean_time = int(update_freq / total_nicks)
    sleep_time = min(max(int(rd.gauss(mean_time, mean_time / 3)), min_time), max_time)
    print(sleep_time)


    try:
        con = None
        con = Connection(
            host='localhost',
            port=3306,
            user='root',
            password='962464',
            database='db_wx',
            autocommit=True
        )
        cursor = con.cursor()
    except Exception as e:
        print(e)
        exit()

    paw = PublicAccountsWeb(cookie=cookie, token=token)
    error_times = 0
    while not stop_event.is_set():
        nickname_list = nicknames.copy()
        while len(nickname_list) > 0:
            nickname = nickname_list.pop()
            print(nickname)

            # change UA or not
            if rd.uniform(0, 1) > p:
                paw = PublicAccountsWeb(cookie=cookie, token=token)


            insert_data = []
            try:
                article_data = paw.get_urls(nickname, begin="0", count="5")
                for article in article_data:
                    ymd = time.localtime(article['create_time'])
                    date = "{}-{}-{}".format(ymd.tm_year, ymd.tm_mon, ymd.tm_mday)
                    insert_data.append([nickname, article['cover'], article['title'], escape_string(article['link']), article['digest'], date])
                error_times = 0
            except Exception as e:
                print(e)
                # append at back, in case of invalid token
                print("error times:", error_times, ' ' + nickname + ' placed back， sleep ', min((2 ** error_times), 4)*3600)
                nickname_list.append(nickname)
                time.sleep(min((2 ** error_times), 4) * 3600)
                error_times += 1
        
            saved = 0
            for data in insert_data:
                title = data[2]
                digest = data[4]
                save_flag = False
                for key_word in key_words:
                    if key_word in title or key_word in digest:
                        save_flag = True
                        break
                
                if save_flag:
                    try:
                        saved += 1
                        cursor.execute("insert into articles values(0, %s, %s, %s, %s, %s, %s, 0)", (*data,))
                    except Exception as e:
                        print(e)
            
            sleep_time = min(max(int(rd.gauss(mean_time, mean_time / 3)), min_time), max_time)
            print(sleep_time, saved)
            time.sleep(sleep_time)
            p, token, cookie, referer, key_words, nicknames, update_freq, max_time, min_time = load_json('config.json')



    if con:
        con.close()

if __name__ == "__main__":
    stop_event = multiprocessing.Event()

    worker_process = multiprocessing.Process(target=worker_function, args=(stop_event,))
    worker_process.start()

    try:
        # 等待用户输入 'q' 以停止程序
        while True:
            user_input = input("Press 'q' to quit: ")
            if user_input.lower() == 'q':
                # 设置 Event，通知工作进程停止
                stop_event.set()
                break
    except KeyboardInterrupt:
        # 处理 Ctrl+C 中断，设置 Event 并等待工作进程结束
        stop_event.set()
    finally:
        # 等待工作进程结束
        worker_process.join()