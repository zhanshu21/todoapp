from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from sqlalchemy.engine.url import URL
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

### todo
# update the completed status in controller

app = Flask(__name__)

# config database
postgres_db = {'drivername': 'postgresql',
               'username': 'udacity',
               'password': 'udacity',
               'host': 'localhost',
               'port': 5432,
               'database': 'mydb'}
# Construct the SQLAlchemy Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = URL.create(**postgres_db)
print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f'<Todo {self.id} {self.description} {self.completed}>'
    
# Ensure the database is initialized
with app.app_context():
    db.create_all()  # Creates tables if they do not exist

@app.route("/")
def index():
    todo_list = Todo.query.order_by('id').all()
    return render_template('index.html', data = todo_list)

@app.route("/todos/create", methods = ['POST'])
def createTodos():
    # fetch the input data
    # new_data = request.form.get('description') # synchrounous method
    error = False
    try:
        new_data = request.get_json()['description']
        new_todo = Todo(description=new_data)
        # add the data to model
        db.session.add(new_todo)
        db.session.commit()
    except: # if try... is failed
        db.session.rollback()
        error = True
    # return newly add the toto.description as json file
    finally:
        if not error:
            return jsonify({
                'id': new_todo.id,
                'description': new_todo.description,
                'completed': new_todo.completed
            })
            db.session.close()
        else:
            abort(400)

@app.route("/todos/<todoId>/update-completed", methods = ['POST'])
def editCompleted(todoId):
    # fetch the input data
    # new_data = request.form.get('description') # synchrounous method
    error = False
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todoId)
        todo.completed = completed
        print(todo)
        db.session.commit()
    except: # if try... is failed
        db.session.rollback()
        error = True
    # return newly add the toto.description as json file
    finally:
        if not error:
            return redirect(url_for('index'))
        else:
            abort(400)

@app.route("/todos/<todoId>/delete", methods = ['POST'])
def delete_todo(todoId):
    # fetch the input data
    # new_data = request.form.get('description') # synchrounous method
    error = False
    try:
        todo = Todo.query.get(todoId)
        db.session.delete(todo)
        db.session.commit()
    except: # if try... is failed
        db.session.rollback()
        error = True
    # return newly add the toto.description as json file
    finally:
        if not error:
            return redirect(url_for('index'))
        else:
            abort(400)

if __name__ == "__main__":
    app.run(debug=True)