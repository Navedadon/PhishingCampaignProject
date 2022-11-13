# TODO:
# 3. Add sender file and random the sender every mail/attack
# 5. Improve template - the massage itself, adding pictures and more templates
# 6. Work on link that can gather data
# 7. Find how report on spam can be catch by the software


from flask import render_template, request, flash
from DataBase import *
from utils import load_email_templates
from emailSender import send_email

email_templates = load_email_templates()

@app.route('/')
def home_screen():
    return render_template("home_screen.html")


@app.route('/attackers_targets_info')
def attackers_targets_info():
    return render_template('attackers_targets_info.html',
                           attackers=AttackersInfo.query.all(),
                           targets=TargetsInfo.query.all())


@app.route('/add_attacker_or_target', methods=['GET', 'POST'])
def add_attacker_or_target():
    if request.method == 'POST':
        if request.form['attacker_Target'] == 'target' and (
                not request.form['name'] or not request.form['email'] or request.form['password']):
            flash('For target please fill the name and email', 'error')
        elif request.form['attacker_Target'] == 'attacker' and (
                not request.form['name'] or not request.form['email'] or not request.form['password']):
            flash('For attacker please fill all fields', 'error')
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
        template = email_templates[request.form['template']]
        send_email(get_all_attackers()[0], get_all_targets(), template)
    return render_template('new_campaign.html')


if __name__ == '__main__':
    #  create_database() #When we want to create new DB
    app.run('127.0.0.1', 5000)
