import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
from flask import Flask, render_template, request
import numpy as np
import cv2
import webbrowser
from threading import Timer


from tensorflow.keras.models import load_model

import tensorflow as tf
np.set_printoptions(precision=16,suppress=True)


def predictit(path):
    
    global graph

    graph = tf.get_default_graph()



    model= load_model("./Model/model")

    img=cv2.imread(path)
    img=cv2.resize(img,(100,100))
    try:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    except:
        img=img
        
    
    img=img.reshape(-1,100,100,1)

    with graph.as_default():
        preds = model.predict(img)[0]

    return preds*100
    
    
    
    
app = Flask(__name__)

@app.route('/')
@app.route('/home')

def home():
    images=os.listdir("input")
    return render_template('home.html',imgs=images)
def open_browser():
  webbrowser.open_new('http://127.0.0.1:5000/')


@app.route('/predict', methods=['POST'])
def predict():
    pn=request.form.get('Name')
    img_name=request.form.get('images')
    path=os.path.join("input",img_name)
    print(path)
    pred=predictit(path)
    print(pred)
    images=os.listdir("input")
    return render_template('home.html',pname=pn ,imgs=images,covid_text=str(pred[2]) ,show_img=img_name, pneumonia_text=str(pred[1]),  normal_text=str(pred[0]))





if __name__ == '__main__':
    Timer(1, open_browser).start();
    app.run(debug=True)
    

