from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(50))
    ISBN = db.Column(db.String(50))
    description = db.Column(db.String(50))

    def __init__(self, title, author, ISBN, description):
      self.title = title
      self.author = author
      self.ISBN = ISBN
      self.description = description

class BookSchema(ma.Schema):
  class Meta:
    fields = ('title', 'author', 'ISBN', 'description')

book_schema = BookSchema()
books_schema = BookSchema(many=True)
allowed_keys = ('title', 'author', 'ISBN', 'description')

@app.route('/books', methods=['GET'])
def listing():
  all_books = Book.query.all()
  if all_books:
    result = books_schema.dump(all_books)
    return jsonify(result), 200    
  else: return "There are no books yet", 200
   

@app.route('/books/<id>', methods=['GET'])
def get_one(id):
  book = Book.query.get(id)
  if book: return book_schema.jsonify(book)
  else: return "there's no book with id: {}".format(id)

@app.route('/books', methods=['POST'])
def adding():
  try: # checks if client sends no data
    book = request.get_json()
  except:
    return "Bad Request", 400  
  if len(book.items()) > 4: 
    return "Too many keys", 400
  elif len(book.items()) < 4:
    return "Something's missing", 400
#  checks client's keys for misspelling
  for i, j in book.items():
    if not i in allowed_keys:
      return "misspelled", 400 
  new_book = Book(title=book['title'], author=book['author'], ISBN=book['ISBN'], description=book['description'])
  db.session.add(new_book)
  db.session.commit()
  return 'Done!', 201

@app.route('/books/<id>', methods=['PUT'])
def updating(id):
  try:
    book = Book.query.get(id)
    
    title = request.json['title']  
    author = request.json['author']
    ISBN = request.json['ISBN']
    description = request.json['description']
    
    book.title = title
    book.author = author
    book.ISBN = ISBN
    book.description = description
    db.session.commit() 
    return book_schema.jsonify(book), 200
  except:
    return "Bad Request", 400  
@app.route('/books/<id>', methods=['DELETE'])
def deleting(id):
  try:
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return book_schema.jsonify(book), 200
  except:
    return "Bad Request", 400

if __name__ == '__main__':
  app.run(debug=True)