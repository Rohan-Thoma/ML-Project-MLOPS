from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app=application

## route for homepage
@app.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender= str(request.form.get('gender')),
            race_ethnicity=str(request.form.get("race_ethnicity")),
            parental_level_of_education=str(request.form.get("parental_level_of_education")),
            lunch=str(request.form.get("lunch")),
            test_preparation_course=str(request.form.get("test_preparation_course")),
            reading_score= int(request.form.get("reading_score", 0)),
            writing_score= int(request.form.get('writing_score', 0))
        )

        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        return render_template('home.html', results= results[0])
    
if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)