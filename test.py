from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

books = []
@app.route('/books', methods=['GET'])
def listing():
  return jsonify({'books' : books}), 200

@app.route('/books/<title>', methods=['GET'])
def get_one(title):
  book = [book for book in books if book['title'] == title]
  return jsonify(book), 200

@app.route('/books', methods=['POST'])
def adding():
  book = request.json
  books.append(book)
  return jsonify({'books' : books}), 201

@app.route('/books/<title>', methods=['PUT'])
def updating(title):

  book_to_update = jsonify([book for book in books if book['title'] == title])
  
  incoming_json_data = request.get_json()
  for key in incoming_json_data:
    book[key] = incoming_json_data[key]

  return "The book {} updated".format(title), 201

@app.route('/books/<title>', methods=['DELETE'])
def deleting(title):
  book = [book for book in books if book['title'] == title]
  books.remove(book[0])
  return "The book {} deleted".format(title), 200

if __name__ == '__main__':
  app.run(debug=True)