import urllib3
import json
import base64
import matplotlib.pyplot as plt
from PIL import Image
from googletrans import Translator
import os



def onclick():
    accessKey = "4154e7c7-e458-4031-b34b-4b871669a8ff"
    openApiURL = "http://aiopen.etri.re.kr:8000/ObjectDetect"
    imageFilePath = file_path
    type = "jpg"
    
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
    count=len(d['return_object']['data'])
    print(count)

    name = []
    translator = Translator()

    for i in range(count):
        text = d['return_object']['data'][i]['class']
        trans = translator.translate(text, src='en', dest='ko')
        name.append(trans.text)


        #name.append(d['return_object']['data'][i]['class'])
        #print(d['return_object']['data'][i]['class'])   

    print(name)

    #객체 탐지된 class 한글로 번역해서 리스트로 저장 완료

    #--------------------QA-----------------------

    openApiURL = "http://aiopen.etri.re.kr:8000/WikiQA"
    accessKey = "4154e7c7-e458-4031-b34b-4b871669a8ff"

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
        