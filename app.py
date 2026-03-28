from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Sample data storage (in real app, use a database)
results = [
    {
        "id": 1,
        "title": "Sample Result 1",
        "snippet": "This is a sample snippet for result 1",
        "journey": "Journey 1",
        "modules": "Module A, Module B",
        "category": "1.1"
    },
    {
        "id": 2,
        "title": "Sample Result 2",
        "snippet": "This is a sample snippet for result 2",
        "journey": "Journey 2",
        "modules": "Module C, Module D",
        "category": "1.2"
    }
]

# Search endpoint
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify(results)
    
    # Search by category first (exact match)
    filtered_results = [
        result for result in results 
        if result.get('category', '').lower() == query
    ]
    
    # If no category match, search by title and snippet
    if not filtered_results:
        filtered_results = [
            result for result in results 
            if query in result['title'].lower() or query in result['snippet'].lower()
        ]
    
    return jsonify(filtered_results)

# Add endpoint
@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    
    # Validate required fields
    if not data or not data.get('category') or not data.get('title') or not data.get('snippet'):
        return jsonify({"error": "Missing required fields"}), 400
    
    new_id = max([r['id'] for r in results], default=0) + 1
    
    new_result = {
        "id": new_id,
        "title": data.get('title', ''),
        "snippet": data.get('snippet', ''),
        "category": data.get('category', '')
    }
    
    results.append(new_result)
    return jsonify(new_result), 201

# Edit endpoint
@app.route('/edit/<int:result_id>', methods=['PUT'])
def edit(result_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    for result in results:
        if result['id'] == result_id:
            result['title'] = data.get('title', result['title'])
            result['snippet'] = data.get('snippet', result['snippet'])
            result['journey'] = data.get('journey', result['journey'])
            result['modules'] = data.get('modules', result['modules'])
            result['category'] = data.get('category', result['category'])  # Update category
            return jsonify(result)
    
    return jsonify({"error": "Result not found"}), 404

# Delete endpoint
@app.route('/delete/<int:result_id>', methods=['DELETE'])
def delete(result_id):
    global results
    initial_count = len(results)
    results = [r for r in results if r['id'] != result_id]
    
    if len(results) < initial_count:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Result not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)