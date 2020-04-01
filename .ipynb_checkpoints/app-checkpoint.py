import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
from flask import Flask, render_template, request
import numpy as np
import cv2
np.set_printoptions(precision=10,suppress=True)
from tensorflow.keras.models import load_model

model= load_model("./Model/model")


def predict(path):
    img=cv2.imread(path)
    img=cv2.resize(img,(100,100))
    try:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    except:
        img=img
        
    
    img=img.reshape(-1,100,100,1)
    preds=model.predict(img)[0]
    preds=preds*100
    
    
    
    
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('/Templates/home.html')


@app.route('/predict', methods=['POST'])
def predict():
	try:
		pn=str()
		path=str(request.form.get('path'))
		
        pred=predict(path)

		return render_template('/Templates/home.html', covid_text=pred,  pneumonia_text=pred,  normal_text=pred)
	except:
		return render_template('/Templates/home.html')




if __name__ == '__main__':
    app.run(debug=True)
    

