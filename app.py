import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from Modules import InputOps

app = Flask(__name__)

@app.route('/') #index or landing page of website
def home():
    return render_template('index1.html',input_value='')
# 127.0.0.1:8080/predict
@app.route('/predict',methods=['POST']) #post method is used to send parameters in http request
def predict():
    '''
    For rendering results on HTML GUI'''
    #int_features = [int(x) for x in request.form.values()]
    df = pd.DataFrame([request.form.to_dict()])
    
    print(df.head())
    prediction = InputOps.transForm(df)
    output = float(prediction)*100
    #output =10
    return render_template('index1.html', input_value=output)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=9000) # Remote Server
    #app.run(host="127.0.0.1",port=9000) # local machine