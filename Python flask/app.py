from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Sample data
tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read a book", "done": True},
    {"id": 3, "title": "Walk the dog", "done": False},
]


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = {
        "id": len(tasks) + 1,
        "title": data.get("title", ""),
        "done": False,
    }
    tasks.append(new_task)
    return jsonify(new_task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def toggle_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = not task["done"]
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
