from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

books = [
#   {
#   'title' : 'LoR',
#   'author' : 'Tolkin',
#   'description' : 'novel',
#   'ISBN' : '8465-4682-4853-1177'
# }
]
@app.route('/books', methods=['GET'])
def listing():
  return jsonify({'books' : books}), 200

@app.route('/books', methods=['POST'])
def entering():
  book = {
    'title': request.json['title'],
    'author': request.json['author'],
    'ISBN' : request.json['ISBN'],
    'description' : request.json['description']
    } 
  books.append(book)
  return jsonify({'books' : books}), 201

@app.route('/books/<title>', methods=['PUT'])
def updating(title):
  for kati in books:
    req = request.get_json()
    books[-1].update(req)
    return "The book {} updated".format(title), 201

@app.route('/books/<title>', methods=['DELETE'])
def deleting(title):
  book = [book for book in books if book['title'] == title]
  books.remove(book[0])
  return "The book {} deleted".format(title), 200

if __name__ == '__main__':
  app.run(debug=True)