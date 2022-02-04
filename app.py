from flask import Flask, request, render_template
import logging
import os
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

app = Flask(__name__)

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        logging.basicConfig(filename='All_logs/Testing_logs.log',
                            filemode='w',
                            level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(module)s---- %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logger = logging.getLogger('')
        f = open('All_logs/Testing_logs.log', 'w')
        f.truncate()

        text = request.form.get('message')

        transformed_sms = transform_text(text)

        vector_input = tfidf.transform([transformed_sms])

        results = model.predict(vector_input)[0]

        if results == 1:
            results = "Yes it is a Spam Message"
        else:
            results = 'No it is not a spam message'
        return render_template('index.html', prediction=results)

    else:
        return render_template('index.html')



port = int(os.getenv("PORT", 5000))
if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5121
    app.run(host=host, port=port)
