import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import replace_space_underscore
PHISHING_LINK = "http://127.0.0.1:5000/account_login:"


def extract_target_info(targets_obj_list):
    names = []
    emails = []
    for target in targets_obj_list:
        names.append(target['name'])
        emails.append(target['email'])
    return names, emails


def try_send_phishing(attackers_obj_list, targets_obj_list, template, campaign_number):
    for attacker in attackers_obj_list:
        try:
            send_phishing(attacker, targets_obj_list, template, campaign_number)
            return True
        except Exception as e:
            print(f'Problem with attacker: {attacker["email"]}, got exception: {e}')
            continue
    return False


def send_phishing(attacker, targets_obj_list, template, campaign_number):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(attacker['email'], attacker['password'])
    names, emails = extract_target_info(targets_obj_list)
    message_temp = Template(template['body'])

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message

        # add in the actual person name to the message template
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
