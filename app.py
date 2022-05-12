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
    # return jsonify(data[name]['imgid_to_annos'][int(img_id)])


# # with open("../data/test/annotations/instances_val2017.json","r") as f:
# #     test=json.load(f)

# # i2c={item["id"]:item['name'] for item in test["categories"]}
# # with open("../data/test/annotations/instances_val2017.json","r") as f:
# #     test_images=json.load(f)['images']
# # print(f"loaded {len(test_images)} test images")

# # with open("../data/train/annotations/instances_train2017.json","r") as f:
# #     trainjson=json.load(f)
# #     train_images=trainjson['images']
# #     train_ann=trainjson['annotations']
# # print(f"loaded {len(train_images)} test images")

# # result_json_path="swinb_morescale_morenms.bbox.json"
# # result_json_path="../submit_research/result_morenms_remove_weird_and_duplicate.json"
# result_json_path="/data/ali/submit_research/fuckfuckfuckfuck.json"
# # result_json_path="/data/ali/submit_research/fucked_swinb_all_icon_mstrain_pipline_anchor_ALL.json"
# with open(result_json_path,"r") as f:
#     result=json.load(f)
# print(f"loaded {len(result)} results from {result_json_path}")

# print("construct id2result dict....")
# id2result={img['id']:[] for img in test_images}

# id2img={img['id']:img for img in test_images}
# for item in result:
#     id2result[item['image_id']].append(item)

# id2trainbox={img['id']:[] for img in train_images}
# for item in train_ann:
#     item['score']=0
#     id2trainbox[item['image_id']].append(item)

# id2trainimg={img['id']:img for img in train_images}


# # result_json_pathb="/data/ali/submit_research/detetors_all_icon_mstrain_pipline_anchor_ALL.bbox.json"
# # result_json_pathb="/data/ali/submit_research/result_01vote_morenms_remove_weird.json"
# # result_json_pathb="/data/ali/submit_research/fucktianchi.json"

# result_json_pathb="/data/ali/submit_research/hybird_fucktianchi_01vote_leak_removed_0_2.json"
# # result_json_pathb="/data/ali/submit_research/final_510_hybird_swin_resnext_mstrain_all_icon_pipline_anchor_ALL_norepeat_nogc_morescale.bbox.json"
# with open(result_json_pathb,"r") as f:
#     resultb=json.load(f)
# print(f"b:loaded {len(resultb)} results from {result_json_pathb}")

# print("b:construct id2result dict....")
# id2resultb={img['id']:[] for img in test_images}

# id2imgb={img['id']:img for img in test_images}
# for item in resultb:
#     id2resultb[item['image_id']].append(item)



# # result_json_pathc="/data/ali/mmdetection/swinb_morescale_all_icon_mstrain_pipline_anchor_ALL.bbox.json"
# # result_json_pathc="/data/ali/submit_research/result_morenms_remove_more_duplicate_099.json"
# # result_json_pathc="/data/ali/submit_research/ratio_removed_5_and_0.99_duplicated.json"
# # result_json_pathc="/data/ali/submit_research/ratio_removed_5_and_0.8_duplicated.json"
# # result_json_pathc="/data/ali/submit_research/ratio_removed_5_and_0.8_duplicated_debug.json"
# # result_json_pathc="/data/ali/submit_research/ratio_removed_5_and_0.7_duplicated.json"
# # result_json_pathc="/data/ali/submit_research/510final_epoch15_softnms.bbox.json"
# result_json_pathc="/data/ali/submit_research/hybird_swin_resnext_mstrain_all_icon_pipline_anchor_ALL_norepeat_nogc_morescale15.bbox.json"
# # result_json_pathc="/data/ali/submit_research/hybird_swin_resnext_mstrain_all_icon_pipline_anchor_ALL_norepeat_nogc_morescale15.bbox.json"
# with open(result_json_pathc,"r") as f:
#     resultc=json.load(f)
# print(f"c:loaded {len(resultc)} result from {result_json_pathc}")

# print("c:construct id2result dict....")
# id2resultc={img['id']:[] for img in test_images}

# id2imgc={img['id']:img for img in test_images}
# for item in resultc:
#     id2resultc[item['image_id']].append(item)



# result_json_pathd="/data/ali/submit_research/508_063source_confidence_great9.json"
# with open(result_json_pathd,"r") as f:
#     resultd=json.load(f)
# print(f"c:loaded {len(resultd)} results from {result_json_pathd}")

# print("c:construct id2result dict....")
# id2resultd={img['id']:[] for img in test_images}

# id2imgd={img['id']:img for img in test_images}
# for item in resultd:
#     id2resultd[item['image_id']].append(item)








# @app.route("/getannosa/<id>")
# def get_anno_by_id(id):
#     t=id2result[int(id)]
#     return render_template("index.html",
#                             imgid=int(id),
#                             image_path="images/"+id2img[int(id)]['file_name'],
#                             image_width=id2img[int(id)]['width'],
#                             image_height=id2img[int(id)]['height'],
#                             annos=sorted(t,key=lambda x:x["score"],reverse=True))



# @app.route("/getannosb/<id>")
# def get_anno_by_idb(id):
#     t=id2resultb[int(id)]
#     return render_template("index.html",
#                             imgid=int(id),
#                             image_path="images/"+id2imgb[int(id)]['file_name'],
#                             image_width=id2imgb[int(id)]['width'],
#                             image_height=id2imgb[int(id)]['height'],
#                             annos=sorted(t,key=lambda x:x["score"],reverse=True))



# @app.route("/getannosc/<id>")
# def get_anno_by_idc(id):
#     t=id2resultc[int(id)]
#     print(t)
#     return render_template("index.html",
#                             imgid=int(id),
#                             image_path="images/"+id2imgc[int(id)]['file_name'],
#                             image_width=id2imgc[int(id)]['width'],
#                             image_height=id2imgc[int(id)]['height'],
#                             annos=sorted(t,key=lambda x:x["score"],reverse=True))

# @app.route("/getannosd/<id>")
# def get_anno_by_idd(id):
#     t=id2resultd[int(id)]
#     print(t)
#     return render_template("index.html",
#                             imgid=int(id),
#                             image_path="images/"+id2imgd[int(id)]['file_name'],
#                             image_width=id2imgd[int(id)]['width'],
#                             image_height=id2imgd[int(id)]['height'],
#                             annos=sorted(t,key=lambda x:x["score"],reverse=True))

# @app.route("/getannostrain/<id>")
# def get_anno_by_idtrain(id):
#     t=id2trainbox[int(id)]
#     print(t)
#     return render_template("index.html",
#                             imgid=int(id),
#                             image_path="train_image/images/"+id2trainimg[int(id)]['file_name'],
#                             image_width=id2trainimg[int(id)]['width'],
#                             image_height=id2trainimg[int(id)]['height'],
#                             annos=sorted(t,key=lambda x:x["score"],reverse=True))





@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
   app.run(host="10.112.13.120",debug=True)