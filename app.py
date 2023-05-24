from flask import Flask,render_template,request,redirect,url_for,flash
from flask_cors import CORS
from  keras.models import load_model
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
from flask import Flask, request, jsonify

model = load_model(r"D:\chatbotInterface\chat\chatbot_model.h5")
import json
import random
intents = json.loads(open(r"D:\chatbotInterface\chat\faqData.json").read())
words = pickle.load(open(r"D:\chatbotInterface\chat\words.pkl",'rb'))
classes = pickle.load(open(r"D:\chatbotInterface\chat\classes.pkl",'rb'))
app=Flask(__name__,template_folder='template')

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words
# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words) 
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))
def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['faqData']
    for i in list_of_intents:
        if(i['label']== tag):
            result = random.choice(i['reply'])
            break
    return result
def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res

    

# @app.route('/')
# def home():
#     return render_template('faq.html')



app = Flask(__name__)

@app.route('/bot')
def bot():
    user_message = request.args.get('message','')
    # Process the user message and generate a bot response
    response=chatbot_response(user_message)
    return jsonify({'message': response})


if __name__=='__main__':
    app.run(debug=True)