from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PickleType
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql.expression import func

from utils import replace_space_underscore

app = Flask("PhishingCampaign")
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProjectDataBase.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)


def create_database():
    db.create_all()


class TargetsInfo(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


def add_target(name, email):
    target = TargetsInfo(name, email)
    db.session.add(target)
    db.session.commit()


def get_all_targets():
    all_targets_list = []
    all_targets_obj = TargetsInfo.query.all()
    for target in all_targets_obj:
        all_targets_list.append({'name': target.name, 'email': target.email})
    return all_targets_list


def delete_target(target_name):
    target = TargetsInfo.query.filter_by(name=target_name).all()
    if len(target) == 1:
        target = target[0]
        db.session.delete(target)
        db.session.commit()


class AttackersInfo(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


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
    return all_attacker_list


class PhishingCampaign(db.Model):
    campaign_number = db.Column(db.Integer, primary_key=True)
    passed_number = db.Column(db.Integer)
    failed_number = db.Column(db.Integer)
    targets_tracer = db.Column(MutableDict.as_mutable(PickleType))
    is_alive = db.Column(db.Boolean)

    def __init__(self, campaign_number, targets_tracer):
        self.campaign_number = campaign_number
        self.passed_number = len(targets_tracer)
        self.failed_number = 0
        self.targets_tracer = targets_tracer
        self.is_alive = True


def get_all_campaigns():
    all_campaigns_list = []
    all_campaigns_obj = PhishingCampaign.query.all()[::-1]
    for campaign in all_campaigns_obj:
        all_campaigns_list.append({'campaign_number': campaign.campaign_number, 'passed_number': campaign.passed_number, 'failed_number': campaign.failed_number, 'is_alive': str(campaign.is_alive)})
    return all_campaigns_list


def add_new_campaign(target_list):
    campaign_number = 0
    targets_tracer = {}
    last_campaign_number = db.session.query(func.max(PhishingCampaign.campaign_number)).scalar()
    if last_campaign_number is not None:
        campaign_number = last_campaign_number + 1
    for target in target_list:  # make a target list the trace who already enter the link
        targets_tracer[replace_space_underscore(target['name'])] = False
    campaign = PhishingCampaign(campaign_number, targets_tracer)
    db.session.add(campaign)
    db.session.commit()
    return campaign.campaign_number


def delete_campaign(campaign_number):
    campaign = PhishingCampaign.query.filter_by(campaign_number=campaign_number).first()
    db.session.delete(campaign)
    db.session.commit()


def inc_campaign_failed_number(campaign_number, target_name):
    campaign = PhishingCampaign.query.filter_by(campaign_number=campaign_number).first()

    # we will update only if campaign is alive and target not already enter the link
    if not campaign.targets_tracer[target_name] and campaign.is_alive:
        campaign.passed_number -= 1
        campaign.failed_number += 1
        campaign.targets_tracer[target_name] = True
        db.session.commit()


def stop_campaign(campaign_number):
    campaign = PhishingCampaign.query.filter_by(campaign_number=campaign_number).first()
    if campaign:
        campaign.is_alive = False
        db.session.commit()


def get_campaign_state(campaign_number):
    campaign = PhishingCampaign.query.filter_by(campaign_number=campaign_number).first()
    return campaign.is_alive


def get_campaign_targets_tracer(campaign_number):
    campaign = PhishingCampaign.query.filter_by(campaign_number=campaign_number).first()
    return campaign.targets_tracer

