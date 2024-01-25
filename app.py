# app.py

from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

with open('extratrees_model.pkl', 'rb') as model_file:
    extratrees_model = pickle.load(model_file)

with open('grad_boost_model.pkl', 'rb') as model_file:
    grad_boost_model = pickle.load(model_file)

def process_uploaded_file(file):
    try:
        uploaded_data = pd.read_csv(file, sep="|")
        
        required_columns = ['Name', 'md5', 'legitimate']
        missing_columns = list(set(required_columns) - set(uploaded_data.columns))
        
        if missing_columns:
            raise Exception(f"Missing columns in the uploaded file: {missing_columns}")
        
        uploaded_data.fillna(0, inplace=True)
        
        uploaded_data = uploaded_data.apply(pd.to_numeric, errors='coerce')
        
        data_in = uploaded_data.drop(required_columns, axis=1).values
        
        return data_in
    except Exception as e:
        raise Exception(f"Error during file processing: {e}")
    

def detect_malware(data):
    return "Malware detection result"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            try:
                data_in = process_uploaded_file(file)
                result = detect_malware(data_in)
                return render_template('index.html', result=result)
            except Exception as e:
                return render_template('index.html', error=f"Error during prediction: {str(e)}")

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
