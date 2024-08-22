from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)

FILE_PATH = 'inventory_data.json'

def load_inventory():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {'items': []}
    return {'items': []}

def save_inventory(inventory):
    with open(FILE_PATH, 'w') as file:
        json.dump(inventory, file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        return jsonify(load_inventory())
    elif request.method == 'POST':
        inventory = load_inventory()
        new_item = request.json
        new_item['id'] = max([item['id'] for item in inventory['items']] + [0]) + 1
        inventory['items'].append(new_item)
        save_inventory(inventory)
        return jsonify({"message": "Item added successfully!", "id": new_item['id']})

@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def item(item_id):
    inventory = load_inventory()
    item_index = next((index for (index, d) in enumerate(inventory['items']) if d["id"] == item_id), None)
    
    if item_index is None:
        return jsonify({"error": "Item not found"}), 404

    if request.method == 'GET':
        return jsonify(inventory['items'][item_index])
    
    elif request.method == 'PUT':
        updated_item = request.json
        inventory['items'][item_index].update(updated_item)
        save_inventory(inventory)
        return jsonify({"message": "Item updated successfully!"})
    
    elif request.method == 'DELETE':
        del inventory['items'][item_index]
        save_inventory(inventory)
        return jsonify({"message": "Item deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
