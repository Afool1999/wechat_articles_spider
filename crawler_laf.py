# coding: utf-8
import os
from pprint import pprint
from wechatarticles import PublicAccountsWeb, Url2Html
from pymysql import Connection
from pymysql.converters import escape_string
import time
import multiprocessing
import random as rd
import json
import requests
from qiniu import Auth, put_file, etag
import qiniu.config

rd.seed(int(time.time()))


class Laf:
    def __init__(self):
        self.s = requests.session()

    def laf_insert(self, data):
        url = "https://sn7kwx.laf.run/add_crawled_articles"
        data = {
            "gzh_name": data[0],
            "cover_url": data[1],
            "title": data[2],
            "url": data[3],
            "digest": data[4],
            "date": data[5],
            "status": 0
        }
        data = self.s.post(
            url, data=data
        )
        return data.json()

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

class Images:
    def __init__(self, save_path):
        self.save_path = save_path

    def download_img(self, url):
        """
        Parameters
        ----------
        url: str
            图片链接

        Returns
        ----------
        str: 下载图片的本地路径
        """
        # 根据链接提取图片名
        name = "{}.{}".format(url.split("/")[-2], url.split("/")[3].split("_")[-1])
        save_path = os.path.join(self.save_path, name)
        # 如果该图片已被下载，可以无需再下载，直接返回路径即可
        if os.path.isfile(save_path):
            with open(save_path, "rb") as f:
                img = f.read()
            return save_path, img

        response = requests.get(url)
        img = response.content
        with open(save_path, "wb") as f:
            f.write(img)
        return save_path, img

    def upload_img(self, path):
        #需要填写你的 Access Key 和 Secret Key
        access_key = '_RryA5cFkhI2bnofaerAurmVGczfY3Pql8skeAXr'
        secret_key = 'U1E73hzkpCQvt6I342VYReNQdPMiayJ9eq1Dkm67'
        #构建鉴权对象
        q = Auth(access_key, secret_key)
        #要上传的空间
        bucket_name = 'siyuaninfo-pic'
        #上传后保存的文件名
        key = "siyuanPics/" + path.split('/')[-1]
        #生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)
        #要上传文件的本地路径
        localfile = path
        ret, info = put_file(token, key, localfile, version='v2') 
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
        return "http://s48xwlg0x.bkt.clouddn.com/" + key

image_storage = Images('./official_images/')


def worker_function(stop_event):
    process_id = os.getpid()
    print(f"Worker process {process_id} started.")

    p, token, cookie, referer, key_words, nicknames, update_freq, max_time, min_time = load_json('config.json')



    total_nicks = len(nicknames)
    mean_time = int(update_freq / total_nicks)
    sleep_time = min(max(int(rd.gauss(mean_time, mean_time / 3)), min_time), max_time)
    print(sleep_time)


    laf = Laf()
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
                    local_path, _ = image_storage.download_img(article['cover'])
                    pico_path = image_storage.upload_img(local_path)
                    insert_data.append([nickname, pico_path, article['title'], escape_string(article['link']), article['digest'], date])
                error_times = 0
            except Exception as e:
                print(e)
                # append at back, in case of invalid token
                # print("error times:", error_times, ' ' + nickname + ' placed back, sleep ', min((2 ** error_times), 4)*3600)
                # nickname_list.append(nickname)
                # time.sleep(min((2 ** error_times), 4) * 3600)
                # error_times += 1
        
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
                        # cursor.execute("insert into articles values(0, %s, %s, %s, %s, %s, %s, 0)", (*data,))
                        laf.laf_insert(data)
                    except Exception as e:
                        print(e)
            
            sleep_time = min(max(int(rd.gauss(mean_time, mean_time / 3)), min_time), max_time)
            print(sleep_time, saved)
            time.sleep(sleep_time)
            p, token, cookie, referer, key_words, nicknames, update_freq, max_time, min_time = load_json('config.json')


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