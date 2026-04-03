from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'results.json'

def load_results():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_results():
    with open(DATA_FILE, 'w') as f:
        json.dump(results, f, indent=2)

results = load_results()

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify(results)
    
    filtered_results = [
        result for result in results 
        if result.get('category', '').lower() == query
    ]
    
    if not filtered_results:
        filtered_results = [
            result for result in results 
            if query in result['title'].lower() or query in result['snippet'].lower()
        ]
    
    return jsonify(filtered_results)

@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    
    if not data or not data.get('category') or not data.get('title') or not data.get('snippet'):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_id = max([r['id'] for r in results], default=0) + 1
    
    new_result = {
        "id": new_id,
        "title": data.get('title', ''),
        "snippet": data.get('snippet', ''),
        "category": data.get('category', ''),
        "image": data.get('image', None)
    }
    
    results.append(new_result)
    save_results()
    return jsonify(new_result), 201

@app.route('/edit/<int:result_id>', methods=['PUT'])
def edit(result_id):
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    for result in results:
        if result['id'] == result_id:
            result['title'] = data.get('title', result['title'])
            result['snippet'] = data.get('snippet', result['snippet'])
            result['category'] = data.get('category', result['category'])
            if data.get('image'):
                result['image'] = data.get('image')
            return jsonify(result)
    
    return jsonify({"error": "Result not found"}), 404

@app.route('/delete/<int:result_id>', methods=['DELETE'])
def delete(result_id):
    global results
    initial_count = len(results)
    results = [r for r in results if r['id'] != result_id]
    
    if len(results) < initial_count:
        save_results()
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Result not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)