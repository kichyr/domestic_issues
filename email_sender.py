import smtplib

mail_user = 'olawed@mail.ru'
mail_password = 'Cheka1755'

sent_from = mail_user
to = []
subject = 'User domesticIssuesMIPTbot verification'
body = ''

email_text = """\
From: {}
To: {}
Subject: {}
{}
"""


def send_verification_message(mail, code):
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        server.ehlo()
        server.login(mail_user, mail_password)
        print(email_text.format(sent_from, mail, subject, "Send verification this verification code to bot: {}".format(code)))
        server.sendmail(
            sent_from,
            [mail],
            email_text.format(sent_from, mail, subject, "Send this verification code to bot: {}".format(code)))
        server.close()
    
        print('Email sent!')


#test
if __name__ == "__main__":
    send_verification_message("kichyr@mail.ru", "test")