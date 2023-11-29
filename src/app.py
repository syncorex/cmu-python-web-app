from typing import Any
from flask import Flask, render_template, redirect, request, url_for, session
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.server_api import ServerApi
import requests
import random
import html

app = Flask(__name__)
app.secret_key = 'BLABLABLA'

cert_path = '/home/user/advpy-web-app/X509-cert-8255257794010601158.pem'

uri = 'mongodb+srv://cluster0.j9gqkfd.mongodb.net/'\
      '?authSource=%24external'\
      '&authMechanism=MONGODB-X509&'\
      'retryWrites=true&w=majority'

client: MongoClient[Any]
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=cert_path,
                     server_api=ServerApi('1'))
db: Database[Any]
db = client['trivia']
collection: Collection[Any]
collection = db['questions']
doc_count = collection.count_documents({})
# print(doc_count)


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/start')
def start() -> Any:
    session['score'] = 0
    res = requests.get('https://opentdb.com/api.php?amount=10').json()
    # print(res)
    qs = list()
    for q in res['results']:
        q['options'] = q['incorrect_answers']
        q['options'].insert(random.randint(0, len(q['incorrect_answers'])),
                            q['correct_answer'])
        q['question'] = html.unescape(q['question'])
        qs.append(q)
    session['questions'] = qs
    # print(session['score'])
    return redirect(url_for('question', question_number=0))


@app.route('/end')
def end() -> Any:
    return render_template('end.html', score=session['score'])


@app.route('/question/<int:question_number>', methods=['GET', 'POST'])
def question(question_number: int) -> Any:

    if request.method == 'POST':
        questions = session['questions']
        user_answer = request.form['answer']
        correct_answer = questions[question_number]['correct_answer']
        if user_answer == correct_answer:
            session['score'] += 1
            result_message = "Correct!"
        else:
            result_message = "Wrong!"

        return render_template('result.html',
                               score=session['score'],
                               question_number=question_number,
                               correct_answer=correct_answer,
                               user_answer=user_answer,
                               result_message=result_message,
                               next_question_number=question_number + 1)

    if question_number < len(questions):
        question_data = questions[question_number]
        return render_template('question.html',
                               score=session['score'],
                               question_number=question_number,
                               question_text=question_data['question'],
                               options=question_data['options'])

    # If there are no more questions, redirect to the result page
    return redirect(url_for('index'))


if __name__ == "__main__":
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)