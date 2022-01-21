from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.idx


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        title = request.form.get('content')
        new_todo = Todo(content=title)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue in your new task'
    else:
        todo_list = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', todo_list=todo_list)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(content=title)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'Cannot delete task'


@app.route('/update/<int:todo_id>', methods=['GET'])
def update_view(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return render_template('update.html', todo=todo)


@app.route('/update/<int:todo_id>', methods=['POST'])
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    title = request.form.get('content')

    todo.content = title
    try:
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(e)
        return 'There was an issue in your updated task'


if __name__ == '__main__':
    db.create_all()
    app.run()
