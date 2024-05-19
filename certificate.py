import cv2
import qrcode
import numpy as np
import sys
from fastapi import FastAPI

app = FastAPI()

@app.post('/certificate')
def certificate():
    data = request.json
    link = data['link']
    date = data['date']
    name = data['name']
    my_list = name
    for index, name in enumerate(my_list):
        template = cv2.imread('../../static/certi.jpg')
        text = name
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
        text_x = (template.shape[1] - text_size[0]) // 2
        text_y = (template.shape[0] + text_size[1]) // 2
        cv2.putText(template, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
        qr_img = qrcode.make(link)
        qr_img = np.array(qr_img.convert('RGB'))
        qr_img = cv2.cvtColor(qr_img, cv2.COLOR_RGB2BGR)
        qr_img = cv2.resize(qr_img, (100, 100))
        qr_x = template.shape[1] - qr_img.shape[1] - 350
        qr_y = template.shape[0] - qr_img.shape[0] - 80  
        template[qr_y:qr_y + qr_img.shape[0], qr_x:qr_x + qr_img.shape[1]] = qr_img
        cv2.imwrite('../../static/certificate.jpg', template)