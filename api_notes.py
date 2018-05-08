# -*- coding:utf-8 -*-
import json
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:\\Users\\User\\PycharmProjects\\API cases\\my_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_tag = db.Column(db.String(50))
    locations = db.Column(db.String(80))


    def __init__(self, user_tag , locations, id=None):
        self.id = id
        self.user_tag = user_tag
        self.locations = locations


    def __repr__(self):
        return '<User %r>' % self.user_tag


class UserApi(Resource):
    def get(self, telegram_id):
        user = User.query.filter_by(telegram_id=telegram_id).first()
        respons = {'id': user.id,
                   'user_tag': user.user_tag,
                   'telegram_id': user.telegram_id,
                   'locations': user.locations}
        return json.dumps(respons)

    def post(self):
        user_tag = request.form['user_tag']
        telegram_id = request.form['telegram_id']
        locations = request.form['locations']
        user = User(user_tag=user_tag, locations=locations,telegram_id=telegram_id)
        db.session.add(user)
        db.session.commit()
        return json.dumps({'status': 'ok'})

    def put(self):
        user_id = 1
        user = User.query.filter_by(id = user_id).first()
        user_tag = request.form['user_tag']
        telegram_id = request.form['telegram_id']
        locations = request.form['locations']
        id = request.form['id']
        user.user_tag = user_tag
        db.session.add(user)
        db.session.commit()

class ManagerDBApi(Resource):

        def post(self):
             db.create_all()
             return {'status': 'ok'}

api.add_resource(UserApi, '/person')
api.add_resource(ManagerDBApi, '/create_db')

# @app.route('/create_db')
# def create_db():
#     db.create_all()
#     return 'ok.DB has been created.'
#
# @app.route('/add/person/<name>')
# def add_person(name):
#     person = Person(name = name)
#     db.session.add(person)
#     db.session.commit()
#
#     return 'ok.DB has been created a person.'
#
#
# @app.route('/add/address/<address_owner_email>/<person>')
# def add_address(address_owner_email,person):
#     owner = Person.query.filter_by(name = person).first()
#     person = Address(email = address_owner_email , person_id = owner.id)
#     db.session.add(person)
#     db.session.commit()
#
#     return 'ok.DB has been created a person.'
#
#
if __name__ == '__main__':
    app.run(debug=True, port=2228)
