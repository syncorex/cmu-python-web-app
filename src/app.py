from typing import Any
from flask import Flask, render_template, redirect, request, url_for, session
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.server_api import ServerApi
import requests
import random
import html
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'BLABLABLA'

cert_path = '/home/user/advpy-web-app/X509-cert-8255257794010601158.pem'

uri = 'mongodb+srv://cluster0.j9gqkfd.mongodb.net/' \
      '?authSource=%24external' \
      '&authMechanism=MONGODB-X509&' \
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
leaderboard_collection: Collection[Any]
leaderboard_collection = db['leaderboard']
doc_count = collection.count_documents({})


def submit_score(user_id, score):
    """Submit user score to the leaderboard."""
    leaderboard_collection.insert_one({'user_id': user_id, 'score': score, 'timestamp': datetime.utcnow()})


def get_top_scores(limit=10):
    """Get top scores from the leaderboard."""
    top_scores = leaderboard_collection.find().sort('score', -1).limit(limit)
    return list(top_scores)


def get_user_position(user_id):
    """Get the position of a user in the leaderboard."""
    user_position = leaderboard_collection.count_documents({'user_id': user_id})
    return user_position + 1  # Adding 1 to make it 1-based index


@app.route('/')
def index() -> str:
    """Render the index page."""
    return render_template('index.html')


@app.route('/start', methods=['GET', 'POST'])
def start() -> Any:
    """Start the trivia game."""
    if request.method == 'POST':
        # Handle the form submission here
        user_name = request.form.get('user_name')
        session['user_name'] = user_name
        session['score'] = 0

        res = requests.get('https://opentdb.com/api.php?amount=10').json()
        qs = list()

        for q in res['results']:
            q['correct_answer'] = html.unescape(q['correct_answer'])
            for r in q['incorrect_answers']:
                r = html.unescape(r)
            q['options'] = q['incorrect_answers']
            q['options'].insert(random.randint(0, len(q['incorrect_answers'])),
                                q['correct_answer'])
            q['question'] = html.unescape(q['question'])
            qs.append(q)

        session['questions'] = qs

        return redirect(url_for('question', question_number=0))
    else:
        return render_template('name_form.html')


@app.route('/end')
def end() -> Any:
    """End the trivia game and display the leaderboard."""
    submit_score(session['user_name'], session['score'])
    top_scores = get_top_scores()
    user_position = get_user_position(session['user_name'])
    return render_template('end.html', score=session['score'], top_scores=top_scores, user_position=user_position)


@app.route('/leaderboard')
def show_leaderboard() -> Any:
    """Display the leaderboard page."""
    top_scores = get_top_scores()
    return render_template('leaderboard.html', top_scores=top_scores)


@app.route('/question/<int:question_number>', methods=['GET', 'POST'])
def question(question_number: int) -> Any:
    """Display a trivia question."""
    questions = session['questions']

    if request.method == 'POST':
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
        user_position = get_user_position(session['user_name'])
        return render_template('question.html',
                               score=session['score'],
                               question_number=question_number,
                               question_text=question_data['question'],
                               options=question_data['options'],
                               user_position=user_position)

    return redirect(url_for('end'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
