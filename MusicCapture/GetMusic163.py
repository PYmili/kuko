import base64
import binascii
import json
import random
import string

from . import HeadersALL

headers = {
        'authority': 'music.163.com',
        'user-agent': random.choice(HeadersALL.HeadersALL),
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://music.163.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://music.163.com/search/',
        'accept-language': 'zh-CN,zh;q=0.9',
    }

import requests
from Crypto.Cipher import AES

class GetParamsAndEncSecKey:
    def __init__(self, MsiceName):
        self.MusicName = MsiceName
        self.Data = {
            "hlpretag": "<span class=\"s-fc7\">",
            "hlposttag": "</span>",
            "s": MsiceName,
            "type": "1",
            "offset": "0",
            "total": "true",
            "limit": "30",
            "csrf_token": ""
            }
        self.Data = json.dumps(self.Data)

    def Generate(self):
        return self.final_param(self.Data, self.RandomString())

    def RandomString(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 16))

    def len_change(self, text):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        text = text.encode("utf-8")
        return text

    def AES(self, text, key):
        iv = b'0102030405060708'
        text = self.len_change(text)
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(text)
        return base64.b64encode(encrypted).decode()

    def B(self, text, String: str):
        first_data = self.AES(text, '0CoJUm6Qyw8W8jud')
        return self.AES(first_data, String)

    def C(self, text):
        e = '010001'
        f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3'
        f += 'ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557'
        f += 'c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e8'
        f += '2047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        text = text[::-1]
        result = pow(int(binascii.hexlify(text.encode()), 16), int(e, 16), int(f, 16))
        return format(result, 'x').zfill(131)

    def final_param(self, text, str):
        return {'params': self.B(text, str), 'encSecKey': self.C(str)}

class GetMusic163Music:
    def __init__(self, MuscicName):
        self.MusicName = MuscicName

    def Search(self):
        main = GetParamsAndEncSecKey(self.MusicName)
        GET = requests.post(
            "https://music.163.com/weapi/cloudsearch/get/web?csrf_token=",
            headers=headers,
            data=main.Generate()
        )
        if GET.status_code == 200:
            JSONDATA = GET.json()['result']['songs']
            ReturnData = {}
            line = 0
            for Data in JSONDATA:
                ReturnData[line] = {
                    "FileName":Data['al']['name'],
                    "introduce":[alia for alia in Data['alia']],
                    "authors":[author['name'] for author in Data['ar']],
                    "img":Data['al']['picUrl'],
                    "Original Address":f"https://music.163.com/#/song?id={Data['id']}",
                    "mp3":self.GetMusicUrl(Data['id'])
                }
                line += 1
            return ReturnData
        else:
            return False

    def GetMusicUrl(self, id: str):
        GET = requests.get(f"http://music.163.com/song/media/outer/url?id={id}.mp3")
        if GET.status_code == 200:
            return GET.url
        else:
            return False

# if __name__ == '__main__':
#     for key, value in GetMusic163Music("打上花火").Search().items():
#         print(key, "--", value)