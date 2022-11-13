# TODO:
# 1. Copy from, last project code with flask the parts you need and organize the send_mail code
# 2. Push the to repository on Git and write the project name
# 3. Add sender file and random the sender every mail/attack
# 4. Switch the files to database
# 5. Improve template - the massage itself, adding pictures and more templates
# 6. Work on link that can gather data
# 7. Find how report on spam can be catch by the software
# 8.
# 9.
# 10.

from flask import render_template, request, flash
from DataBase import *


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
        if request.form['attacker_Target'] == 'target' and (not request.form['name'] or not request.form['email'] or request.form['password']):
            flash('For target please fill the name and email', 'error')
        elif request.form['attacker_Target'] == 'attacker' and (not request.form['name'] or not request.form['email'] or not request.form['password']):
            flash('For attacker please fill all fields', 'error')
        else:
            if request.form['attacker_Target'] == 'attacker':
                add_attacker(request.form['name'], request.form['email'], request.form['password'])
                flash('Attacker was successfully added')
            else:
                add_target(request.form['name'], request.form['email'])
                flash('Target was successfully added')
    return render_template('add_attacker_or_target.html')


if __name__ == '__main__':
    # create_database() -> When we want to create new DB
    app.run('127.0.0.1', 5000)
