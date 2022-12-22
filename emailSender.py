import smtplib
from random import shuffle
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from DataBase import get_campaign_targets_tracer
from utils import replace_space_underscore

# Prefix of the phishing link, need to be changed according to the host website
PHISHING_LINK = "http://127.0.0.1:5000/account_login:"


# The function get target object list and return two list: names and emails
def extract_target_info(targets_obj_list):
    names = []
    emails = []
    for target in targets_obj_list:
        names.append(target['name'])
        emails.append(target['email'])
    return names, emails


def try_send_phishing(attackers_obj_list, targets_obj_list, template, campaign_number):
    shuffle(attackers_obj_list)
    for attacker in attackers_obj_list:
        try:
            send_phishing(attacker, targets_obj_list, template, campaign_number)
            return True, attacker
        except Exception as e:  # Mail can be blocked because we use existing mail hosts
            print(f'Problem with attacker: {attacker["email"]}, got exception: {e}')
            continue
    return False, None


def send_phishing(attacker, targets_obj_list, template, campaign_number):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(attacker['email'], attacker['password'])
    names, emails = extract_target_info(targets_obj_list)
    message_temp = Template(template['body'])

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message

        # add the name and link to the template
        phishing_link = PHISHING_LINK + replace_space_underscore(name) + "/" + str(campaign_number)
        message = message_temp.substitute(PERSON_NAME=name.title(), LINK=phishing_link)

        # set up the parameters of the message
        msg['From'] = attacker['email']
        msg['To'] = email
        msg['Subject'] = template['subject']

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)

        del msg

    # Terminate the SMTP session and close the connection
    s.quit()


def send_result_for_target(attacker, targets_obj_list, campaign_number, pass_temp, fail_temp):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(attacker['email'], attacker['password'])
    names, emails = extract_target_info(targets_obj_list)
    targets_tracer = get_campaign_targets_tracer(campaign_number)

    # For each contact, send the email:
    for name, email in zip(names, emails):

        # choose the right template for each target
        temp = None
        if not targets_tracer[replace_space_underscore(name)]:
            temp = pass_temp
        else:
            temp = fail_temp

        # add the name and the campaign number to the template
        message_temp = Template(temp['body'])
        message = message_temp.substitute(NAME=name.title(), NUMBER=campaign_number)
        msg = MIMEMultipart()

        # set up the parameters of the message
        msg['From'] = attacker['email']
        msg['To'] = email
        msg['Subject'] = temp['subject']

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)

        del msg

    s.quit()
