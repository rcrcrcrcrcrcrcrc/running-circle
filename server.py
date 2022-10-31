from ctypes.wintypes import LANGID
from flask import Flask, render_template,url_for, request
from werkzeug.utils import secure_filename
import urllib3
import json
import base64
import matplotlib.pyplot as plt
from PIL import Image
from googletrans import Translator
import time
import os
import json
from functools import reduce


app = Flask(__name__)

# 파일 업로드 창 template
def template(content, id=None):
    if id != None:
        contextUI = f'''
        <div class="intro"> <!-- 로그인&회원가입, 목록 -->
                    <div class="intro1">
                        <div class="name">
                            <h1><a id=info href="/">L.L.P</a></h1>
                        </div>
                    </div>
                </div>

            <div class="information_list">
                <div id="grid">
                <ol>
                    <h3><li><a>번역</a></li></h3><br>
                    <h3><li><a>위키백과</a></li></h3>
                </ol>
                    <div>
                <!--<h2 style="text-align:center;"><a style="border:3px solid; padding:5px;"></a></h2>-->'''
    return f'''<!doctype html>
<!doctype html>
<html lang="eng">
    <head>
        <link href="https://fonts.googleapis.com/css?family=Noto+Sans+KR&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="{url_for('static',filename='css/upload.css')}">

        <title> 코딩 만재들 </title>
        <meta charset="utf-8">

    </head>
    <body>
        <div class="wrap">
        {contextUI}
        {content}
                    </div>
                </div>
              </div>
          </div>
            </div>
        </div>
    </body>
</html>
'''

# id 값을 이용하여 무슨 언어로 번역할지 받아옴
# 영어: en, 한국어:ko, 일본어:jp, 중국어: zh-cn
def onclick(id):
    accessKey = "468252bc-5e0c-4871-a70c-1ccd230831f0"
    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
    dir_path='./static/upload'
    file_list = os.listdir(dir_path)
    imageFilePath = dir_path + '/' + file_list[0]
    #imageFilePath ="./static/upload/image2.jpg"
    filname=os.path.basename(imageFilePath)
    #print("filename::::::::::::"+filname)
    ext=os.path.splitext(filname)[-1]
    s = reduce(lambda x, y: str(x) + str(y), ext, '')
    ext1=s.split('.')[-1]
    #print("확장자:::: ",ext1)
    type = ext1
    #type='jpg'
    
    file = open(imageFilePath, "rb")
    imageContents = base64.b64encode(file.read()).decode("utf8")
    file.close()
    requestJson = {
        "access_key": accessKey,
        "argument": {
            "type": type,
            "file": imageContents
        }
    }
    
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    
    #print("[responseCode] " + str(response.status))
    #print("[responBody]")
    #print(response.data)
    #print("\n")


    #img_test = Image.open(imageFilePath)
    #plt.imshow(img_test)
    #plt.show()

    result=str(response.data,"utf-8")
    #print(result)
    d = json.loads(result)
    
    try:
        count=len(d['return_object']['data'])
        print(count)

        name = []
        classname = []
        translator = Translator()

        for i in range(count):
            text = d['return_object']['data'][i]['class']

            if id == "ko":
                trans = translator.translate(text, src='en', dest='ko')
                name.append(trans.text)
                classname.append(trans.text)
        
            elif id == "en":
                trans = text
                trans_2 = translator.translate(text, src='en', dest='ko')
                classname.append(trans)
                name.append(trans_2.text)

            elif id == "ja":
                trans = translator.translate(text, src='en', dest='ja')
                trans_2 = translator.translate(text, src='en', dest='ko')
                classname.append(trans.text)
                name.append(trans_2.text)

            elif id == "zh-cn":
                trans = translator.translate(text, src='en', dest='zh-cn')
                trans_2 = translator.translate(text, src='en', dest='ko')
                classname.append(trans.text)
                name.append(trans_2.text)           


            #name.append(d['return_object']['data'][i]['class'])
            #print(d['return_object']['data'][i]['class'])   

        print(classname)

        #객체 탐지된 class 한글로 번역해서 리스트로 저장 완료

        #--------------------QA-----------------------

        openApiURL = "http://aiopen.etri.re.kr:8000/WikiQA"
        accessKey = "468252bc-5e0c-4871-a70c-1ccd230831f0"

        for i in range(len(name)):
            question = name[i]
            type = "hybridqa"
        
            requestJson = {
            "access_key": accessKey,
            "argument": {
                "question": question,
                "type": type
            }
            }
        
            http = urllib3.PoolManager()
            response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
            )
        
            print("[responseCode] " + str(response.status))
            print("[responBody]")
            wiki_result=(str(response.data,"utf-8"))
            #print(wiki_result)
            json_return=json.loads(wiki_result)
            print(json_return['return_object']['WiKiInfo']['AnswerInfo'][0]['answer'])
            dump = json_return['return_object']['WiKiInfo']['AnswerInfo'][0]['answer']

            c = []

            if id == "ko":
                s = dump
                c.append(s)
            elif id == "en":
                s = translator.translate(dump, src='ko', dest='en')
                c.append(s.text)
            elif id == "ja":
                s = translator.translate(dump, src='ko', dest='ja')
                c.append(s.text)
            elif id == "zh-cn":
                s = translator.translate(dump, src='ko', dest='zh-cn')
                c.append(s.text)

        return classname, c
    except:
        return '읽히는 값이 없습니다'

## 폴더에 파일이 있다면 파일 삭제
def file_list():
    dir_path='./static/upload'
    file_list = os.listdir(dir_path)
    if os.path.exists(dir_path):
        for file in os.scandir(dir_path):
            os.remove(file.path)

# 메인 화면
@app.route('/')
def index():
    file_list()
    return render_template('main.html')


# 업로드 HTML 렌더링
@app.route('/upload/<string:id>')
def read(id):
    file_list()
    content=f'''
        <form action = "http://localhost:5000/fileUpload/{id}" method = "POST" enctype = "multipart/form-data">
        <input type = "file" name = "file" />
        <input type = "submit" />
        </form>'''
    return template(content, id)


# 선택한 언어를 id값으로 받아와서 번역 API에 넣음
@app.route('/fileUpload/<string:id>', methods = ['GET', 'POST'])
def read1(id):
    if request.method == 'POST':
        f = request.files['file']
        # 사진을 저장할 경로 + 파일명
        f.save("./static/upload/"+secure_filename(f.filename))
        time.sleep(1)
        try:
            name, value = onclick(id)
        except:
            return 'error'
        # 업로드한 파일을 결과창에 보여주기 위한 파일 주소
        path='./upload'
        dir_path='./static/upload'
        file_list = os.listdir(dir_path)
        img_name = path + '/' + file_list[0]
        return render_template('index.html',imagename=img_name, name=name, value=value)


if __name__ == '__main__':
    # 서버 실행
    app.run(debug = True)

