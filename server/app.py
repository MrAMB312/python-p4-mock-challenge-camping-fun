#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/campers', methods=["GET", "POST"])
def campers():
    if request.method == 'GET':
        
        campers = [camper.to_dict(only=('id', 'name', 'age')) for camper in Camper.query.all()]
        response = make_response(campers, 200)
        return response
    
    elif request.method == 'POST':
        
        data = request.get_json()

        name=data.get('name')
        age=data.get('age')

        if not name or not age or not 8 <= age <= 18:
            return { 'errors': ['validation errors'] }, 400

        new_camper = Camper(
            name=name,
            age=age
        )

        db.session.add(new_camper)
        db.session.commit()

        response = make_response(new_camper.to_dict(only=('id', 'name', 'age')), 201)
        return response

@app.route('/campers/<int:id>', methods=["GET", "PATCH"])
def camper_by_id(id):
    if request.method == 'GET':
        
        camper = Camper.query.filter_by(id=id).first()
        if not camper:
            response = make_response({ 'error': 'Camper not found'}, 404)
            return response
        
        response = make_response(camper.to_dict(), 200)
        return response
    
    elif request.method == 'PATCH':
        
        data = request.get_json()
        camper = Camper.query.filter_by(id=id).first()
        if not camper:
            response = make_response({ 'error': 'Camper not found'}, 404)
            return response
        
        name=data.get('name')
        age=data.get('age')

        if not name or not age or not 8 <= age <= 18:
            return { 'errors': ['validation errors']}, 400

        for attr in data:
            setattr(camper, attr, data[attr])

        db.session.add(camper)
        db.session.commit()

        response = make_response(camper.to_dict(), 202)
        return response

@app.route('/activities', methods=["GET"])
def activities():

        activities = [activity.to_dict(only=('id', 'name', 'difficulty')) for activity in Activity.query.all()]
        response = make_response(activities, 200)
        return response

@app.route('/activities/<int:id>', methods=["DELETE"])
def activity_by_id(id):
    
    activity = Activity.query.filter_by(id=id).first()
    if not activity:
        return { 'error': 'Activity not found'}, 404
    
    db.session.delete(activity)
    db.session.commit()

    response = make_response('', 204)
    return response

@app.route('/signups', methods=["POST"])
def signups():
    
        data = request.get_json()

        time=data.get('time')
        camper_id=data.get('camper_id')
        activity_id=data.get('activity_id')

        if not time or not camper_id or not activity_id or not 0 <= time <= 23:
            return { 'errors': ['validation errors'] }, 400

        new_signup = Signup(
            time=time,
            camper_id=camper_id,
            activity_id=activity_id
        )

        db.session.add(new_signup)
        db.session.commit()

        response = make_response(new_signup.to_dict(), 201)
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
