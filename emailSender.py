import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from DataBase import AttackersInfo, TargetsInfo


# global variables
SENDER_ADDRESS = "liadavisror@outlook.com"
SENDER_PASSWORD = "Liad123Avisror456"


def get_targets(filename):
    TargetsInfo.query.all()
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_email(target_list, attacker_list):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)

    names, emails = get_contacts(contacts_filename)
    message_temp = read_template(temp_filename)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()  # create a message

        # add in the actual person name to the message template
        message = message_temp.substitute(PERSON_NAME=name.title())

        # set up the parameters of the message
        msg['From'] = SENDER_ADDRESS
        msg['To'] = email
        msg['Subject'] = f'Hi {name.title()} need your help!'

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        s.send_message(msg)

        del msg

    # Terminate the SMTP session and close the connection
    s.quit()