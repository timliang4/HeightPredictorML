from flask import Flask
from flask import request
import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
import __main__
setattr(__main__, "powerOfFour", lambda A: np.power(A, 4))

model = joblib.load("model.pkl")
app = Flask(__name__)

def predictHeight(fatherHeight, motherHeight, gender):
    data = pd.DataFrame({'father': [fatherHeight], 'mother': [motherHeight], 'male': [float(gender == 'M')], 'female': [float(gender == 'F')]})
    return model.predict(data)[0]

@app.route("/height")
def get_height():
    try:
        fatherHeight = float(request.args["father"])
        motherHeight = float(request.args["mother"])
        gender = request.args["gender"]
        if gender != 'M' and gender != 'F':
            raise Exception("invalid gender")
        return {'height': predictHeight(fatherHeight, motherHeight, gender)}
    except:
        return {'height': 'invalid parameters'}
