# from django.core.mail import send_mail
# from core.settings import EMAIL_HOST_USER
# subject = 'Test Email'
# message = 'This is a test email sent using SMTP in Django.'
# from_email = EMAIL_HOST_USER
# recipient_list = ['aamirchik19@example.com']

# send_mail(subject, message, from_email, recipient_list)


import random

def send_otp_code():
    return random.randint(10000, 99999)

