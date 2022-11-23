from __future__ import division, print_function
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image 
from tensorflow.keras.models import load_model
from flask import Flask, request, render_template,url_for
from werkzeug.utils import secure_filename
import cv2
import smtplib
from twilio.rest import Client

global graph
app = Flask(__name__)
model = load_model('forest1 (2).h5')


print('Model loaded. Check http://127.0.0.1:5000/')




@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('digital.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        img = image.load_img(file_path, target_size=(64,64))
        
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        
        #with graph.as_default():
        preds = np.argmax(model.predict(x))
        index = ["forest","with fire"]
        print(preds)
        text = index[preds]
        return text
        
@app.route('/video', methods=['GET', 'POST'])
def opencv():
    video = cv2.VideoCapture(0)
    name = ['forest','with fire']
        
    while(1):
        success, frame = video.read()
        cv2.imwrite("image.jpg",frame)
        img = image.load_img("image.jpg",target_size = (64,64))
        x  = image.img_to_array(img)
        x = np.expand_dims(x,axis = 0)
        pred=np.argmax(model.predict(x),axis=1)
        #pred = model.predict_classes(x)
        pred=model.predict(x)
        #p = pred[0]
        p=int(pred[0][0])
        print(pred)
        #cv2.putText(frame, "predicted  class = "+str(name[p]), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)
        
        
        pred = model.predict(x)
        pred=np.argmax(model.predict(x),axis=1)
        print(pred)
        #cv2.putText(frame, "predicted  class = "+str(name[pred]), (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)
        if pred[0]==1:
            
            cv2.putText(frame, "predicted  class = Fire Detected" ,(100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)
            account_sid = 'AC7db15b986f289b8f4f894e5b5017ee83'
            auth_token = 'fa990be8b020760d74e76ec3bf56490c'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                messaging_service_sid='MG850cc8d4d19f095137c2bd6457ca00fe',
             body='alert fire is detected',
             to='+918499882843'  ) 
            print(message.sid)
        
            print('Fire Detected')
            print ('SMS sent!')
            #return 'Fire Detected'
            return render_template('video.html',pred="Fire Detected Alert Notification Sent")
            break
        else:
            cv2.putText(frame, "predicted  class = No Danger",(100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)
            print("no danger")
           #break
        cv2.imshow("image",frame)
       
        if cv2.waitKey(1) & 0xFF == ord('a'): 
            break

    video.release()
    cv2.destroyAllWindows()
    return render_template('digital.html')

if __name__ == '__main__':
    app.run(threaded = False)

