import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
from calculator import math_expression_generator, caluclate
from utils import save_image, get_values
from flask import Flask, render_template, request
import base64
import numpy as np
from PIL import Image


app = Flask(__name__)

init_Base64 = 21


@app.route('/')
@app.route('/index')
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    draw = request.form['url']
    draw = draw[init_Base64:]
    draw_decoded = base64.b64decode(draw)
    image = np.asarray(bytearray(draw_decoded), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    save_image(image)
    image = Image.open("temp.jpg").convert("L")
    preds = get_values(image)
    equation = math_expression_generator(preds)
    final = caluclate(equation)
    return render_template(
        "output.html",
        entered=final[1],
        result=final[2],
        valid=final[0]
    )

if __name__ == "__main__":
    app.run(port = 9900)