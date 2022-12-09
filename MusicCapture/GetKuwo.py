import random

import requests
from . import HeadersALL

class Kuwo:
    def __init__(self, MusicName):
        self.MusicName = MusicName

    def Search(self):
        GET = requests.get(
            f"http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={self.MusicName}&pn=1&rn=30&httpsStatus=1",
            headers={
                "User-Agent":random.choice(HeadersALL.HeadersALL),
                "Accept":"application/json, text/plain, */*",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.9",
                "Connection":"keep-alive",
                "Cookie":"Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1664283247; _ga=GA1.2.1841019568.1664283248; _gid=GA1.2.1022942782.1664283248; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1664283851; kw_token=M114UNY2MWR",
                "csrf":"M114UNY2MWR",
                "Host":"www.kuwo.cn",
                "Referer":"http://www.kuwo.cn/search/list?key=%E6%89%93%E4%B8%8A%E8%8A%B1%E7%81%AB"
            }
        )
        if GET.status_code == 200:
            ReturnData = {}
            line = 0
            for data in GET.json()['data']['list']:
                ReturnData[line] = {
                    "FileName":data['name'],
                    "authors":data['artist'].split("&"),
                    "img":data['pic'],
                    "Original Address":f"http://www.kuwo.cn/play_detail/{data['musicrid'].split('_')[-1]}",
                    "mp3":self.GetMp3(data['musicrid'].split('_')[-1])
                }
                line += 1
            return ReturnData
        else:
            return False

    def GetMp3(self, id) -> str:
        GET = requests.get(
            f"http://www.kuwo.cn/api/v1/www/music/playUrl?mid={id}&type=music&httpsStatus=1&reqId=c202a0f1-3e63-11ed-b448-5b804af194f7",
            headers={
                "Accept":"application/json, text/plain, */*",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.9",
                "Connection":"keep-alive",
                #"Cookie":"Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1664283247; _ga=GA1.2.1841019568.1664283248; _gid=GA1.2.1022942782.1664283248; _gat=1; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1664283332; kw_token=9E8UOVUJU6V",
                "Host":"www.kuwo.cn",
                "Referer":"http://www.kuwo.cn/play_detail/28510075",
                "User-Agent":random.choice(HeadersALL.HeadersALL)
            }
        )
        if GET.status_code == 200:
            return GET.json()['data']['url']
        else:
            return False

# for value in Kuwo("打上花火").Search().values():
#     print(value)