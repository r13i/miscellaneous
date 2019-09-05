from os.path import basename
import logging

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr

import config

class Reporter(object):
    '''
        Reporter object for sending emails
    '''
    def __init__(self, host, port, user_address, user_password, user_name = None):
        self.HOST   = host
        self.PORT   = port
        self.ADDR   = user_address
        self.PASS   = user_password
        if user_name is not None:
            self.FROM = formataddr((str(Header(user_name.encode(), 'utf-8')), self.ADDR))
        else:
            self.FROM = self.ADDR

        logging.basicConfig(level=logging.INFO, format="[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")

    def send(self, mail_to_list, cc_mail_to_list, bcc_mail_to_list, subject, body, attachement = None):
        # Make sure recipients is an array of unique elements, then format it to be a coma-separated string
        mail_to_list     = list(set(mail_to_list))
        cc_mail_to_list  = list(set(cc_mail_to_list))
        bcc_mail_to_list = list(set(bcc_mail_to_list))

        # Set email sender in the header, recipients, subject, and email body
        msg = MIMEMultipart()
        msg['From'] = self.FROM
        msg['To'] = ','.join(mail_to_list)
        msg['CC'] = ','.join(cc_mail_to_list)
        msg['BCC'] = ','.join(bcc_mail_to_list)
        msg['Subject'] = subject

        formatted_body = """
            <html>
                <head></head>
                <body>
                    {body}
                </body>
            </html>
        """.format(body=body)
        msg.attach(MIMEText(formatted_body, 'html'))

        # Attach file if any
        if attachement is not None:
            with open(attachement, 'r') as f:
                attachement_data = f.read()

            payload = MIMEBase('application', 'octet-stream')
            payload.set_payload(attachement_data)
            encoders.encode_base64(payload)
            payload.add_header('Content-Disposition', 'attachement; filename={}'.format(basename(attachement)))

            msg.attach(payload)
            logging.info('Payload file attached !')

        msg = msg.as_string()
        logging.info('Email successfully formatted !')

        try:
            server = SMTP(host=self.HOST, port=self.PORT)
            logging.info('Successfully connected to SMTP server !')
            server.starttls()
            server.login(user=self.ADDR, password=self.PASS)

            logging.info('Successfully logged in to email user {}'.format(self.ADDR))

            to_addresses = mail_to_list + cc_mail_to_list + bcc_mail_to_list
            server.sendmail(self.ADDR, to_addresses, msg)

            logging.info('Email sent to {}'.format(to_addresses))

            server.quit()

        except Exception as e:
            logging.exception('Error: {}'.format(e))


if __name__ == '__main__':
    r = Reporter(config.SMTP_URL, config.SMTP_PORT, config.SENDER_EMAIL_USER, config.SENDER_EMAIL_PASS, 'Email Sender Name')

    # Send this file as attachement as proof of concept
    import os
    attachement = os.path.abspath(__file__)

    r.send(['<email to>'], ['<email CC>'], ['<email BCC>'], 'Email subject', 'Here comes email body', attachement)