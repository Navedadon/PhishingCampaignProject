import os
import re


# Build array of email templates
def load_email_templates():
    email_templates = {}
    # loop over each email template
    for f in os.listdir("phishing_templates"):
        template_file = os.path.join("phishing_templates/", f)

        if os.path.isfile(template_file):
            # read in the template SUBJECT, TYPE, and BODY
            temp_type = ""
            temp_subject = ""
            temp_body = ""
            with open(template_file, "r") as myfile:
                for line in myfile.readlines():
                    match = re.search("TYPE=", line)
                    if match:
                        temp_type = line.replace('"', "")
                        temp_type = temp_type.split("=")
                        temp_type = temp_type[1].lower().strip()
                    match2 = re.search("SUBJECT=", line)
                    if match2:
                        temp_subject = line.replace('"', "")
                        temp_subject = temp_subject.split("=")
                        temp_subject = temp_subject[1].strip()
                    match3 = re.search("BODY=", line)
                    if match3:
                        temp_body = line.replace('"', "")
                        temp_body = temp_body.replace(r'\n', "\n")
                        temp_body = temp_body.split("=")
                        temp_body = temp_body[1].strip()
            email_templates[temp_type] = {'type': temp_type, 'subject': temp_subject, 'body': temp_body}
    return email_templates
