from bson import ObjectId
from flask import Flask, redirect, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='template')
app.config["MONGO_URI"]="mongodb://127.0.0.1:27017/flask"
mongo=PyMongo(app)

@app.route("/")
def home(): 
    return render_template('users.html')

@app.route('/users', methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        age = request.form.get('age')
        location = request.form.get('location')
        if id and name and age and location: 
            mongo.db.Users.insert_one({'id': id ,'name': name, 'age': age, 'location': location})
        # else:
        #     mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {'name': name, 'age': age, 'location': location}})
        #     return redirect('/users')

    users = list(mongo.db.users.find({}))
    if not users:
        return "<h1> NO Users </h1>"
    else:
        return render_template('users.html', users=users)


@app.route('/addUser')
def createuser():
    return render_template('addUser.html')

@app.route('/usersList')
def userList():
    data = list(mongo.db.Users.find({}))
    return render_template('users.html', users=data)

@app.route('/deleteUser/<string:_id>')
def deleteUser(_id):
    mongo.db.Users.delete_one({'_id': ObjectId(_id)})
    return redirect('/users')

@app.route('/editUser/<string:_id>', methods=['GET', 'POST'])
def editUser(_id): 
    user = mongo.db.Users.find_one({'_id': ObjectId(_id)})
    if request.method == 'POST':
        # user['id'] = request.form.get('id')
        user['name'] = request.form.get('name')
        user['location'] = request.form.get('location')
        user['age'] = request.form.get('age')
        mongo.db.Users.update_one({'_id': ObjectId(_id)}, {'$set': user})
        return redirect('/usersList')
    return render_template('editUser.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
