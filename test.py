from flask import Flask, request, jsonify, json
import pdb
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
allowed_keys = ('title', 'author', 'ISBN', 'description')
books = []
@app.route('/books', methods=['GET'])
def listing():
  if books: return jsonify({'books' : books}), 200    
  return "There are no books yet", 200

@app.route('/books/<title>', methods=['GET'])
def get_one(title):
  if books:
    if not list(filter(lambda book: book['title'] == title, books)):
      return "There is no {} book in the list".format(title), 404
    else:  
      book = [book for book in books if book['title'] == title]
      return jsonify(book), 200
  return "There are no books yet", 200

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
  books.append(book)
  return jsonify({'books' : books}), 201

@app.route('/books/<title>', methods=['PUT'])
def updating(title):
  if not list(filter(lambda book: book['title'] == title, books)):
    return "The book {} isn't in the list".format(title), 404
  else:  
    try: # checks if client sends no data
      incoming_json_data = request.get_json()
      if len(incoming_json_data.items()) > 4: 
        return "Too many keys", 400
    except:
      return "Bad Request", 400  
#  checks client's keys for misspelling
  for i, j in incoming_json_data.items():
    if not i in allowed_keys:
      return "misspelled", 400
    for book in books:
     if book['title'] == title:
       for key, value in tuple(incoming_json_data.items()):
         book[str(key)] = incoming_json_data.get(key, None)
    return "The book {} updated".format(title), 200

@app.route('/books/<title>', methods=['DELETE'])
def deleting(title):
  if not list(filter(lambda book: book['title'] == title, books)):
    return "The book {} isn't in the list".format(title), 404
  else:
    book = [book for book in books if book['title'] == title]
    books.remove(book[0])
    return "The book {} deleted".format(title), 200

if __name__ == '__main__':
  app.run(debug=True)