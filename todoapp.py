import os
import re
import pickle
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todos = []

# Load the saved list if it exists
if os.path.exists('todos.pkl'):
    with open('todos.pkl', 'rb') as file:
        todos = pickle.load(file)

@app.route('/')
def index():
    error = request.args.get('error', '')
    return render_template('index.html', todos=todos, error=error)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']

    # Validate email
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return redirect(url_for('index', error='Invalid email'))

    # Validate priority
    if priority not in ['Low', 'Medium', 'High']:
        return redirect(url_for('index', error='Invalid priority'))

    new_todo = {
        'task': task,
        'email': email,
        'priority': priority
    }
    todos.append(new_todo)

    return redirect(url_for('index'))

@app.route('/delete/<int:todo_index>', methods=['POST'])
def delete(todo_index):
    if 0 <= todo_index < len(todos):
        del todos[todo_index]
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    todos.clear()
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save():
    with open('todos.pkl', 'wb') as file:
        pickle.dump(todos, file)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
