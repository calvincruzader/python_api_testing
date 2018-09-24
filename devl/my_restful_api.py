from flask import Flask
from flask_restful import Api, Resource, reqparse
import sqlite3

my_app = Flask(__name__)
print(__name__)
api = Api(my_app)

class User(Resource):
    def get(self, name):
        conn = sqlite3.connect('my_users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for user in results:
            name_in_db = user[0] # output is tuple for some reason
            if name == name_in_db:
                return user, 200

        return 'User not found', 404

    # create user if not existing yet in db
    def post(self, name):
        conn = sqlite3.connect('my_users.db')
        cursor = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        cursor.execute("SELECT name FROM users")
        results = cursor.fetchall()

        for user in results:
            name_in_db = user[0]
            if name == name_in_db:
                return "User with name {} already exists in db".format(name), 400

        insert_user = "INSERT INTO users (name, age, occupation) VALUES ('{}', {}, '{}')".format(name, args["age"], args["occupation"])
        cursor.execute(insert_user)
        conn.commit()

        return "{} was added.".format(name), 201

    # update
    def put(self, name):
        conn = sqlite3.connect('my_users.db')
        cursor = conn.cursor()
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        cursor.execute("SELECT name FROM users")
        results = cursor.fetchall()

        for user in results:
            name_in_db = user[0]
            if name == name_in_db:
                sql_update = "UPDATE users SET age={}, occupation='{}' WHERE name='{}'".format(args["age"], args["occupation"], name_in_db)
                print(sql_update)
                cursor.execute(sql_update)
                conn.commit()
                return "{} was updated.".format(name), 200

        insert_user = "INSERT INTO users (name, age, occupation) VALUES ('{}', {}, '{}')".format(name, args["age"], args["occupation"])
        cursor.execute(insert_user)
        conn.commit()

        return "{} was added.".format(name), 201

    def delete(self, name):
        conn = sqlite3.connect('my_users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users")
        result = cursor.fetchall()
        for user in result:
            name_in_db = user[0]
            if name == name_in_db:
                sql_delete = "DELETE FROM users WHERE name='{}'".format(name)
                cursor.execute(sql_delete)
                conn.commit()
                return "{} has been deleted.".format(name), 200

        return "User {} not in db".format(name), 404


class AllUsers(Resource):
    def get(self):
        conn = sqlite3.connect('my_users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        return results


api.add_resource(User, "/user/<string:name>")
api.add_resource(AllUsers, "/user/")

my_app.run(debug=True)

