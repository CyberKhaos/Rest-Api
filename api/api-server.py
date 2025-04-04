import uuid, json

from pydantic import ValidationError
from api.models.TodoList import TodoList, TodoEnty
from flask import Flask, request, jsonify

# initialize Flask server
app = Flask(__name__)

shopping_list_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'

todo_list = [TodoList(**{
    'id' : shopping_list_id,
    'name' : 'Einkaufsliste'
})]

todo_entries = [TodoEnty(**{
    'id' : '3062dc25-6b80-4315-bb1d-a7c86b014c65',
    'name' : 'Milch',
    'description' : '3,5% Fett Vollmilch',
    'list_id' : shopping_list_id
})]


# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoints for getting deleting creating and updating todo lists
@app.route('/todo-list', methods=['POST'])
def create_new_list():
    try:
        data = request.get_json(force=True)
        new_list = TodoList(**data)
        new_list['id'] = uuid.uuid4()
        todo_list.append(new_list)
        return jsonify(new_list.dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400

# Endpoint zum Abrufen aller Todo-Listen
@app.route('/todo-lists', methods=['GET'])
def get_all_todo_lists():
    try:
        return jsonify([i.dict() for i in todo_list]), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400

# Endpoint zum Abrufen oder Löschen einer bestimmten Todo-Liste
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handel_list(list_id):
    list_item = TodoList
    for item in todo_list:
        if item.id == list_id:
            list_item = item
            break
    if not list_item:
        return jsonify({"error": "Wrong Id"}), 404
    if request.method == 'GET':
        return jsonify([i for i in todo_list if i.id == list_id]), 200
    if request.method == 'DELETE':
        todo_list.remove(list_item)
        return '', 200

# Endpoint zum Erstellen eines neuen Eintrags in einer bestimmten Todo-Liste
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def create_new_entry(list_id):
    try:
        data = request.get_json(force=True)
        new_list_entry = TodoEnty(**data)
        new_list_entry['id'] = uuid.uuid4()
        todo_entries.append(new_list_entry)
        return jsonify(new_list_entry.dict()), 200
    except ValidationError as e:
        return jsonify(e.errors()), 400

# Endpoint zum Aktualisieren oder Löschen eines bestimmten Eintrags in einer Todo-Liste
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def handel_list_entries(list_id, entry_id):
    try:
        entry_item = TodoEnty
        for item in todo_entries:
            if item.id == entry_id:
                entry_item = item
                break
        if not entry_item:
            return jsonify({"error": "Wrong Id"}), 404
        if request.method == 'PUT':
            data = request.get_json(force=True)
            updated_entry = TodoEnty(**data)
            updated_entry['id'] = entry_id
            todo_entries.append(updated_entry)
            return jsonify(updated_entry.dict()), 200
        if request.method == 'DELETE':
            todo_entries.remove(entry_item)
            return '', 200
    except ValidationError as e:
        return jsonify(e.errors()), 400


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)