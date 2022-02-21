from flask import Flask, request
from flask import render_template
import os,json,tweepy
from deep_translator import GoogleTranslator
from textblob import TextBlob
from bs4 import BeautifulSoup

app = Flask(__name__)

_port = os.environ.get('PORT', 5000)

@app.route('/')
def index():
    data = {"a":"1234"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/twits')
def twits():
    word = "millos"
    cantidad = 10
    client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAAaNYwEAAAAAZ9%2Bw4m2IzGYfdrpNT%2FF8RBvNHRY%3DMaZm6FLYw2uI34yKfjaz6ZUpUyZcWKU70OKx4RvMWdLDLUphOj')
    query = f'{word} -is:retweet'
    l_twits = []
    positivos_t = []
    negativos_t = []
    neutrales_t = []
    positivos = 0
    negativos = 0
    neutrales1 = 0
    subjetivos_p = 0
    subjetivos_n = 0
    subjetivos_ne = 0
    objetivos_p = 0
    objetivos_n = 0
    objetivos_ne = 0
    neutrales_p = 0
    neutrales_n = 0
    neutrales_ne = 0
    traductor = GoogleTranslator(source='es', target='en')
    for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
    tweet_fields=['context_annotations', 'created_at'], max_results=10).flatten(limit=cantidad):
        print(str(type(tweet.data)))
        print(tweet.data)
        datos = dict(tweet.data)
        datos_t = traductor.translate(datos['text'])
        polaridad = ""
        subjetividad = ""
        analisisPol = TextBlob(datos_t).polarity
        analisisSub = TextBlob(datos_t).subjectivity
        if analisisPol > 0:
            positivos_t.append(datos['text'])
            polaridad = "Positiva"
            positivos += 1
            if analisisSub > 0:
                subjetivos_p += 1
            if analisisSub == 0:
                neutrales_p += 1
            if analisisSub < 0:
                objetivos_p += 1
        if analisisPol == 0:
            polaridad = "Neutral"
            neutrales_t.append(datos['text'])
            neutrales1 += 1
            if analisisSub > 0:
                subjetivos_ne += 1
            if analisisSub == 0:
                neutrales_ne += 1
            if analisisSub < 0:
                objetivos_ne += 1
        if analisisPol < 0:
            polaridad = "Negativa"
            negativos_t.append(datos['text'])
            negativos += 1
            if analisisSub > 0:
                subjetivos_n += 1
            if analisisSub == 0:
                neutrales_n += 1
            if analisisSub < 0:
                objetivos_n += 1
        
        print(datos['text'])
        di = {'text':datos['text'],'polaridad':polaridad,'subjetividad':subjetividad}
        
        l_twits.append(di)
    data_g = [{'sentimiento':'positivos','valor':positivos,'subjetivos':subjetivos_p,'neutrales':neutrales_p,'objetivos':objetivos_p},
    {'sentimiento':'neutrales','valor':neutrales1,'subjetivos':subjetivos_ne,'neutrales':neutrales_ne,'objetivos':objetivos_ne},
    {'sentimiento':'negativos','valor':negativos,'subjetivos':subjetivos_n,'neutrales':neutrales_n,'objetivos':objetivos_n}]
    chart = pygal.Bar()
    value_list = [x['valor'] for x in data_g]
    chart.add('Sentimientos',value_list)
    chart.x_labels = [x['sentimiento'] for x in data_g]

    subjetividad_list = [x['subjetivos'] for x in data_g]
    chart.add('Subjetividad',subjetividad_list)

    neutralidad_list = [x['neutrales'] for x in data_g]
    chart.add('Neutralidad',neutralidad_list)

    objetividad_list = [x['objetivos'] for x in data_g]
    chart.add('Objetividad',objetividad_list)
    data = {
        "positivos":positivos_t,
        "neutrales":neutrales_t,
        "negativos":negativos_t,
        "subjetividad":subjetividad_list,
        "neutralidad":neutralidad_list,
        "objetividad":objetividad_list
    }
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=_port)