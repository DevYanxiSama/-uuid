import base64

import requests
import time


class App:

    def __init__(self):
        self.phoneNumber = ""
        self.verifiCode = ""
        self.token = ""
        self.grant = ""
        self.headers = {
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0",
            "sec-ch-ua": '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

    def test(self):
        print("此方法仅供调试")
        self.token = input("请输入token:")
        if self.token:
            self.getGrant()
            self.getBindList()

    def mainloop(self):
        self.getPhoneNumber()
        self.getVerifiCode()

        if self.verifiCode:
            self.getToken()
        print(self.token)
        if self.token:
            self.getGrant()
            self.getBindList()

    def getPhoneNumber(self, a=False):
        if a:
            print("输入的手机号无效,请重新输入")
            time.sleep(0.1)
        self.phoneNumber = input("请输入手机号以获取验证码:")
        if not self.phoneNumber or len(self.phoneNumber) != 11:
            self.getPhoneNumber(True)

    def getVerifiCode(self):
        print("正在尝试获取验证码...")
        if not self.phoneNumber or len(self.phoneNumber) < 11:
            self.getPhoneNumber(True)
        result = requests.post("https://as.hypergryph.com/general/v1/send_phone_code",
                               json={"phone": str(self.phoneNumber), "type": 2}, headers=self.headers)
        if not result.ok:
            print(result.content)
            if input("请求失败(请求失败),输入任意内容回车重新尝试。"):
                self.getVerifiCode()
            else:
                print("程序退出")
            return

        if result.json()['msg'] == "OK":
            self.verifiCode = input(f"验证码已发送到 {self.phoneNumber} ,请输入验证码:")
        else:
            print(result.json()['msg'])
            if input("接口拒绝,输入任意内容回车重新尝试。"):
                self.getVerifiCode()
            else:
                print("程序退出")
            return

    def getToken(self):
        print("正在获取token...")
        result = requests.post(f"https://as.hypergryph.com/user/auth/v2/token_by_phone_code", json={
            "phone": self.phoneNumber, "code": self.verifiCode}, headers=self.headers)
        if not result.ok:
            if input("请求失败,输入任意内容回车重新尝试。"):
                self.getToken()
            else:
                print("程序退出")
            return

        if result.json()['msg'] == "OK":
            print(f"token获取成功\n鉴于安全考虑,此处不展示")
            self.token = result.json()["data"]["token"]
        else:
            print(result.json()['msg'])
            if input("接口拒绝,输入任意内容回车重新尝试。"):
                self.getToken()
            else:
                print("程序退出")
            return

    def getGrant(self):
        print("正在请求grant token...")
        result = requests.post(f"https://as.hypergryph.com/user/oauth2/v2/grant", json={
            "token": self.token, "appCode": "be36d44aa36bfb5b", "type": 1}, headers=self.headers)
        if not result.ok:
            if input("请求失败,输入任意内容回车重新尝试。"):
                self.getGrant()
            else:
                print("程序退出")
            return

        if result.json()['msg'] == "OK":
            print(f"grant token获取成功\n鉴于安全考虑,此处不展示")
            self.grant = result.json()["data"]["token"]
            if not self.is_base64(self.grant):
                self.grant = base64.b64encode(self.grant.encode('utf-8')).decode('utf-8')
        else:
            print(result.json()['msg'])
            if input("接口拒绝,输入任意内容回车重新尝试。"):
                self.getGrant()
            else:
                print("程序退出")
            return

    @staticmethod
    def is_base64(s):
        try:
            # 尝试解码
            base64.b64decode(s, validate=True)
            return True
        except:
            return False

    def getBindList(self):
        print("正在获取绑定结果")
        result = requests.get(
            f"https://binding-api-account-prod.hypergryph.com/account/binding/v1/binding_list?",
            params={"token": self.grant},
            headers=self.headers)

        if not result.ok:
            print(result.content)
            if input("请求失败,输入任意内容回车重新尝试。"):
                self.getBindList()
            else:
                print("程序退出")
            return

        if result.json()['msg'] != "OK":
            print(result.json()['msg'])
            if input("接口拒绝,输入任意内容回车重新尝试。"):
                self.getBindList()
            else:
                print("程序退出")
            return
        else:
            data = result.json()['data']['list']
            print(data)
            print("\n" * 5)
            for __data in data:
                nickName = "不存在"
                if "nickName" in __data["bindingList"][0].keys():
                    nickName = __data["bindingList"][0]["nickName"]
                print(
                    f"游戏名:{__data["appName"]}\n昵称:{nickName}\nuuid:{__data["bindingList"][0]["uid"]}\n服务器:{__data["bindingList"][0]["channelName"]}")
                print("\n" * 1)


def show_disclaimer():
    disclaimer = """
    =============== 重要警告 ===============
    1. 这是非官方工具，可能违反服务条款
    2. 使用可能导致账号风险
    3. 作者不承担任何使用后果
    4. 仅限个人学习和研究使用

    输入 '我了解并接受风险' 继续：
    """
    print(disclaimer)
    confirm = input()
    if confirm != "我了解并接受风险":
        print("已取消")
        exit(0)


if __name__ == '__main__':
    show_disclaimer()

    print("-" * 20)
    print("\n\n\n")
    print("本项目涉及你的token，但是承诺token仅用于数据查询，不做任何保留。")
    print("\n\n\n")
    print("-" * 20)

    app = App()
    app.mainloop()
