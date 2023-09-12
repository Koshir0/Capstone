
import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from models import setup_db
from functools import wraps
from auth import *

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  db.app = app
  setup_db(app)
  db.init_app(app)
  # db.create_all()
  CORS(app)
  return app

app = create_app()




# Sample user roles
ROLES = {
    'casting_assistant': ['view_actors', 'view_movies'],
    'casting_director': ['view_actors', 'view_movies', 'add_actor', 'delete_actor', 'modify_actor_movie'],
    'executive_producer': ['view_actors', 'view_movies', 'add_actor', 'delete_actor', 'modify_actor_movie', 'add_movie', 'delete_movie']
}

# In-memory storage for movies and actors
movies = []
actors = []

# Mock user role
current_user_role = 'casting_director'  # Change this to test different roles

def requires_role(*allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user_role not in allowed_roles:
                return jsonify({"message": "Unauthorized"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/')
def index():
    movies = Movie.query.all()
    actors = Actor.query.all()
    return render_template('index.html', movies=movies, actors=actors) 

@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    actor_list = [{"name": actor.name, "age": actor.age, "gender": actor.gender} for actor in actors]
    return jsonify({"actors": actor_list})

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_list = [{"title": movie.title, "release_date": movie.release_date} for movie in movies]
    return jsonify({"movies": movie_list})

@app.route('/actors', methods=['POST'])
@requires_auth(permission='post:actors')
def add_actor(payload):
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    actor = Actor(name=name, age=age, gender=gender)
    if not name or not age or not gender:
        return jsonify({'error': 'Name, age and gender are required'}), 400
    else:
        actor.insert()
    return redirect(url_for('index'))

@app.route('/movies', methods=['POST'])
@requires_auth(permission='post:movies')
def add_movie(payload):
    title = request.form.get('title')
    release_date = request.form.get('release_date')
    new_movie = Movie(title=title, release_date=release_date)
    if not title or not release_date:
        return jsonify({'error': 'Title and release_date are required'}), 400
    else:
        new_movie.insert()
    return redirect(url_for('index'))

@app.route('/actors/<int:actor_id>', methods=['POST','PATCH'])
def update_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if not actor:
        return jsonify({'error': 'Actor not found'}), 404
    
    data = request.form
    name = data.get('name')
    age = data.get('age')
    actor.update(name, age)
    # if name:
    #     actor.update(name) 
    # if age:
    #     actor.update(age)
    
    return redirect(url_for('index'))

@app.route('/movies/<int:movie_id>', methods=['POST','PATCH'])
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    
    data = request.form
    title = data.get('title')
    release_date = data.get('release_date')
    movie.update(title, release_date )
    # if title:
    #     movie.update(title )
    # if release_date:
    #     movie.update(release_date )
    return redirect(url_for('get_movies'))

@app.route('/actors/<int:actor_id>', methods=['POST','DELETE'])
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor:
        actor.delete()
    return redirect(url_for('index'))
    # del actors[actor_id]
    # return jsonify({"message": "Actor deleted successfully"})

@app.route('/movies/<int:movie_id>', methods=['POST','DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)  
    if movie:
        movie.delete()
    else:
        return jsonify({'error': 'Movie not found'}), 404
    return redirect(url_for('index'))



# Handle 404 Not Found
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

# Handle 500 Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal Server Error'}), 500

# Custom 403 Forbidden error handler
@app.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

# Custom 401 Unauthorized error handler
@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('401.html'), 401



if __name__ == '__main__':
    # app.run(debug=True)
    app.debug = True
    app.run()


