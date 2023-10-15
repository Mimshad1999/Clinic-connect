from flask import Flask, request, url_for, redirect, render_template
from flask import Flask
from flask import render_template,jsonify
from flask import request
import pymongo
import os
import requests
import json
from flask import Flask, flash, request, redirect, url_for,session
import pickle

import numpy as np

app = Flask(__name__, template_folder='./templates', static_folder='./static')
client=pymongo.MongoClient("mongodb://localhost:27017/")
db=client['Msaad']
Doctors=db['Doctors']
Query=db['Query']

Pkl_Filename = "rf_tuned.pkl" 
with open(Pkl_Filename, 'rb') as file:  
    model = pickle.load(file)
@app.route('/')

def hello_world():
    return render_template('home.html')
@app.route('/Home')

def Home():
    return render_template('home.html')
@app.route('/doctorRecommend')

def doctorRecommend():
    return render_template('doctorRecommend.html')

@app.route('/submit',methods=['get','POST'])
def Submit():
    print("hello")
    if request.method=='POST':
       data= request.form.to_dict()
       print(data)
       res=Doctors.find({'type':data['section']})
       print(res)
       print(data['section'])
       return render_template('doctorRecommend.html',res=res)
    # return render_template('doctorRecommend.html')
@app.route('/query',methods=['POST','GET'])
def query():
    if request.method=='POST':
       data= request.form.to_dict()
       print(data)
       res=Query.insert_one(data)
    return render_template('query.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    features = [int(x) for x in request.form.values()]

    print(features)
    final = np.array(features).reshape((1,6))
    print(final)
    pred = model.predict(final)[0]
    print(pred)

    
    if pred < 0:
        return render_template('op.html', pred='Error calculating Amount!')
    else:
        return render_template('op.html', pred='Expected amount is {0:.3f}'.format(pred))

if __name__ == '__main__':
    app.run(debug=True)