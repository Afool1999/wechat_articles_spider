# coding: utf-8
import os
from pprint import pprint
from wechatarticles import PublicAccountsWeb

if __name__ == "__main__":
    # 模拟登录微信公众号平台，获取微信文章的url
    cookie = "RK=YYlIy87YR6; ptcz=97355eef17b34f45776c7532edcf0812fc192ecf68f9ffdffef7722e7b5db53f; eas_sid=A1r6j9G1r8T5E6A2m3h8Z5F8z0; pgv_pvid=1846195224; fqm_pvqid=cd09baab-c963-4d2e-af78-4ae42fe489e6; qq_domain_video_guid_verify=dde95339f7c6b042; ua_id=CsFwkMtNgJ9WxwirAAAAAL8Mq4Lf-3XxfMrCLMNVTcs=; wxuin=99953537801256; _clck=1g6fqgz|1|fgp|0; uuid=94c07757ba4e6db00ef42ba555d5a517; bizuin=3936613344; ticket=1f01a03733a08843e388879cd3c6c954dbab1bf2; ticket_id=gh_ace33390697f; slave_bizuin=3936613344; cert=HViiPP_SWJdF9OKS0amX3Cb2gdX7OM0K; noticeLoginFlag=1; remember_acct=yieer123%40126.com; rand_info=CAESIE7JyJlwfqXTGNxG45abCW+WjQMBpDC2EuY/YzUToYOw; data_bizuin=3936613344; data_ticket=cA0uC3bBGDB+ZnEAbreM2WBTQQH8iG8Wc5zGOzFMbeoxnaF4vE6MGTOoYVkJ83nK; slave_sid=a2ZiRzlBZmpBeHhORjFMYnh2ZXlsSUYzZHBJWlFndkJ5UXlicU5SdEFmdUliQ1FqMTFJcWF0a3ZRNE5wdUJjOWpHVXBmQjQyaUI5SlV2RGtSQjFabzM3ZzZWMXRKYm9mOUtfME5PdUI2d2hTZzZaU0tWMHl3TjEwMGw1QnhQYmtxWVAxM0VoUWphZGU3MGM1; slave_user=gh_ace33390697f; xid=655281c23512e168893bb46a89c9602c; openid2ticket_o4POj6mtvi9BHD616Eio3zmAqf3I=fM1WGbHUHpfyDafCZP3Fhptrg1X30cLH2ytEBmBiY/I=; mm_lang=zh_CN; _clsk=1505l1m|1699953585252|2|1|mp.weixin.qq.com/weheat-agent/payload/record"
    token = "880378220"
    nickname = "萤人聚集地"

    paw = PublicAccountsWeb(cookie=cookie, token=token)
    # articles_sum = paw.articles_nums(nickname)
    article_data = paw.get_urls(nickname, begin="0", count="5")
    # official_info = paw.official_info(nickname)

    # print("articles_sum:", end=" ")
    # print(articles_sum)
    print("artcles_data:")
    pprint(article_data)
