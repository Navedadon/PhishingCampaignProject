# TODO:
# 3. Add sender file and random the sender every mail/attack
# 5. Improve template - the massage itself, adding pictures and more templates
# 6. Work on link that can gather data
# 7. Find how report on spam can be catch by the software
from threading import Timer

from flask import render_template, request, flash, json
from DataBase import *
from utils import load_email_templates, is_email_valid
from emailSender import try_send_phishing, send_result_for_target

phishing_email_templates = load_email_templates("phishing_templates")
response_email_templates = load_email_templates("response_templates")

@app.route('/')
def home_screen():
    return render_template("home_screen.html")


@app.route('/attackers_targets_info')
def attackers_targets_info():
    attackers = json.dumps(get_all_attackers())
    targets = json.dumps(get_all_targets())
    return {'attackers': attackers,
            'targets': targets 
    }


@app.route('/add_attacker_or_target', methods=['GET', 'POST'])
def add_attacker_or_target():
    if request.method == 'POST':
        if request.form['attacker_Target'] == 'target' and (
                not request.form['name'] or not request.form['email'] or request.form['password']):
            flash('For target please fill the name and email', 'error')
        elif request.form['attacker_Target'] == 'attacker' and (
                not request.form['name'] or not request.form['email'] or not request.form['password']):
            flash('For attacker please fill all fields', 'error')
        elif not is_email_valid(request.form['email']):
            flash('Email not valid')
        else:
            if request.form['attacker_Target'] == 'attacker':
                add_attacker(request.form['name'], request.form['email'], request.form['password'])
                flash('Attacker was successfully added')
            else:
                add_target(request.form['name'], request.form['email'])
                flash('Target was successfully added')
    return render_template('add_attacker_or_target.html')


@app.route('/new_campaign', methods=['GET', 'POST'])
def new_campaign():
    if request.method == 'POST':
        template = phishing_email_templates[request.form['template']]
        target_list = get_all_targets()
        campaign_number = add_new_campaign(target_list)
        phishing_email_sent, attacker = try_send_phishing(get_all_attackers(), target_list, template, campaign_number)
        if not phishing_email_sent:
            flash('Could not start the campaign - check attacker mails')
            delete_campaign(campaign_number)
        else:
            campaign_time = int(request.form['time']) * 60
            timer = Timer(campaign_time, end_campaign, args=(campaign_number, attacker, target_list))
            timer.start()
    return render_template('new_campaign.html')


@app.route('/campaign_data')
def show_campaign_data():
    return render_template('campaign_data.html',
                           campaigns=PhishingCampaign.query.all()[::-1])


@app.route('/account_login:<target_name>/<phishing_number>')
def fall_to_phishing(phishing_number, target_name):
    inc_campaign_failed_number(phishing_number, target_name)
    return render_template("fail_to_phishing.html")


def end_campaign(campaign_number, attacker, target_list):
    with app.app_context():
        stop_campaign(campaign_number)
        send_result_for_target(attacker, target_list, campaign_number, response_email_templates["pass"],  response_email_templates["fail"])


if __name__ == '__main__':

    # create_database() #When we want to create new DB
    # add_target("nave dadon", "navedadon97@gmail.com")
    # add_attacker("TheServiceNow", "TheServiceNow@outlook.com", "The123Service456Now789")
    # add_attacker("TheCustomerServices", "TheCustomerServices@outlook.com", "The12Customer456Services789")
    # add_attacker("TheMicroServices", "TheMicroServices@outlook.com", "The123Micro456Services789")
    # delete_target("asd")
    # delete_attacker("liad avisror ")
    app.run('127.0.0.1', 5000)
