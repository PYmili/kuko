# [kuko](https://www.kuko.icu)

![kuko.ico](/static/index/images/favicon.ico)

___

使用 **flask** 框架制作

## 功能

- index http://127.0.0.1:8990

    主页 (/templates/index.html) 静态资源 (/static/index/*)

- 10_12

  None

- API

  - RandomAudio
    ```http://127.0.0.1:8990/API/RandomAudo?role=xxx```
    
    静态资源 (/static/)
  
  - share
  
    ```
    共享 /static/share下所有文件
     http://127.0.0.1:8990/share?filename=xxx
    ```
  
  - PixivImage http://127.0.0.1:8990/API/PixivImage
    
    随机返回一个P站图片

## 使用

```
pip install -r requirements.txt
```

```
python app.py
```

建议使用nginx反向代理域名
