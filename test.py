from flask import Flask, request, jsonify, json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

books = []
@app.route('/books', methods=['GET'])
def listing():
  return jsonify({'books' : books}), 200

@app.route('/books/<title>', methods=['GET'])
def get_one(title):
  if not filter(lambda book: book['title'] == title, books):
    return "There is no {} book in the list".format(title), 404
  else:  
    book = [book for book in books if book['title'] == title]
    return jsonify(book), 200

@app.route('/books', methods=['POST'])
def adding():
  book = request.json
  books.append(book)
  return jsonify({'books' : books}), 201

@app.route('/books/<title>', methods=['PUT'])
def updating(title):
  if filter(lambda book: book['title'] == title, books):
    incoming_json_data = request.get_json()
    for key, value in tuple(incoming_json_data.items()):
      for book in books:
        if book['title'] == title:
          book[str(key)] = incoming_json_data.get(key, None)
    return "The book {} updated".format(title), 200
  else:
    return "The book {} isn't in the list".format(title), 404

@app.route('/books/<title>', methods=['DELETE'])
def deleting(title):
  if not filter(lambda book: book['title'] == title, books):
    return "The book {} isn't in the list".format(title), 404
  else:
    book = [book for book in books if book['title'] == title]
    books.remove(book[0])
    return "The book {} deleted".format(title), 200

if __name__ == '__main__':
  app.run(debug=True)