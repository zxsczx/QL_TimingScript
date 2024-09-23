# -*- coding=UTF-8 -*-
# @Project          QL_TimingScript
# @fileName         hykb.py
# @author           Echo
# @EditTime         2024/9/20
import os
import re
from datetime import datetime

import requests
import random
from sendNotify import send_notification_message

if 'Hykb_cookie' in os.environ:
    Hykb_cookie = re.split("@|&", os.environ.get("Hykb_cookie"))
else:
    Hykb_cookie = []
    print("未查找到Hykb_cookie变量.")


class HaoYouKuaiBao():
    """好游快爆签到
    """

    def __init__(self, cookie, user_agent):
        self.cookie = cookie
        self.url = "https://huodong3.3839.com/n/hykb/{}/ajax{}.php"
        self.data = "ac={}&r=0.{}&scookie={}"
        self.headers = {
            "Origin": "https://huodong3.i3839.com",
            "Referer": "https://huodong3.3839.com/n/hykb/cornfarm/index.php?imm=0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": user_agent
        }

    def plant(self) -> int:
        """播种
        """
        url = self.url.format("cornfarm", "_plant")
        data = self.data.format("Plant", random.randint(1000000000000000, 8999999999999999), self.cookie)
        try:
            response = requests.post(url, headers=self.headers, data=data).json()
            if response['key'] == 'ok':
                print("好游快爆-播种成功")
                send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"), "好游快爆-播种成功")
                return 1
            else:
                if response['seed'] == 0:
                    print("好游快爆-种子已用完")
                    send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"), "好游快爆-种子已用完")
                    return -1
                else:
                    print("好游快爆-播种失败")
                    send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"), "好游快爆-播种失败")
                    return 0
        except Exception as e:
            print(f"好游快爆-播种出现错误：{e}")
            return False

    def harvest(self) -> bool:
        """收获
        """
        url = self.url.format("cornfarm", "_plant")
        data = self.data.format("Harvest", random.randint(1000000000000000, 8999999999999999), self.cookie)
        try:
            response = requests.post(url, headers=self.headers, data=data).json()
            if response['key'] == 'ok':
                print("好游快爆-收获成功")
                send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"), "好游快爆-收获成功")
                return True
            else:
                print("好游快爆-收获失败")
                send_notification_message("好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"), "好游快爆-收获失败")
                return False
        except Exception as e:
            print(f"好游快爆-收获出现错误：{e}")
            return False

    def login(self):
        """登录
        """
        url = self.url.format("cornfarm", "")
        data = self.data.format("login", random.randint(100000000000000, 8999999999999999), self.cookie)
        response = requests.post(url, headers=self.headers, data=data)
        try:
            response = response.json()
            return response
        except Exception as e:
            print("好游快爆-登录出现错误：{}".format(e))
            # response = response.text
            # return response

    def watering(self):
        """浇水
        """
        url = self.url.format("cornfarm", "_sign")
        data = self.data.format("Sign&verison=1.5.7.005&OpenAutoSign=",
                                random.randint(100000000000000, 8999999999999999), self.cookie)
        try:
            response = requests.post(url, headers=self.headers, data=data).json()
            if response['key'] == 'ok':
                print("好游快爆-浇水成功")
                send_notification_message(title="好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"), content="好游快爆-浇水成功")
                return 1, response['add_baomihua']
            elif response['key'] == '1001':
                print("好游快爆-今日已浇水")
                send_notification_message(title="好游快爆签到通知 - " + datetime.now().strftime("%Y/%m/%d"), content="好游快爆-今日已浇水")
                return 0, 0
            else:
                print("好游快爆-浇水出现错误：{}".format(response))
                return -1, 0
        except Exception as e:
            print("好游快爆-浇水出现错误：{}".format(e))
            return -1, 0

    # def buyseeds(self):
    #     """购买种子
    #     """
    #     url = self.url.format("bmhstore2/inc/virtual", "Virtual")
    #     print(url)
    #     ac = "exchange&t=" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "&goodsid=14565"
    #     data = self.data.format(ac, random.randint(100000000000000, 8999999999999999), self.cookie)
    #     print(data)
    #     response = requests.post(url, headers=self.headers, data=data)
    #     print(response.json())

    def sgin(self):
        info = ""
        # 登录
        data = self.login()
        if data['key'] == 'ok':
            if data['config']['csd_jdt'] == "100%":
                # 收获
                if self.harvest():
                    info = info + "收获成功\n"
                    # 播种
                    b = self.plant()
                    if b == -1:
                        info = info + "播种失败，没有种子\n"
                    elif b == 1:
                        info = info + "播种成功\n"
                        # 浇水
                        data = self.watering()
                        if data[0] == 1:
                            info = info + f"浇水成功,获得{data[1]}爆米花\n"
                        elif data[0] == 0:
                            info = info + f"今日已浇水\n"
                        else:
                            info = info + f"浇水失败\n"
                    else:
                        info = info + "播种失败\n"
                else:
                    info = info + "收获失败\n"

            elif data['config']['grew'] == '-1':
                # 播种
                b = self.plant()
                if b == -1:
                    info = info + "播种失败，没有种子\n"
                elif b == 1:
                    info = info + "播种成功\n"
                    # 浇水
                    data = self.watering()
                    if data[0] == 1:
                        info = info + f"浇水成功,获得{data[1]}爆米花\n"
                    elif data[0] == 0:
                        info = info + f"今日已浇水\n"
                    else:
                        info = info + f"浇水失败\n"
                else:
                    info = info + "播种失败\n"

            else:
                # 浇水
                data = self.watering()
                if data[0] == 1:
                    info = info + f"浇水成功,获得{data[1]}爆米花\n"
                elif data[0] == 0:
                    info = info + f"今日已浇水\n"
                else:
                    info = info + f"浇水失败\n"
        else:
            info = info + "登录失败\n"

        return info


if __name__ == '__main__':
    user_agents = [
        "Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/115.0.5790.166 Mobile Safari/537.36Androidkb/1.5.7.005(android;M2012K11AC;13;1080x2320;WiFi);@4399_sykb_android_activity@",
        "Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/96.0.4664.104 Mobile Safari/537.36Androidkb/1.5.7.507(android;Redmi K30 Pro;12;1080x2356;WiFi);@4399_sykb_android_activity@"
    ]
    for cookie_, user_agent in zip(Hykb_cookie, user_agents):
        hykb = HaoYouKuaiBao(cookie_, user_agent)
        hykb.sgin()
        del hykb
