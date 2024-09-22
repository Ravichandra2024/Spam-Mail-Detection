import joblib
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
import nltk
from flask_cors import CORS  
from flask import *
app=Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
nltk.download('stopwords')
warnings.filterwarnings('ignore')
model=joblib.load("model.joblib")
vector=joblib.load("vectorizer.joblib")
port_stem = PorterStemmer()
def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]',' ',content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content
@app.route('/', methods=['GET'])
def index():
    param1 = request.args.get('message')
    p = stemming(param1)
    p = np.array([p])  
    p = vector.transform(p) 
    p = p.toarray()  
    prediction = model.predict(p)[0] 
    if prediction == 1:
        o = "spam"
    else:
        o = "good"
    return {'message': o}

if __name__ == '__main__':
    app.run()