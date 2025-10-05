import os
from flask import Flask, request, jsonify
from db import get_conn, init_db

app = Flask(__name__)
init_db()

def row_to_dict(row):
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}

@app.route("/tasks", methods=["GET"])
def list_tasks():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM tasks order by id").fetchall()
    return jsonify([row_to_dict(r) for r in rows])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return jsonify({"error" : "title required"}), 400
    with get_conn() as conn:
        cur=conn.execute("INSERT INTO tasks (title) VALUES (?)",(title,))
        task_id = cur.lastrowid
        row = conn.execute("Select * from tasks where id =?", (task_id,)).fetchone()

    return jsonify(row_to_dict(row)), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def mark_done(task_id):
    with get_conn() as conn:
        conn.execute("UPDATE tasks set done = 1 where id = ?", (task_id,))
        row = conn.execute("select * from tasks where id =?", (task_id,)).fetchone()
        if row is None:
            return jsonify({"error":"not found"}), 404
    return jsonify(row_to_dict(row))

@app.route("/tasks/<int:task_id>", methods = ["DELETE"])
def delete_task(task_id):
    with get_conn() as conn:
        curr = conn.execute("DELETE from tasks where id = ?", (task_id,))
        if curr.rowcount == 0:
            return jsonify({"error":"not found"}), 404
     
    return jsonify({"message":"deleted"}), 200

if __name__ == "__main__":
    app.run(debug = True)
    
