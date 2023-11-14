# coding: utf-8
import os
from pprint import pprint
from wechatarticles import Url2Html

if __name__ == "__main__":
    # 微信文章下载为离线HTML（含图片）
    # 微信文章的url
    url = "http://mp.weixin.qq.com/s?__biz=MzA4ODAwMTQzMg==&amp;mid=2650095989&amp;idx=1&amp;sn=c3ef1c41e55826aec8ee957ae242ad8e&amp;chksm=aa4a1c9c01383930e0d449079e655c6a51d1c42c47abb7f113b2f1d8e22873db14f8b4d3ec50&amp;scene=27#wechat_redirect"
    uh = Url2Html()
    # 请提前创建一个以公众号为名的文件夹，并且在该文件夹下创建imgs文件夹
    res = uh.run(url, mode=4)
    print(res)
