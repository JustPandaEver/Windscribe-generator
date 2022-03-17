import requests
from bs4 import BeautifulSoup
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

class GmailnatorAPI():
    def __init__(self):
        self.setup_email_connection()
        self.email = self.generate_email()
    
    def setup_email_connection(self):
        self.retry_strategy = Retry(
            total=3,
            connect=5,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["GET", "POST"]
        )
        self.adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.email_session = requests.Session()
        self.email_session.headers.update({'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'})
        self.csrf_gmailnator_token = self.get_csrf()
        self.email_session.headers.update({'cookie': f'csrf_gmailnator_cookie={self.csrf_gmailnator_token}'})

    def get_csrf(self):
        request = self.email_session.get("https://www.gmailnator.com")
        return request.cookies['csrf_gmailnator_cookie']

    def generate_email(self):
        data = {
            'csrf_gmailnator_token': self.csrf_gmailnator_token,
            'action': 'GenerateEmail'
        }
        email_request = self.email_session.post('https://www.gmailnator.com/index/indexquery', data=data)
        return email_request.json()['email']

    def get_emails(self):
        data = {
            'csrf_gmailnator_token': self.csrf_gmailnator_token,
            'action': 'LoadMailList',
            'Email_address': self.email
        }
        inbox = self.email_session.post('https://www.gmailnator.com/mailbox/mailboxquery', data=data).json()
        if len(inbox) > 1:
            return inbox

    def retrieve_message(self, email_id):
        r = requests.get(email_id)
        return BeautifulSoup(r.text, features="lxml").find("iframe")['srcdoc']