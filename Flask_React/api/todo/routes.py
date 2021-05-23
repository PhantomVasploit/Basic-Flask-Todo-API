from flask import Blueprint, request, jsonify
from api.model import Todo
from api import db


todo = Blueprint("todo", __name__)


# todo crud
# create
@todo.route("/todo/new_todo", methods=["POST"])
def new_todo():
    name = request.json.get("name", None)
    # date_of_todo = request.json.get("date_of_todo", None)
    todo_data_1 = Todo.query.filter_by(name=name).first()
    if not todo_data_1:
        todo_data = Todo(name=name)
        db.session.add(todo_data)
        db.session.commit()
        return jsonify(todo_data.name, todo_data.date_of_todo)
    elif todo_data_1:
        error = {"Error Message": "Todo already exits"}
        return jsonify(error)


# read
@todo.route("/todo/all", methods=["GET"])
def get_todos():
    todo_data = Todo.query.all()
    for item in todo_data:
        data = {"name":item.name, "date_of_todo": item.date_of_todo}
        return jsonify(data)


# update
@todo.route("/todo/<int:todo_id>/update", methods=["POST"])
def update_todo(todo_id):
    todo_data = Todo.query.get_or_404(todo_id)
    name = request.json.get("name", None)
    todo_data = Todo.query.filter_by(id=todo_id).first()
    todo_data.name = name
    db.session.commit()
    success = {"Success_Message": "Update successful"}
    return jsonify(todo_data.name, todo_data.date_of_todo, success["Success_Message"])


# delete
@todo.route("/todo/delete", methods=["POST"])
def delete_post():
    name = request.json.get("name", None)
    todo_data = Todo.query.filter_by(name=name).first()
    db.session.delete(todo_data)
    db.session.commit()
    success = {"Delete_Success": "Todo deleted successfully!"}
    return jsonify(success["Delete_Success"])
