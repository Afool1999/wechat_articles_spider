from pymysql import Connection
from get_parameters import main
from wechatarticles import AccountBiz
from wechatarticles import ArticlesInfo
from wechatarticles.utils import get_history_urls, verify_url
from pprint import pprint
from proxy import start_proxy, close_proxy
import pandas as pd

import json
import os
import random
import time

nickname_lst = ["萤人聚集地"]
cookie = ""
method = 'qingbo'
AUTO_PARAMS = True

def save_xlsx(fj, lst):
    df = pd.DataFrame(lst, columns=["url", "title", "date", "read_num", "like_num"])
    df.to_excel(fj + ".xlsx")
    # df.to_excel(fj + ".xlsx", encoding="utf-8")

def get_bizs(cookie, nickname_lst, method='qingbo', t=10):
    ab = AccountBiz(cookie, method=method, t=t)
    res_lst = ab.run(nickname_lst)
    bizs = {}
    for res in res_lst:
        biz, nm = res.split(', ')
        bizs[nm] = biz
    return bizs

def get_articles(lst):
    
    item_lst = []
    for i, line in enumerate(lst, 0):
        print("index:", i)
        # item = json.loads('{' + line + '}', strict=False)
        item = line
        timestamp = item["comm_msg_info"]["datetime"]
        ymd = time.localtime(timestamp)
        date = "{}-{}-{}".format(ymd.tm_year, ymd.tm_mon, ymd.tm_mday)

        infos = item["app_msg_ext_info"]
        print(item)
        url_title_lst = [[infos["content_url"], infos["title"]]]
        if "multi_app_msg_item_list" in infos.keys():
            url_title_lst += [
                [info["content_url"], info["title"]]
                for info in infos["multi_app_msg_item_list"]
            ]

        for url, title in url_title_lst:
            item_lst.append([title, url])


if __name__ == '__main__':
    uin = "MjYwOTk2NzcwMA=="

    if AUTO_PARAMS:
        start_proxy()
        appmsg_token, cookie, key = main('output.txt')
        print(key)
        print(appmsg_token)
        print(cookie)
        close_proxy()
    else:
        key = "b8982b21b1d07965c2852fb27cba643334a1683d52ec27650ee893f2c11e6e3ac0bb18124882b57d7b1c56d21c9a2013bb58740dc95fa80c2f1fd5252f450acbb42e80add3fa1ff521b6188d7933cb6ca1343da5d4b44c3a1c8d307849d8692fec2f40635300c241415915a97d1935dba5337f5029e5c44342266a1e20c29cd3"
        appmsg_token = "1243_yAVjxy%2FtbJMuZE7P6zTAekOyfiKI3hsyQvVxeEwzt33RwQxWuKN5ylbJ9Hv8f_8oQMsyekC7t1i7HRCi"
        cookie = "rewardsn=; wxtokenkey=777; wxuin=2609967700; devicetype=Windows10x64; version=6309071d; lang=zh_CN; appmsg_token=1243_FvHB9vgbs3aTk58Z6zTAekOyfiKI3hsyQvVxeKvIZ6meUhjKivDiY6t1-57sAWFbJUHzRpiqru1uBBof; pass_ticket=0qd1KeoF7HTrcAnsPy2vfhus6OwvU6wgq8WMIs01ycCXJCMImhmxcoLkBvUI4T9UPy7gTKAgWVFi8/B3rRDceg==; wap_sid2=CNTkw9wJEooBeV9IT0lzZHZfZmdrdFFSbnNJRjZnaDNBRV93WnFaeHh2WGIxRUNyR1ZrTDQzOHFHRDY1YzBFaVdwZEZnOFpFSHcxSWd4WmR2Rk5vb2Z6REgyLTdjUmdjX3I0THN1X3FJNGszWDJ2NFc0NmFwdnBiLU9ISC1CWldjbGNmQkNhdXVYNFBya1NBQUF+MP3ey6oGOA1AAQ=="
    
    bizs = get_bizs(cookie, nickname_lst, method)
    res_lst = []
    for biz in bizs.values():
        lst = get_history_urls(
            biz, uin, key, lst=[], start_timestamp=0, start_count=0, end_count=10
        )
        for item_lst in lst:
            res_lst += item_lst

    # appmsg_token, cookie = main('output.txt')
    # 
    ai = ArticlesInfo(appmsg_token, cookie)
    get_articles(res_lst)




    con = None
    try:
        con = Connection(
            host='localhost',
            port=3306,
            user='root',
            password='962464',
            database='db_wx',
            autocommit=True
        )
        cursor = con.cursor()
        cursor.execute("insert into articles values(0, {}, {}, {}, {}, {}, 0)".format(gzh_name, title, url, digest))
    except Exception as e:
        print(e)
    finally:
        if con:
            con.close()