from flask import Flask, render_template, request, url_for, jsonify, Blueprint, g
import pickle  # or the appropriate library for loading your model
import string
from nltk.corpus import stopwords
import nltk
import sklearn
from nltk.stem.porter import PorterStemmer
from .extensions import db, Session
from .models import SMSMessage, Base
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


nltk.download('punkt')
nltk.download('stopwords')


#app = Flask(__name__)
main = Blueprint('main', __name__)

ps = PorterStemmer()

chichewa_stopwords = [
    "ndi",
    "mu",
    "a",
    "kuti",
    "ndine",
    # Add more Chichewa stopwords here
]

def transform_text(text):
     #Lowercase
    text = text.lower()
    
    #Tokenization
    text = nltk.word_tokenize(text)
    
    #alpha numerical values
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
            
    text = y[:]
    y.clear()
    
    #Removing stopwords
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
            
    text = y[:]
    y.clear()
    
    #Stemming
    for i in text:
        y.append(ps.stem(i))
    
    return " ".join(y)  
'''
user_ip = request.remote_addr
# Initialize the Flask Limiter
limiter = Limiter(
    main,
    key_func=get_remote_address,  # Use client IP address as the key
    storage_uri="memory://",  # Use in-memory storage (you can use other storage options)
    #app_limits=["2 per minute "]  # Define your rate limiting rules (e.g., 100 requests per minute per IP)
)
'''
#2 Loading model and vectorizer

tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))


@main.route("/")
def index():
    return render_template('/index.html')


#3 Getting text from user input
@main.route('/predict', methods=['POST'])
#@limiter.limit("2 per minute")
def predict():
    #session = Session()
    if request.method == 'POST':
        
        msg = request.form['textHere']

        preprocessed_sms = transform_text(msg)

        data = [preprocessed_sms]

        vect = tfidf.transform(data)[0]

        result = model.predict(vect)
    
    if result == 1:
        db_msg = 'smishing'
    else:
        db_msg = 'legit'
        '''
    new_message = SMSMessage(text=msg, result=db_msg)
    session.add(new_message)
    session.commit()
    session.close()
'''

#4. Display result on html page

    if result == 1:
        return render_template("/index.html", data="Smishing")
    else:
        return render_template("/index.html", data="Legit")



#Point for API documentation
@main.route('/API')
def API():
    return render_template('APIDocumentation.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/about')
def about():
    return render_template('about.html')

#API
@main.route('/detect', methods=['POST'])
def detect():
    #session = Session()
    data = request.get_json()
    
    if 'sms_message' not in data:
        return jsonify({'error': 'Missing "sms_message" field in the request'}), 400
        
    sms_message = data['sms_message']
    a = transform_text(sms_message)

    # Preprocess the SMS message
    preprocessed_sms = [a]

    vect = tfidf.transform(preprocessed_sms)
    
    # Make predictions using the pre-trained model
    prediction = model.predict(vect)
    
    result = "smishing" if prediction == 1 else "legit"
    '''
    # Store the SMS message and result in the database
    new_message = SMSMessage(text=sms_message, result=result)
    session.add(new_message)
    session.commit()
    session.close()
    '''
    return jsonify({'result': result})

if __name__ == '__main__':
    main.run(debug=True)
