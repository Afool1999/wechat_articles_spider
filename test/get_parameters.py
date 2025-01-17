# get_params.py
from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
import re
import os
from urllib.parse import parse_qs



# command: python get_params outfile
def get_params(outfile):
    appmsg_token = ''
    cookie = ''
    key_ = ''
    with open(outfile, "rb") as logfile:
        freader = io.FlowReader(logfile)
        try:
            for f in freader.stream():
                # 获取完整的请求信息
                state = f.get_state()
                # 尝试获取cookie和appmsg_token,如果成功就停止
                try:
                    # 截取其中request部分
                    request = state["request"]
                    print(request['content'])
                    # 提取Cookie
                    for item in request["headers"]:
                        key, value = item
                        if key == b"cookie":
                            cookie = cookie + value.decode() + '; '
                    params = parse_qs(request['path'])
                    key_ = params[b'key'][0].decode()


                    # 提取appmsg_token
                    path = request["path"].decode()
                    appmsg_token_string = re.findall("appmsg_token.+?&", path)
                    appmsg_token = appmsg_token_string[0].split("=")[1][:-1]
                    break
                except Exception:
                    continue
        except FlowReadException as e:
            print("Flow file corrupted: {}".format(e))
    return appmsg_token, cookie[:-2], key_


def main(outfile):
    path = os.path.split(os.path.realpath(__file__))[0]
    command = "mitmdump -q -s {}/get_outfile.py -w {} mp.weixin.qq.com/mp/getappmsgext".format(
        path, outfile)
    os.system(command)
    return get_params(outfile)