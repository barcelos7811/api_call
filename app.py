from flask import Flask, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
import psycopg2
import os
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/call'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))

    def __init__(self, description):
        self.description = description


class Kind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dat_user = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)
    name = db.Column(db.String(500))
    email = db.Column(db.String(500))
    login = db.Column(db.String(200))
    id_admin = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    password = db.Column(db.String(200))
    repeat_password = db.Column(db.String(200))

    def __init__(self, name, email, login, id_admin, password, repeat_password):
        self.name = name
        self.email = email
        self.login = login
        self.id_admin = id_admin
        self.password = password
        self.repeat_password = repeat_password


# 04 - LIST ALL USER
@app.route('/list_user', methods=['GET'])
def get_users():
    results = db.session.query(User, Admin).join(Admin).all()
    data = []
    for user, admin in results:
        d = {'id': user.id, 'name': user.name.upper(), 'login': user.login.upper(), 'email': user.email,
             'admin': admin.description.upper()}
        data.append(d)
    return jsonify(data)


# LIST ALL USER
# @app.route('/list_all', methods=['GET'])
# def get_users():
    #     users = []
    # for user in db.session.query(User).all():
    #     del user.__dict__['_sa_instance_state']
    #     users.append(user.__dict__)
    # return jsonify(users)


# 04 - FIND USER ID
@app.route('/find_user_id/<int:id>', methods=['GET', 'POST'])
def find_user_id(id):
    cod = id
    results = db.session.query(User).filter_by(id=cod)
    for user in results:
        d = {'id': user.id, 'name': user.name.upper(), 'login': user.login.upper(), 'email': user.email, 'id_admin': user.id_admin, 'password': user.password, 'repeat_password': user.repeat_password}
    return jsonify(d)


# 04 - FIND USER
@app.route('/find_user/<string:obj>/', methods=['POST'])
def find_user(obj):
    nm = obj
    results = db.session.query(User, Admin).join(Admin).filter(
        User.name.like('%'+nm.upper()+'%'))
    data = []
    for user, admin in results:
        d = {'id': user.id, 'name': user.name.upper(), 'login': user.login.upper(), 'email': user.email,
             'admin': admin.description.upper()}
        data.append(d)
    return jsonify(data)


# 04 - FIND USER TO LOGIN
@app.route('/find_user_login_/<string:usr>/<string:pas>/', methods=['GET'])
def find_user_login(usr, pas):
    # usr = 'ADM'
    # pas = '123'
    results = db.session.query(User).filter(User.login.like(usr), User.password.like(pas)).all()
    # results = db.session.query(User).all()
    # results = db.session.query(User).filter(User.name == "ADM").first()
    data = []
    for user in results:
        d = {'id': user.id, 'name': user.name.upper(), 'login': user.login.upper(), 'email': user.email,
             'id_admin': user.id_admin}
        data.append(d)
    return jsonify(data)


# FIND USER
# @app.route('/find/<id>', methods=['GET'])
# def get_user(id):
    #     user = User.query.get(id)
    # del user.__dict__['_sa_instance_state']
    # return jsonify(user.__dict__)


# 01 - CREATE USER
@app.route('/create_user_', methods=['GET', 'POST'])
def create_user_():
    print('entrei no create user API')
    body = request.get_json()
    obj_user = User(name=body['name'].upper(), login=body['login'].upper(), email=body['email'], id_admin=body['id_admin'],
                    password=body['password'], repeat_password=body['repeat_password'])
    db.session.add(obj_user)
    db.session.commit()
    return "user created"


# CREATE USER
# @app.route('/create_user', methods=['POST'])
# def create_user():
    # body = request.get_json()
    # db.session.add(
    # User(body['name'], body['email'], body['login'], body['id_admin'], body['password'], body['repeat_password']))
    # db.session.commit()
    # return "item created"


# 02 - UPDATE USER
@app.route('/update_user_/<int:id>', methods=['PUT'])
def update_user_(id):
    body = request.get_json()
    print(body)
    db.session.query(User).filter_by(id=id).update(
        dict(name=body['name'].upper(), login=body['login'].upper(), id_admin=body['id_admin'], email=body['email'], password=body['password'],
             repeat_password=body['repeat_password']))
    db.session.commit()
    print('UPDATE FEITO API')
    return "user updated"


# 02 - UPDATE USER
@app.route('/update_user/<id>', methods=['PUT'])
def update_user(id):
    body = request.get_json()
    db.session.query(User).filter_by(id=id).update(
        dict(name=body['name'], login=body['login'], id_admin=body['id_admin'], password=body['password'],
             repeat_password=body['repeat_password']))
    db.session.commit()
    return "user updated"


