import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Use environment variable for data file location
DATA_FILE = os.environ.get('DATA_FILE', 'results.json')

def load_results():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_results():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(results, f, indent=2)
    except Exception as e:
        print(f"Error saving results: {e}")

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
    global results
    data = request.get_json()
    
    if not data or not data.get('category') or not data.get('title') or not data.get('snippet'):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_id = max([r['id'] for r in results], default=0) + 1
    
    new_result = {
        "id": new_id,
        "title": data.get('title', ''),
        "snippet": data.get('snippet', ''),
        "category": data.get('category', ''),
        "images": data.get('images', [])
    }
    
    results.append(new_result)
    save_results()
    return jsonify(new_result), 201

@app.route('/edit/<int:result_id>', methods=['PUT'])
def edit(result_id):
    global results
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    for result in results:
        if result['id'] == result_id:
            result['title'] = data.get('title', result['title'])
            result['snippet'] = data.get('snippet', result['snippet'])
            result['category'] = data.get('category', result['category'])
            result['images'] = data.get('images', result.get('images', []))
            save_results()
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
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)