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
i = 0
@app.route('/books', methods=['GET', 'POST'])
def kati():
  if request.method == 'POST':
    if books:
      global i
      i = i + 1
    book = {
    # 'id' : books[-1]['id'] +1,
    'id' : i,
    'title': request.json['title'],
    'author': request.json['author'],
    'ISBN' : request.json['ISBN'],
    'description' : request.json['description']
    } 
    books.append(book)
  return jsonify({'books' : books})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete(book_id):
  book = [book for book in books if book['id'] == book_id]
  books.remove(book[0])
  return "deleted"

if __name__ == '__main__':
  app.run(debug=True)