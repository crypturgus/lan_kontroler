import smtplib


class Nofication(object):
    @staticmethod
    def email_sender(rec, usr, pwd):
        ''' function to send email '''
        # to = email_to
        input_message = 'Czas na ssanie'
        if not isinstance(rec, list):
            rec = [rec]

        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(usr, pwd)
        for receiver in rec:
            header = 'To:' + receiver + '\n' + 'From: ' + usr + '\n' + 'Subject:SSANIE! \n'
            input_message = input_message
            msg = header + input_message
            smtpserver.sendmail(usr, receiver, msg)
        smtpserver.close()
        return True
# data = get_config()
# Nofication.email_sender(**data)
