from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
  global task_id_control
  data = request.get_json()
  new_task = Task(task_id_control, data['title'], data.get("description", ""))
  task_id_control += 1
  tasks.append(new_task)
  return jsonify({"message": "New task created", "id": new_task.id})

@app.route('/tasks', methods=['GET'])
def get_tasks():
  task_list = [task.to_dict() for task in tasks]
  output = {
      "tasks": task_list,
      "total_tasks": len(task_list)
    }
  return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
  for task in tasks:
    if task.id == id:
      return jsonify(task.to_dict())
    
    return jsonify({"message": "It wasn't possible to find the task, check if the ID is right."}), 404
  
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
  task = None  
  for t in tasks:
    if t.id == id:
      task = t
      break

  if task == None:
    return jsonify({"message": "It wasn't possible to find the task, check if the ID is right."}), 404
  
  data = request.get_json()
  task.title = data['title']
  task.description = data['description']
  task.completed = data['completed']

  return jsonify({"message": "Task successfully updated"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
  task = None  
  for t in tasks:
    if t.id == id:
      task = t
      break

  if task == None:
    return jsonify({"message": "It wasn't possible to find the task, check if the ID is right."}), 404
  
  tasks.remove(task)
  return jsonify({"message": "Task successfully deleted"})

if __name__ == "__main__":
  app.run(debug=True)