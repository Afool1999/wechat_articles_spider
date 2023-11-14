# coding: utf-8
import os
from pprint import pprint
from wechatarticles import PublicAccountsWeb
from pymysql import Connection
from pymysql.converters import escape_string
import time

if __name__ == "__main__":
    # 模拟登录微信公众号平台，获取微信文章的url
    cookie = "RK=YYlIy87YR6; ptcz=97355eef17b34f45776c7532edcf0812fc192ecf68f9ffdffef7722e7b5db53f; eas_sid=A1r6j9G1r8T5E6A2m3h8Z5F8z0; pgv_pvid=1846195224; fqm_pvqid=cd09baab-c963-4d2e-af78-4ae42fe489e6; qq_domain_video_guid_verify=dde95339f7c6b042; ua_id=CsFwkMtNgJ9WxwirAAAAAL8Mq4Lf-3XxfMrCLMNVTcs=; wxuin=99953537801256; _clck=1g6fqgz|1|fgp|0; uuid=94c07757ba4e6db00ef42ba555d5a517; bizuin=3936613344; ticket=1f01a03733a08843e388879cd3c6c954dbab1bf2; ticket_id=gh_ace33390697f; slave_bizuin=3936613344; cert=HViiPP_SWJdF9OKS0amX3Cb2gdX7OM0K; noticeLoginFlag=1; remember_acct=yieer123%40126.com; rand_info=CAESIE7JyJlwfqXTGNxG45abCW+WjQMBpDC2EuY/YzUToYOw; data_bizuin=3936613344; data_ticket=cA0uC3bBGDB+ZnEAbreM2WBTQQH8iG8Wc5zGOzFMbeoxnaF4vE6MGTOoYVkJ83nK; slave_sid=a2ZiRzlBZmpBeHhORjFMYnh2ZXlsSUYzZHBJWlFndkJ5UXlicU5SdEFmdUliQ1FqMTFJcWF0a3ZRNE5wdUJjOWpHVXBmQjQyaUI5SlV2RGtSQjFabzM3ZzZWMXRKYm9mOUtfME5PdUI2d2hTZzZaU0tWMHl3TjEwMGw1QnhQYmtxWVAxM0VoUWphZGU3MGM1; slave_user=gh_ace33390697f; xid=655281c23512e168893bb46a89c9602c; openid2ticket_o4POj6mtvi9BHD616Eio3zmAqf3I=fM1WGbHUHpfyDafCZP3Fhptrg1X30cLH2ytEBmBiY/I=; mm_lang=zh_CN; _clsk=1505l1m|1699953585252|2|1|mp.weixin.qq.com/weheat-agent/payload/record"
    token = "880378220"
    nicknames = ['交大社总',
'交大艺术中心',
'菁菁有戏',
'上海交通大学励志讲坛',
'SJTU勤工助学部',
'上海交大生活',
'上海交通大学学生事务中心',
'益友sjtu',
'交大源源',
'平安交大',
'交大思思',
'上海交通大学教务处',
'上海交通大学学生联合会',
"国情研习社",
"交大新青年集结号",
"交大戎耀",
"晨曦志愿者服务社",
"蒲公英服务社",
"SJTU思源爱心服务社",
"SJTU翡翠丝带",
"交大守望HospiceCare",
"上海交大阳光工程",
"sjtu馆遍上海",
"TECC",
"sjtu手语社",
"SJTU喵汪",
"SJTUOceanAssociation",
"SJTU交心",
"上海交通大学校友会",
"达医晓护 菁菁校园",
"SJTU名道文博社",
"绿格SJTU",
"交大白岩诗社",
"800号电影社",
"上交笛协",
"SJTU精油与芳香疗法社团",
"交大吉协",
"玛纳卡实验剧社",
"交大花花",
"SJTUPA摄影协会",
"上海交通大学Minecraft社",
"阳光剧社",
"上海交大推协",
"交大乐队联盟",
'上交粤协',
'交大书协',
'上海交通大学西洲古琴社',
'SJTU源社',
'SJTU中日桥',
'上海交通大学中法协会',
'sjtu钢协',
'交大肉协',
'MICA器乐交流',
'SJTU巴协',
'上海交大国学社',
'SAPA',
'思南汉韵',
'上海交大偶像研究院',
'交大歌手联盟',
'交大美协',
'南洋舞社',
'上海交大葡萄与葡萄酒',
'SJTU烘焙社',
'SJTU豫文化交流协会',
'SJTU数独社',
'SJTU二十四节令鼓队',
'交大幻协',
'Fsquare舞社',
'上海交大领读者',
'上海交大ICCI创想社',
'览卓藏文化社',
'MagicCircleSJTU',
'SJTU音乐剧社',
'上海交通大学网络文化工作室联盟',
'哑巴FM',
'J-Teen说唱社',
'上海交大SIEC',
'SJTU阿卡贝拉',
'上海交通大学思辩学社',
'交大模联',
'思源星君',
'未建协sjtu',
'上海交通大学交龙机器人俱乐部',
'交大史学社',
'SJTU未来现实LAB',
'SJTUG',
'SJTU船模队',
'SJTU赛车队',
'SJTU数学建模',
'交大PHD',
'SJTUblockchain',
'SJTU无人机俱乐部',
'SJTU英语辩论社',
'交大棒垒',
'SJTUJeetKuneDo',
'SJTU交大空手道',
'交大篮协',
'SJTU乒协',
'525dancecrewSJTU',
'交大围棋',
'交大野协',
'上海交大泳协',
'上海交大羽协',
'上海交大足协',
'SJTU cycling',
'上海交大棋联',
'SJTU跆拳道协会',
'SJTU轮滑社',
'上海交大棋联',
'SJTU跑虫俱乐部',
'SJTU台协',
'交大武协',
'SJTU铁三',
'上交网协sjtu',
'交大滑板社,SJTU滑板之家',
'浮泽',
'上交相协',
'SJTU极限篮球',
'SJTU魔方社',
'交大极限飞盘',
'上海交大国标舞',
'erdo63@126.com',
'交大排协',
'交大万智桌游',
'SJTU赛艇俱乐部',
'交大搏击俱乐部',
'上海交大电竞社',
'上海交大桌游社',
'SJTU射艺',
'sjtu冰壶',
'上交格斗俱乐部',
'上海交大Labview',
'SJTU双创',
'交大CIC',
'上海交大安泰美世CDA',
'SJTU创客联萌、SJTU创客联萌微服务',
'交大人世界声'
]

    insert_data = []
    paw = PublicAccountsWeb(cookie=cookie, token=token)
    for nickname in nicknames:
        print(nickname)
        try:
            article_data = paw.get_urls(nickname, begin="0", count="5")
            for article in article_data:
                ymd = time.localtime(article['create_time'])
                date = "{}-{}-{}".format(ymd.tm_year, ymd.tm_mon, ymd.tm_mday)
                insert_data.append([nickname, article['cover'], article['title'], escape_string(article['link']), article['digest'], date])
            time.sleep(3)
        except Exception as e:
            print(e)
        



    # print(insert_data)
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
    for data in insert_data:
        try:
            cursor.execute("insert into articles values(0, %s, %s, %s, %s, %s, %s, 0)", (*data,))
        except Exception as e:
            print(e)

    if con:
        con.close()