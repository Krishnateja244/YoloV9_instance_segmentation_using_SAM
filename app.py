import argparse
from flask import Flask, render_template, request, redirect, send_file, url_for, Response
import os
import cv2
import subprocess

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index_cus.html')

    
@app.route("/", methods=["GET","POST"])
def predict_img():
    if request.method == "POST":
        if 'file' in request.files:
            f = request.files['file']
            basepath = os.path.dirname(__file__)
            filepath = os.path.join(basepath,'uploads',f.filename)
            print("upload folder is ", filepath)
            f.save(filepath)
            global imgpath
            predict_img.imgpath = f.filename
            print("printing predict_img :::::: ", predict_img)
                                               
            file_extension = f.filename.rsplit('.', 1)[1].lower() 
            
            cmd = ["python","./segment/predict.py", "--data","data/dataset.yaml","--img","1024","--conf","0.001","--iou","0.7", \
                   "--weights","./E:/yolov9/runs/train-seg/gelan-c-seg-1024/weights/best.pt", \
                   "--source",filepath,"--max-det","15"]
            subprocess.run(cmd)
                
    folder_path = 'runs/predict-seg'
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]    
    latest_subfolder = max(subfolders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))    
    image_path = folder_path+'/'+latest_subfolder+'/'+f.filename 
    # return render_template('index_cus.html', image_path=image_path)
    return send_file(image_path, mimetype='image/png')

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov9 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port) 