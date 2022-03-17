import time
import requests
from hashlib import md5
from re import sub, findall
from bs4 import BeautifulSoup
from simple_colors import green, red
from .GmailnatorAPI import GmailnatorAPI
from requests.adapters import HTTPAdapter


class WindscribeCreator(GmailnatorAPI):
    def __init__(self, filename, semaphore):
        super().__init__()
        self.semaphore = semaphore
        self.setup_connection()
        self.generate_creds()
        self.result_file = open(filename, 'a+', buffering=1)

    def setup_connection(self):
        adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.generate_client_auth()
        self.session = requests.Session()
        self.session.mount("https://", adapter)

    def generate_client_auth(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '86',
            'Host': 'api.staticnetcontent.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'okhttp/4.9.3',
        }
        self.epoch = str(time.time()).replace(".", "")[:13]
        self.client_auth = md5(f"952b4412f002315aa50751032fcaab03{self.epoch}".encode()).hexdigest()
        data = f'client_auth_hash={self.client_auth}&time={self.epoch}&session_type_id=4'
        requests.post('https://api.staticnetcontent.com/RecordInstall/mobile/android', headers=headers, data=data)

    def generate_creds(self):
        self.username = requests.post("https://windscribe.com/signup", data={'generate_username': '1'}).json()['data']['username']
        self.password = requests.post("https://windscribe.com/signup", data={'generate_password': '1'}).json()['data']['password']

    def extract_confirmation_link(self):
        while True:
            try:
                email = self.get_emails()[-1]
                message = sub('[\n\t]', '', email['content'])
                email_sent_from = findall('<td>(.*)</td><td>', message)[0]
                if "windscribe" in email_sent_from.lower():
                    email_id = BeautifulSoup(message, features="lxml").find("a")['href']
                    return self.confirm_email(email_id)
            except:
                pass
            time.sleep(1)

    def confirm_email(self, email_id):
        try:
            email_content = self.retrieve_message(email_id)
            confirmation_link = BeautifulSoup(email_content, features="lxml").findAll("a")[0]['href']
            confirmation_request = self.session.get(confirmation_link)
            if confirmation_request.status_code == 200:
                return True
        except Exception as e:
            print(e)

    def confirm_account(self):
        if self.extract_confirmation_link():
            self.semaphore.acquire()
            print(f'{green("[*]Account Confirmed!", "bold")}\n{green("Username: ", "bold")}{self.username}\n{green("Email: ", "bold")}{self.email}\n{green("Password: ", "bold")}{self.password}\n-----------------------')
            self.semaphore.release()
            self.result_file.write(f"Username: {self.username}\nEmail: {self.email}\nPassword: {self.password}\n-----------------------\n")
        else:
            self.semaphore.acquire()
            print(red("[ERROR] Can't confirm the account", 'bold'), "\n-----------------------")
            self.semaphore.release()

    def register_account(self, proxy):
        data = {
            'platform': 'android',
            'email': self.email,
            'password': self.password,
            'client_auth_hash': self.client_auth,
            'time': self.epoch,
            'username': self.username,
            'session_type_id': '4'
        }
        registration_request = self.session.post('https://api.staticnetcontent.com/Users', data=data, proxies=proxy)
        if 'errorCode' in registration_request.json().keys():
            self.semaphore.acquire()
            print(red(f"[ERROR] {registration_request.json()['errorMessage']}", 'bold'), "\n-----------------------")
            self.semaphore.release()
            return
        self.confirm_account()
