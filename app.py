import random

from flask import Flask, render_template, request, jsonify
import csv
import time
from init import Speller

app = Flask(__name__)
spell = Speller()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    start = time.time()
    query = request.form.get('query', '')

    if not query:
        return jsonify({'error': 'Empty query'})

    p = spell(query).lower().split()

    results = []
    count = 0

    with open("Database_updated.csv", encoding='ANSI') as r_file:
        file_reader = csv.reader(r_file, delimiter=";")
        for row in file_reader:
            t = True
            for j in p:
                if j not in row[1].lower():
                    t = False
            if t:
                results.append({
                    'id': count + 1,
                    'text': row[1],
                    'cal': row[2]
                })
                count += 1

    execution_time = (time.time() - start) * 10 ** 3

    return jsonify({
        'results': results,
        'count': count,
        'time': f"{execution_time:.2f} ms"
    })


if __name__ == '__main__':
    app.run(debug=True)