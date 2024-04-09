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

cert_path = 'cert.pem'

uri = 'mongodb+srv://cluster0.j9gqkfd.mongodb.net/'\
      '?authSource=%24external'\
      '&authMechanism=MONGODB-X509'\
      '&retryWrites=true'\
      '&w=majority'\
      '&appName=Cluster0'

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


class Trivia:
    difficulty = {'easy': {'score': 30},
                  'medium': {'score': 40},
                  'hard': {'score': 50}}

    def getDifficultyValue(self, diff: str) -> int:
        val = self.difficulty[diff]['score']
        if val:
            return val
        else:
            return 1


trivia = Trivia()


def submit_score(user_id: str, score: int) -> None:
    """Submit user score to the leaderboard."""
    leaderboard_collection.insert_one(
        {'user_id': user_id, 'score': score, 'timestamp': datetime.utcnow()})


def get_top_scores(limit: int = 10) -> list[Any]:
    """Get top scores from the leaderboard."""
    top_scores = leaderboard_collection.find().sort('score', -1).limit(limit)
    return list(top_scores)


@app.route('/')
def index() -> str:
    """Render the index page."""
    return render_template('index.html')


@app.route('/start', methods=['GET', 'POST'])
def start() -> Any:
    session['score'] = 0
    session['difficulty'] = request.args.get('difficulty')

    api_url = 'https://opentdb.com/api.php?amount=10'
    if (session['difficulty'] in ['easy', 'medium', 'hard']):
        api_url += f"&difficulty={session['difficulty']}"

    res = requests.get(api_url).json()

    qs = list()
    for q in res['results']:
        q['correct_answer'] = html.unescape(q['correct_answer'])
        for i in range(len(q['incorrect_answers'])):
            q['incorrect_answers'][i] = html.unescape(
                q['incorrect_answers'][i])
        q['options'] = q['incorrect_answers']
        q['options'].insert(random.randint(0, len(q['incorrect_answers'])),
                            q['correct_answer'])
        q['question'] = html.unescape(q['question'])
        qs.append(q)
    session['questions'] = qs

    return redirect(url_for('question', question_number=0))


@app.route('/end', methods=['GET', 'POST'])
def end() -> Any:
    if request.method == 'POST':
        session['user_name'] = request.form['user_name']

        """Submit score to db and display the leaderboard."""
        submit_score(session['user_name'], session['score'])
        return redirect(url_for('leaderboard'))

    difficulty = 'test' if app.testing else session['difficulty']

    return render_template('end.html',
                           score=session['score'],
                           difficulty=difficulty)


@app.route('/leaderboard')
def leaderboard() -> Any:
    """Display the leaderboard page."""
    top_scores = get_top_scores()

    if not session.get('score'):
        session['score'] = 0

    return render_template(
        'leaderboard.html',
        score=session['score'],
        top_scores=top_scores,)


@app.route('/question/<int:question_number>', methods=['GET', 'POST'])
def question(question_number: int) -> Any:

    if app.testing:  # Set values for unit testing
        questions = [{"answer": "test",
                      "correct_answer": "test",
                      "question": "test",
                      "options": "test",
                      "difficulty": "easy"}]
        score = 0
    else:
        questions = session['questions']
        score = session['score']

    # If there are no more questions, redirect to the result page
    if question_number >= len(questions):
        return redirect(url_for('end'))

    question_data = questions[question_number]
    question_value = trivia.getDifficultyValue(question_data['difficulty'])

    if request.method == 'POST':
        if 'answer' not in request.form:
            return redirect(
                url_for(
                    'question',
                    question_number=question_number))

        user_answer = request.form['answer']

        correct_answer = question_data['correct_answer']
        if user_answer == correct_answer:
            score += question_value
            if not app.testing:
                session["score"] = score
            result_message = f"Correct! +{question_value} points"
        else:
            result_message = "Wrong!"

        return render_template('result.html',
                               score=0 if app.testing else session['score'],
                               question_number=question_number,
                               correct_answer=correct_answer,
                               user_answer=user_answer,
                               result_message=result_message,
                               next_question_number=question_number + 1,
                               value=question_value,
                               num_questions=len(questions))

    if question_number < len(questions):
        return render_template(
            'question.html',
            score=0 if app.testing else session['score'],
            question_number=question_number,
            question_text=question_data['question'],
            options=question_data['options'],
            difficulty=question_data['difficulty'],
            value=question_value)

    return redirect(url_for('end'))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
