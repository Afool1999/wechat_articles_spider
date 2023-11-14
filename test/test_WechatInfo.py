# coding: utf-8
import os
from pprint import pprint
from wechatarticles import ArticlesInfo

if __name__ == "__main__":
    # 登录微信PC端获取文章信息
    appmsg_token, cookie = "1243_yAVjxy%2FtbJMuZE7P6zTAekOyfiKI3hsyQvVxeEwzt33RwQxWuKN5ylbJ9Hv8f_8oQMsyekC7t1i7HRCi", "rewardsn=; wxtokenkey=777; wxuin=2609967700; devicetype=Windows10x64; version=6309071d; lang=zh_CN; appmsg_token=1243_FvHB9vgbs3aTk58Z6zTAekOyfiKI3hsyQvVxeKvIZ6meUhjKivDiY6t1-57sAWFbJUHzRpiqru1uBBof; pass_ticket=0qd1KeoF7HTrcAnsPy2vfhus6OwvU6wgq8WMIs01ycCXJCMImhmxcoLkBvUI4T9UPy7gTKAgWVFi8/B3rRDceg==; wap_sid2=CNTkw9wJEooBeV9IT0lzZHZfZmdrdFFSbnNJRjZnaDNBRV93WnFaeHh2WGIxRUNyR1ZrTDQzOHFHRDY1YzBFaVdwZEZnOFpFSHcxSWd4WmR2Rk5vb2Z6REgyLTdjUmdjX3I0THN1X3FJNGszWDJ2NFc0NmFwdnBiLU9ISC1CWldjbGNmQkNhdXVYNFBya1NBQUF+MP3ey6oGOA1AAQ=="
    article_url = "http://mp.weixin.qq.com/s?__biz=MjM5NDU4ODI0NQ==&mid=2650949647&idx=1&sn=854714295ceee7943fe9426ab10453bf&chksm=bd739b358a041223833057cc3816f9562999e748904f39b166ee2178ce1a565e108fe364b920#rd'"
    test = ArticlesInfo(appmsg_token, cookie)
    comments = test.comments(article_url)
    read_num, like_num, old_like_num = test.read_like_nums(article_url)
    print("comments:")
    pprint(comments)
    print("read_like_num:", read_num, like_num, old_like_num)
