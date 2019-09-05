import os
import sys

SMTP_URL    = os.getenv('SMTP_URL', 'smtp.gmail.com')
SMTP_PORT   = os.getenv('SMTP_PORT', 587)

SENDER_EMAIL_USER = os.getenv('SENDER_EMAIL_ADDRESS', '<your email account>')
SENDER_EMAIL_PASS = os.getenv('SENDER_EMAIL_PASS', '<your password>')
