import io
import json
import os
import random

from flask import Flask
from flask import url_for
from flask import request
from flask import jsonify
from flask import render_template
from flask import send_file

import requests
from rembg import remove
from PIL import Image
from fileid import fileid

import GetPixivImage
import SearchMusic

app = Flask(__name__)

@app.route("/")
def index():
    # with open("./static/index/PYDOME_TYPE/images/slides/slides.json", "r", encoding="utf-8") as rfp:
    #     return render_template("index.html", BgImageFile=dict(json.loads(rfp.read())).values())
    __files = []
    for paths, dirs, files in os.walk(f"./static/index/PYDOME_TYPE/images/slides"):
        for file in files:
            __files.append(paths+f"/{file}")

    return render_template("index.html", BgImageFile=__files)

@app.route("/10_12")
def birthday10_12():
    return render_template("10_12.html")

@app.errorhandler(404)
def Error_404(error):
    return render_template("404.html"), 404

@app.route("/Mili_Wallpaper")
def Mili_Wallpaper():
    return render_template("Mili_Wallpaper.html")

@app.route("/Mili_Wallpaper/list")
def Mili_Wallpaper_List():
    return render_template("list.html")

@app.route("/and")
def Mili_Wallpaper_AndHtml():
    return render_template("and.html")

@app.route("/API/MiliWallpaper/Mili_Wallpaper_Version")
def Mili_Wallpaper_Version():
    return render_template("MiliWallpaperVersion.html")

def GetAPIAudio(DIR):
    Audio = []
    for paths, dirs, files in os.walk(DIR):
        for file in files:
            Audio.append(f"{paths}/{file}")

    return Audio

@app.route("/API/dls")
def Dls():
    return send_file(random.choice(GetAPIAudio("./static/dls/audio")))

@app.route("/API/hutao")
def hutao():
    return send_file(random.choice(GetAPIAudio("./static/hutao/audio")))

@app.route("/API/maren")
def maren():
    return send_file(random.choice(GetAPIAudio("./static/maren/audio")))

@app.route("/API/share")
def ShareFile():
    FileName = request.args.get("filename")
    if FileName:
        try:
            return send_file(f"./static/share/{FileName}")
        except FileNotFoundError:
            return "FileName Error"
    else:
        return "Not FileName"

@app.route("/API/PixivImage")
def PixivImage():
    return {
        "url": GetPixivImage.GetImageUrl(random.choice(GetPixivImage.GetRanking()))
    }

@app.route("/rembg")
def Rembg():
    FileUrl = request.args.get("file")
    RandomFileName = fileid.Newid(10).newfileid()
    if FileUrl:
        GET = requests.get(FileUrl)
        if GET.status_code == 200:
            remove(Image.open(io.BytesIO(GET.content))).save(f"./static/rembg/log/{RandomFileName}.png")
            return send_file(f"./static/rembg/log/{RandomFileName}.png")
        else:
            return jsonify({"code": "File Url Eorror"})
    else:
        return jsonify({"code": "Not File Url"})

@app.route("/RziL")
def RziL():
    RaedSlidesJson = json.loads(open("./static/index/PYDOME_TYPE/images/slides/slides.json", "r", encoding="utf-8").read())
    return render_template(
        "RziL.html",
        bg=random.choice([i for i in RaedSlidesJson.values()]),
        RandomColor=random.choice(
                [
                    'rad',
                    'yellow',
                    'blue',
                    "black",
                    "silver",
                    "gray",
                    "white",
                    "maroon",
                    "purple",
                    "fuchsia",
                    "green",
                    "lime",
                    "olive",
                    "navy",
                    "blue",
                    "teal",
                    "aqua"
                ]
            )
    )

@app.route("/RziLSearch")
def RziLSearch():
    MusicName = request.args.get("MusicName")
    if MusicName:
        return render_template(
            "RziLSearch.html",
            MusicData=SearchMusic.Search(MusicName).SearchAll()
        )
    else:
        return "Not FileName"

@app.route("/LSP")
def LSP():
    return render_template("LSP.html")

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True,
    )