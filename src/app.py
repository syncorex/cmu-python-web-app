from typing import Any
from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.server_api import ServerApi

questions = [
    {
        'question_text': 'What is the capital of France?',
        'options': ['London', 'Berlin', 'Madrid', 'Paris'],
        'correct_answer': 'Paris'
    },
    {
        'question_text': 'Which planet is known as the Red Planet?',
        'options': ['Mars', 'Jupiter', 'Venus', 'Earth'],
        'correct_answer': 'Mars'
    },
    # Add more questions here...
]

app = Flask(__name__)

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
print(doc_count)


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/start')
def start() -> Any:
    return redirect(url_for('question', question_number=0))


@app.route('/question/<int:question_number>', methods=['GET', 'POST'])
def question(question_number: int) -> Any:
    if request.method == 'POST':
        user_answer = request.form['answer']
        correct_answer = questions[question_number]['correct_answer']
        if user_answer == correct_answer:
            result_message = "Correct!"
        else:
            result_message = "Wrong!"

        return render_template('result.html',
                               question_number=question_number,
                               correct_answer=correct_answer,
                               user_answer=user_answer,
                               result_message=result_message,
                               next_question_number=question_number + 1)

    if question_number < len(questions):
        question_data = questions[question_number]
        return render_template('question.html',
                               question_number=question_number,
                               question_text=question_data['question_text'],
                               options=question_data['options'])

    # If there are no more questions, redirect to the result page
    return redirect(url_for('index'))


if __name__ == "__main__":
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
