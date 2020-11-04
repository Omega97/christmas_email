import smtplib
from random import shuffle
from users import user_list, manager_address
from credentials import credentials


class ChristmasEmailSender:

    def __init__(self, cred):
        self.credentials = cred     # manager credentials, dict of user, password
        self.subject = None     # subject of the mail, str
        self.users = None       # dict of name: address
        self.manager = None     # address, sends mail
        self.matches = None     # dict of sender_name: receiver_name

    def set_users(self, users: dict):
        """dict of name: address"""
        self.users = users

    def set_manager(self, manager: str):
        """address of the account that sends mail"""
        self.manager = manager

    def set_subject(self, subject: str):
        """subject of the mail"""
        self.subject = subject

    def compute_matches(self):
        """compute who will end mail to who"""
        names = list(self.users)
        shuffle(names)
        self.matches = {names[i]: names[i - 1] for i in range(len(self.users))}

    def send_mail(self, to, subject, email_text):
        """manager sends mail to user"""
        text = structure(self.manager, to, subject, email_text)
        text = text.encode('utf-8')
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login(**self.credentials)
        server.sendmail(self.manager, to, text)
        server.close()

    def send_mail_to_users(self):
        """send the mail to everybody"""
        for sender in self.matches:
            receiver = self.matches[sender]
            text = f"Quest'anno farai il tuo ragalo di Natale a {receiver}!"
            self.send_mail(self.users[sender], self.subject, text)

    def send_retract_mail(self):
        """in case somethig goes wrong, send this mail to everybody"""
        for name in self.users:
            text = 'Please ignore any previous mail'
            self.send_mail(self.users[name], f'Retracting {self.subject}', text)

    def health_check(self):
        """check whether all required attributes have been filled"""
        if self.users is None:
            raise ValueError('Please set users!')
        for name in self.users:
            if not self.users[name]:
                raise ValueError('please fill all the fields!')

        if self.manager is None:
            raise ValueError('Please set manager!')

        if not credentials['password']:
            raise ValueError('credentials: password field not filled!')

    def execute(self, ):
        """send to everybody a mail containing their receiver"""
        self.health_check()
        self.compute_matches()
        try:
            print('Sending mail...')
            self.send_mail_to_users()
            print('Done!')
        except Exception as e:
            print('Error: ', e)
            self.send_retract_mail()
            raise e


def structure(sent_from, to, subject, body):
    """transform mail parameters to mail text"""
    return f'From: {sent_from} \n' \
        f'To: {to}\n' \
        f'Subject: {subject}\n' \
        f'\n{body}'


if __name__ == '__main__':

    input('\nPress Enter to send mail to everybody...')
    mail_sender = ChristmasEmailSender(credentials)
    mail_sender.set_subject('regalo di Natale 2020')
    mail_sender.set_users(user_list)
    mail_sender.set_manager(manager_address)
    mail_sender.execute()
