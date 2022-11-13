from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("PhishingCampaign")
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProjectDataBase.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)


def create_database():
    db.create_all()


def add_target(name, email):
    target = TargetsInfo(name, email)
    db.session.add(target)
    db.session.commit()


def get_all_targets():
    all_targets_list = []
    all_targets_obj = TargetsInfo.query.all()
    for target in all_targets_obj:
        all_targets_list.append({'name': target.name, 'email': target.email})
    print(all_targets_list)
    return all_targets_list


def delete_target(target_name):
    target = TargetsInfo.query.filter_by(name=target_name).all()
    if len(target) == 1:
        target = target[0]
        db.session.delete(target)
        db.session.commit()


class TargetsInfo(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


def add_attacker(name, email, password):
    attacker = AttackersInfo(name, email, password)
    db.session.add(attacker)
    db.session.commit()


def delete_attacker(attacker_name):
    attacker = AttackersInfo.query.filter_by(name=attacker_name).all()
    if len(attacker) == 1:
        target = attacker[0]
        db.session.delete(target)
        db.session.commit()


def get_all_attackers():
    all_attacker_list = []
    all_attacker_obj = AttackersInfo.query.all()
    for attacker in all_attacker_obj:
        all_attacker_list.append({'name': attacker.name, 'email': attacker.email, 'password': attacker.password})
    print(all_attacker_list)
    return all_attacker_list


class AttackersInfo(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

