import threading
import os
from threading import Timer
from flask import render_template, request, flash, json
from DataBase import *
from utils import load_email_templates, is_email_valid
from emailSender import try_send_phishing, send_result_for_target


# Email templates that need to be loaded at the beginning of the run
phishing_email_templates = load_email_templates("phishing_templates")
response_email_templates = load_email_templates("response_templates")


@app.route('/')
def home_screen():
    return


@app.route('/attackers_targets_info')
def attackers_targets_info():
    attackers = json.dumps(get_all_attackers())
    targets = json.dumps(get_all_targets())
    return { 'attackers': attackers, 'targets': targets }, 200


@app.route('/add_attacker_or_target', methods=['POST'])
def add_attacker_or_target():
    if request.method == 'POST':
        type = request.json['type']
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        # Input check
        if type == 'target' and (not name or not email):
            return { 'status': 400, 'message': 'For target please fill the name and email' }, 400
        elif type == 'attacker' and (not name or not email or not password):
            return { 'status': 400, 'message': 'For attacker please fill all fields' }, 400
        elif not is_email_valid(email, type == 'attacker'):
            return { 'status': 400, 'message': 'Email not valid' }, 400
        else:
            # Try to add attacker/target to the DB, can fail in case of repeating names
            try:
                if type == 'attacker':
                    add_attacker(name, email, password)
                    return {'status': 200, 'message': 'Attacker was successfully added'}, 200
                else:
                    add_target(name, email)
                    return {'status': 200, 'message': 'Target was successfully added'}, 200
            except Exception as e:
                return { 'status': 400, 'message': "Something went wrong - check if the name is not already at the database" }, 400


@app.route('/remove_attacker_or_target', methods=['POST'])
def remove_attacker_or_target():
    if request.method == 'POST':
        name = request.json['name']
        type = request.json['type']
        if type == 'attacker':
            delete_attacker(name)
        else:
            delete_target(name)
        attackers = json.dumps(get_all_attackers())
        targets = json.dumps(get_all_targets())
        return { 'attackers': attackers, 'targets': targets }, 200


@app.route('/new_campaign', methods=['POST'])
def new_campaign():
    if request.method == 'POST':
        # Create the campaign from the input
        temp = request.json['template']
        template = phishing_email_templates[temp]
        target_list = get_all_targets()
        campaign_number = add_new_campaign(target_list)
        phishing_email_sent, attacker = try_send_phishing(get_all_attackers(), target_list, template, campaign_number)

        # check if the phishing campaign failed, and if so remove it from the DB
        if not phishing_email_sent:
            delete_campaign(campaign_number)
            return { 'status': 400, 'message': 'Could not start the campaign - check attacker mails' }, 400
        else:
            # The campaign started, need new thread to monitor campaign life.
            time = request.json['time']
            campaign_time = int(time) * 60
            timer = Timer(campaign_time, end_campaign, args=(campaign_number, attacker, target_list))
            timer.start()
            return { 'status': 200, 'message': temp+' campagin added successfully' }, 200


@app.route('/campaign_data')
def show_campaign_data():
    return { 'campaigns': json.dumps(get_all_campaigns()) }


@app.route('/account_login:<target_name>/<phishing_number>')
def fall_to_phishing(phishing_number, target_name):
    # when the target enter to the link that he got, we will update the DB accordingly
    inc_campaign_failed_number(phishing_number, target_name)
    return render_template("fail_to_phishing.html")


# function for the monitoring thread that close the campaign after time is up
def end_campaign(campaign_number, attacker, target_list):
    with app.app_context():
        stop_campaign(campaign_number)
        send_result_for_target(attacker, target_list, campaign_number, response_email_templates["pass"],  response_email_templates["fail"])


def run_server():
    app.run('127.0.0.1', 5000)


if __name__ == '__main__':

    # When we want to create new DB
    # create_database()
    # add_attacker("TheServiceNow", "TheServiceNow@outlook.com", "The123Service456Now789")
    # add_attacker("ServiceWithYou", "ServiceWithYou@outlook.com", "Service123With456You789")
    # New thread to run the sever
    serverRunner = threading.Thread(target=run_server, args=())
    serverRunner.start()

    # start the front with npm command
    cmd = 'cd client/ && npm start'
    os.system(cmd)

