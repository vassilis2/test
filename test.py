from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

books = [
#   {
#   'id' : 0,
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
    if not books:
      i = 0
    else:
      i = books[-1]['id'] +1
    book = {
    # 'id' : books[-1]['id'] +1,
    'id' : i,
    'title': request.json['title'],
    'author': request.json['author'],
    'ISBN' : request.json['ISBN'],
    'description' : request.json['description']
    } 
    books.append(book)
    return jsonify({'books' : books}), 201

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete(book_id):
  book = [book for book in books if book['id'] == book_id]
  books.remove(book[0])
  return "The book {} deleted".format(book), 200

if __name__ == '__main__':
  app.run(debug=True)