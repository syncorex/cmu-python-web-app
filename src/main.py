from flask import Flask
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://cluster0.j9gqkfd.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='../X509-cert-8255257794010601158.pem',
                     server_api=ServerApi('1'))
db = client['trivia']
collection = db['questions']
doc_count = collection.count_documents({})
print(doc_count)

@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"
