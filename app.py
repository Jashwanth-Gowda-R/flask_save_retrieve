from flask import Flask, request
from flask_pymongo import PyMongo
import flask


app = Flask(__name__)

app.secret_key = "jashu"

app.config["MONGO_URI"] = "mongodb://localhost:27017/filesave"

mongo = PyMongo(app)


@app.route('/')
def index():
    return '''
        <form method="POST" action="/create" enctype="multipart/form-data">
            <input type="text" name="username">
            <input type="file" name="profile_image">
            <input type="submit" >
    '''


@app.route('/create', methods=['POST'])
def save():
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename, profile_image)
        mongo.db.filesave.insert(
            {'username': request.form.get('username'), 'profile_image_name': profile_image.filename})

    return 'done!'


@app.route('/file/<filename>')
def retrieve(filename):
    return mongo.send_file(filename)


@app.route('/profile/<username>')
def profile(username):
    user = mongo.db.filesave.find_one_or_404({'username': username})
    return f"""
        <h1>{username}</h1>
        <img src="{flask.url_for('retrieve',filename=user['profile_image_name'])}">
    """

if __name__ == " __main__":
    app.run(debug=True)
