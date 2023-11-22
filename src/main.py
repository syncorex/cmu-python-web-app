import typing
from flask import Flask
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.server_api import ServerApi

app = Flask(__name__)

cert_path = '/home/user/advpy-web-app/X509-cert-8255257794010601158.pem'

uri = 'mongodb+srv://cluster0.j9gqkfd.mongodb.net/'\
      '?authSource=%24external'\
      '&authMechanism=MONGODB-X509&'\
      'retryWrites=true&w=majority'

client: MongoClient[typing.Any]
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=cert_path,
                     server_api=ServerApi('1'))
db: Database[typing.Any]
db = client['trivia']
collection: Collection[typing.Any]
collection = db['questions']
doc_count = collection.count_documents({})
print(doc_count)


@app.route("/")
def hello_world() -> str:
    return "<p>Hello, World!</p>"