# 03 - DELETE USER
@app.route('/delete_user_', methods=['DELETE'])
def delete_user_():
    body = request.get_json()
    print(body['id'])
    db.session.query(User).filter_by(id=body['id']).delete()
    db.session.commit()
    return "user deleted"


# DELETE USER
# @app.route('/delete_user/<id>', methods=['DELETE'])
# def delete_user(id):
    # db.session.query(User).filter_by(id=id).delete()
    # db.session.commit()
    # return "user deleted"


class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dat_call = db.Column(DateTime, default=datetime.now, onupdate=datetime.now)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_kind = db.Column(db.Integer, db.ForeignKey('kind.id'), nullable=False)
    id_status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    description = db.Column(db.String(2000))

    def __init__(self, id_user, id_kind, id_status, description):
        self.id_user = id_user
        self.id_kind = id_kind
        self.id_status = id_status
        self.description = description


# LIST ALL CALL
# @app.route('/list_all_call', methods=['GET'])
# def get_calls():
#    calls = []
#    for call in db.session.query(Call).join(User, User.id == Call.id_user).all():
#        del call.__dict__['_sa_instance_state']
#        calls.append(call.__dict__)
#    return jsonify(calls)

# 04 - LIST ALL CALL
@app.route('/list_call', methods=['GET'])
def get_calls():
    results = db.session.query(Call, User, Kind, Status).join(User).join(Kind).join(Status).all()
    data = []
    for call, user, kind, status in results:
        d = {'id': call.id, 'call': call.description, 'user': user.name, 'kind': kind.description,
             'status': status.description}
        data.append(d)
    return jsonify(data)


# 04 - LIST ALL CALL
@app.route('/find_call/<string:obj>/', methods=['POST'])
def find_call(obj):
    # print(obj)
    # print('passou aqui')
    nm = obj
    # print(nome.upper)
    results = db.session.query(Call, User, Kind, Status).join(User).join(Kind).join(Status).filter(
        Call.description.like('%' + nm.upper() + '%'))
    data = []
    for call, user, kind, status in results:
        d = {'id': call.id, 'call': call.description, 'user': user.name, 'kind': kind.description,
             'status': status.description}
        data.append(d)
    return jsonify(data)


# 04 - LIST ALL CALL
@app.route('/find_call_id/<int:id>', methods=['GET', 'POST'])
def find_call_id(id):
    cod = id
    results = db.session.query(Call).filter_by(id=cod)
    for call in results:
        d = {'id': call.id, 'description': call.description, 'id_user': call.id_user, 'id_kind': call.id_kind,
             'id_status': call.id_status}
    return jsonify(d)


# 04 - FIND CALL
@app.route('/find/<id>', methods=['GET'])
def get_call(id):
    call = Call.query.get(id)
    del call.__dict__['_sa_instance_state']
    return jsonify(user.__dict__)


# 01 - CREATE CALL
@app.route('/create_call_', methods=['GET', 'POST'])
def create_call_():
    body = request.get_json()
    obj_call = Call(id_user=body['id_user'], id_kind=body['id_kind'], id_status=body['id_status'],
                    description=body['description'].upper())
    db.session.add(obj_call)
    db.session.commit()
    return "call created"


# 01 - CREATE CALL
@app.route('/create_call', methods=['POST'])
def create_call():
    body = request.get_json()
    db.session.add(Call(body['id_user'], body['id_kind'], body['id_status'], body['description']))
    db.session.commit()
    return "call created"


# 02 - UPDATE CALL
@app.route('/update_call/<int:id>', methods=['GET', 'POST'])
def update_call(id):
    body = request.get_json()
    db.session.query(Call).filter_by(id=id).update(
        dict(id_user=body['id_user'], id_kind=body['id_kind'], id_status=body['id_status'],
             description=body['description']))
    db.session.commit()
    return "call updated"


# 02 - UPDATE CALL
@app.route('/update_call_/<int:id>', methods=['PUT'])
def update_call_(id):
    body = request.get_json()
    print(body)
    db.session.query(Call).filter_by(id=id).update(
        dict(id_kind=body['id_kind'], id_status=body['id_status'], description=body['description'].upper()))
    db.session.commit()
    return "call updated"


# 03 - DELETE CALL
@app.route('/delete_call/<id>', methods=['DELETE'])
def delete_call(id):
    db.session.query(Call).filter_by(id=id).delete()
    db.session.commit()
    return "call deleted"


# 03 - DELETE CALL
@app.route('/delete_call_', methods=['DELETE'])
def delete_call_():
    body = request.get_json()
    db.session.query(Call).filter_by(id=body['id']).delete()
    db.session.commit()
    return "call deleted"