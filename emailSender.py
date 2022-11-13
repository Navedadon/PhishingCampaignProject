import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from DataBase import get_all_targets


def extract_target_info(targets_obj_list):
    names = []
    emails = []
    for target in targets_obj_list:
        names.append(target['name'])
        emails.append(target['email'])
    return names, emails


def send_email(attacker, targets_obj_list, template):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(attacker['email'], attacker['password'])

    names, emails = extract_target_info(targets_obj_list)
    message_temp = Template(template['body'])

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message

        # add in the actual person name to the message template
        message = message_temp.substitute(PERSON_NAME=name.title(), LINK='www.google.com')

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
