import os
import random
import json

from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import send_file

# from PIL import Image
# import requests
#
import GetPixivImage

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


def GetSlidesImage() -> list:
    # https://gitcode.net/qq_53280175/kuko/-/raw/master/static/index/PYDOME_TYPE/images/slides/{file}
    ImageList = []

    walkPath = "./static/index//images/slides/"
    for paths, dirs, files in os.walk(walkPath):
        for file in files:
            ImageList.append(paths+file)

    return ImageList


@app.route("/", )
def index():
    return render_template(
        "index.html",
        BgImageFile=GetSlidesImage()
    )


@app.route("/LSP")
def LSP():
    return render_template("LSP.html")


@app.route("/PYahao")
def PYahao():
    return render_template("PYahao.html")


@app.route("/10_12")
def fun10_12():
    return render_template("10_12.html")


def GetAudio(_DIR):
    Audio = []

    for paths, dirs, files in os.walk(_DIR):
        for file in files:
            Audio.append(f"{paths}{file}")

    return Audio


@app.route("/API/RandomAudio")
def ApiDls():
    role = int(request.args.get("role"))
    if role == 0:
        audio = random.choice(GetAudio("./static/hutao/audio/"))
    elif role == 1:
        audio = random.choice(GetAudio("static/dls/audio/"))
    else:
        return jsonify(
            {
                "code": 0,
                "audio": None,
                "illustrate": "?role=[角色数字] 0: 胡桃, 1: 德丽莎 "
            }
        )

    return jsonify(
        {
            "code": 1,
            "audio": "/"+audio
        }
    )



@app.get("/share")
def share():
    filename = request.args.get("filename")
    if filename is not None:
        iFpath = "static/share/"+filename

        if os.path.isfile(iFpath):
            return send_file(iFpath)
        else:
            return f"没有找到文件：{filename}"

    return """
        <h1 style="text-align: center;color: red;">
            参数错误
        </h1>
    """


@app.route("/API/PixivImage")
def PixivImage():
    return jsonify(
        {
            "url": GetPixivImage.GetImageUrl(
                random.choice(
                    GetPixivImage.GetRanking()
                )
            )
        }
    )


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8990,
        debug=True
    )
