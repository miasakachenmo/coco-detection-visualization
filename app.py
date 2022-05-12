from re import I
from flask import Flask, Response,render_template,jsonify,request,send_file,make_response
from flask_cors import CORS, cross_origin
import json
import os
import cv2
import base64
# from mim import test
app = Flask(__name__)

cors = CORS(app)
#这里定义数据集

images_path="static/images/"
with open("../data/test/annotations/instances_val2017.json","r") as f:
    _=json.load(f)
    test_images=_['images']
    categories=_['categories']
print(f"loaded {len(test_images)} test images")

id2img={img['id']:img for img in test_images}

data={}

json_names=os.listdir("./jsons")
for name in json_names:
    with open(f"./jsons/{name}",'r') as f:
        data[name]={
            'annotations':json.load(f)
        }
        items=data[name]['annotations']
        data[name]['imgid_to_annos']={img['id']:[] for img in test_images}
        for item in items:
            data[name]['imgid_to_annos'][item['image_id']].append(item)
print("load complete")
@app.route("/getcategories")
def get_categories():
    return jsonify(categories)

#获取所有json文件的名字
@app.route("/getnames")
def get_names():
    return jsonify(list(data.keys()))

@app.route("/getannos",methods=["POST"])
def get_annos():
    json_data = request.get_json()
    name=json_data["name"]
    img_id=json_data['img_id']
    return jsonify(   sorted(data[name]['imgid_to_annos'][int(img_id)],key=lambda x:x['score'],reverse=True)    )



@app.route("/getimg",methods=["GET","POST"])
def get_img():
    json_data = request.get_json()
    name=json_data["name"]
    img_id=json_data['img_id']
    img_dict=id2img[int(img_id)]
    file_path=images_path+img_dict['file_name']
    if img_dict.get("img",None) is None:
        img=cv2.imread(file_path)
        byte_img=cv2.imencode('.png', img)[1]
        image_code = str(base64.b64encode(byte_img))[2:-1]
        image_code="data:image/png;base64,"+image_code
        # array_bytes=img.tobytes()
        img_dict['img']=image_code
    # else:

    return make_response(img_dict
        # attachment_filename='result.jpg'
    )



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
   app.run(host="0.0.0.0",debug=True)