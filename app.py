from flask import Flask, render_template, request
import pickle
import numpy as np
import sklearn

model = pickle.load(open('model_1.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict_placement():
    carlength = float(request.form.get('carlength'))
    carwidth = float(request.form.get('carwidth'))
    carheight = float(request.form.get('carheight'))
    enginesize = float(request.form.get('enginesize'))
    horsepower = float(request.form.get('horsepower'))
    peakrpm = float(request.form.get('peakrpm'))

    print("Input Data:", [carlength, carwidth, carheight, enginesize, horsepower, peakrpm])

    result = model.predict(np.array([carlength, carwidth, carheight, enginesize, horsepower, peakrpm]).reshape(1, 6))

    print("Prediction:", result)

    return str(result[0])

if __name__ == '__main__':
    app.run(debug = True)


