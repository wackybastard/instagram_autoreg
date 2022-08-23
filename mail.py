import requests
from time import sleep


class MailAccount():

    url = 'http://api.kopeechka.store/'
    site = 'instagram.com'
    regular_expression = r'\d\d\d\d\d\d'

    def __init__(self, token, mail_type):

        parameters = {
            'site': self.site,
            'mail_type': mail_type,
            'regex': self.regular_expression,
            'token': token,
            'api': '2.0'
        }

        response = requests.get(f'{self.url}/mailbox-get-email', params=parameters)
        self.task_id = response.json()['id']
        self.address = response.json()['mail']

        print(f'{self.address} created')

    def get_code(self):

        parameters = {
            'id': self.task_id,
            'token': self.token,
            'api': '2.0'
        }

        while True:
            response = requests.get(f'{self.url}/mailbox-get-message', params=parameters)
            if response.json()['status'] == 'OK':
                code = response.json()['value']
                return code
            else:
                sleep(3)
