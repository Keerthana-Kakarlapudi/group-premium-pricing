from prem_calc import premium_pricing
from model import model_obj
from preprocessing import PreProcess
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import pandas as pd

# creating an object of Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static')


# Home page
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('demo.html')


# Upload the group file
@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == "POST":
        f = request.files['file1']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    return render_template('demo.html', run=True)


# Premium calculation
@app.route('/run')
def pre_process():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.csv')]
    input_file_loc = os.path.join(app.config['UPLOAD_FOLDER'], files[0])
    input_df = pd.read_csv(input_file_loc)

    pp = PreProcess()
    df = pp.processing(pp.default(input_df))

    df2 = model_obj().predict_model(df)

    premObj = premium_pricing()
    premium = premObj.prem_calc(df2)
    premium2 = premObj.prem_calc(df2, extra_cover=2000)

    os.remove(input_file_loc)
    return render_template('demo.html', premium_value=premium, premium_value_2=premium2,
                           members=len(df2), run=True, complete=True)


if __name__ == "__main__":
    app.run(debug=True)
