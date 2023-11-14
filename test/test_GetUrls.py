# coding: utf-8
import json
import os
import random
import time
from pprint import pprint

import pandas as pd
from wechatarticles import ArticlesInfo
from wechatarticles.utils import get_history_urls, verify_url

# 快速获取大量文章urls（利用历史文章获取链接）


def save_xlsx(fj, lst):
    df = pd.DataFrame(lst, columns=["url", "title", "date", "read_num", "like_num"])
    df.to_excel(fj + ".xlsx")
    # df.to_excel(fj + ".xlsx", encoding="utf-8")


def demo(lst):
    # 抓取示例，供参考，不保证有效
    fj = "公众号名称"
    item_lst = []
    for i, line in enumerate(lst, 0):
        print("index:", i)
        # item = json.loads('{' + line + '}', strict=False)
        item = line
        timestamp = item["comm_msg_info"]["datetime"]
        ymd = time.localtime(timestamp)
        date = "{}-{}-{}".format(ymd.tm_year, ymd.tm_mon, ymd.tm_mday)

        infos = item["app_msg_ext_info"]
        url_title_lst = [[infos["content_url"], infos["title"]]]
        if "multi_app_msg_item_list" in infos.keys():
            url_title_lst += [
                [info["content_url"], info["title"]]
                for info in infos["multi_app_msg_item_list"]
            ]

        flag = 0
        for url, title in url_title_lst:
            try:
                if not verify_url(url):
                    continue
                # 获取文章阅读数在看点赞数
                read_num, like_num, old_like_num = ai.read_like_nums(url)
                print(read_num, like_num)
                item_lst.append([url, title, date, read_num, like_num])
                time.sleep(random.randint(5, 10))
            except Exception as e:
                print(e)
                flag = 1
                break
            finally:
                save_xlsx(fj, item_lst)

        if flag == 1:
            break

    save_xlsx(fj, item_lst)


if __name__ == "__main__":
    # 需要抓取公众号的__biz参数
    biz = "MzA4ODAwMTQzMg=="
    # 个人微信号登陆后获取的uin
    uin = "MjYwOTk2NzcwMA=="
    # 个人微信号登陆后获取的key，隔段时间更新
    key = "312ddfd3b954ef2514e804e9474167ad0f1e1bc17bddf42a897e59f15d776a65f17ccafcdef1d4b712c5aa1b5f5440b96088153c3ef31878b107b9ed8fe289f5bbf769a7f6b9d8fd5d8a4598169a29b81bae1ff1c3dd5951c0395bc5f4806c75e842416f579d4d1a3f479339d77d2c2dc80214b13de851cc2e96066fff64e5a5"

    lst = get_history_urls(
        biz, uin, key, lst=[], start_timestamp=0, start_count=0, end_count=10
    )
    print("抓取到的文章链接")
#     print(lst)
    res_lst = []
    for item_lst in lst:
        res_lst += item_lst

    # 个人微信号登陆后获取的token
    appmsg_token, cookie = "1243_yAVjxy%2FtbJMuZE7P6zTAekOyfiKI3hsyQvVxeEwzt33RwQxWuKN5ylbJ9Hv8f_8oQMsyekC7t1i7HRCi", "rewardsn=; wxtokenkey=777; wxuin=2609967700; devicetype=Windows10x64; version=6309071d; lang=zh_CN; appmsg_token=1243_FvHB9vgbs3aTk58Z6zTAekOyfiKI3hsyQvVxeKvIZ6meUhjKivDiY6t1-57sAWFbJUHzRpiqru1uBBof; pass_ticket=0qd1KeoF7HTrcAnsPy2vfhus6OwvU6wgq8WMIs01ycCXJCMImhmxcoLkBvUI4T9UPy7gTKAgWVFi8/B3rRDceg==; wap_sid2=CNTkw9wJEooBeV9IT0lzZHZfZmdrdFFSbnNJRjZnaDNBRV93WnFaeHh2WGIxRUNyR1ZrTDQzOHFHRDY1YzBFaVdwZEZnOFpFSHcxSWd4WmR2Rk5vb2Z6REgyLTdjUmdjX3I0THN1X3FJNGszWDJ2NFc0NmFwdnBiLU9ISC1CWldjbGNmQkNhdXVYNFBya1NBQUF+MP3ey6oGOA1AAQ=="
    article_url = "http://mp.weixin.qq.com/s?__biz=MjM5NDU4ODI0NQ==&mid=2650949647&idx=1&sn=854714295ceee7943fe9426ab10453bf&chksm=bd739b358a041223833057cc3816f9562999e748904f39b166ee2178ce1a565e108fe364b920#rd'"
    ai = ArticlesInfo(appmsg_token, cookie)

    # url：微信文章链接. 
    url = res_lst[0]["app_msg_ext_info"]["content_url"]
    read_num, like_num, old_like_num = ai.read_like_nums(url)
    item = ai.comments(url)
    print("阅读：{}; 在看: {}; 点赞: {}".format(read_num, like_num, old_like_num))
    print("评论信息")
    pprint(item)
    
    # 所有url文件
    demo(res_lst)

