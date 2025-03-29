import random, base64, string, requests, pytesseract, io, os, webbrowser, tempfile, time, imaplib, re
import email
from email.header import decode_header
from datetime import datetime, timedelta
from PIL import Image
from colorama import init, Fore

init(autoreset=True)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
mail = "use ur mail@gmail.com"
password = "uanp ewzy nezv bkyu"


c = requests.session()
os.system('cls' if os.name == 'nt' else 'clear')

def generate_username():
    username_length = random.randint(4, 7)
    return 'PandaEver' + ''.join(random.choices(string.ascii_letters + string.digits, k=username_length))

def generate_num():
    return str(random.randint(1111, 999999))

def login_mail(email_address, password):
    emails = []
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_address, password) # Corrected login
        mail.select('inbox')
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        since_date = one_minute_ago.strftime('%d-%b-%Y')
        status, messages = mail.search(
            None, f'(SINCE "{since_date}" FROM "noreply@windscribe.com")'
        )
        if status == "OK":
            for num in messages[0].split():
                status, data = mail.fetch(num, '(RFC822)')
                if status == "OK":
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            email_dict = {
                                "subject": "",
                                "from": "",
                                "to": "",
                                "body": "",
                            }

                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(
                                    encoding if encoding else "utf-8"
                                )
                            email_dict["subject"] = subject

                            from_, encoding = decode_header(msg.get("From"))[0]
                            if isinstance(from_, bytes):
                                from_ = from_.decode(encoding if encoding else "utf-8")
                            email_dict["from"] = from_

                            to_, encoding = decode_header(msg.get("To"))[0]
                            if isinstance(to_, bytes):
                                to_ = to_.decode(encoding if encoding else "utf-8")
                            email_dict["to"] = to_

                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True)
                                        if body:
                                            email_dict["body"] = body.decode()
                                        break
                            else:
                                body = msg.get_payload(decode=True)
                                if body:
                                    email_dict["body"] = body.decode()
                            emails.append(email_dict)
        url_pattern = r'https://windscribe\.com/signup/confirmemail/[a-zA-Z0-9]+/[a-zA-Z0-9]+(?:\?ts=\d+)?'
        match = re.search(url_pattern, emails[len(emails)-1]['body'])
        if match:
            extracted_url = match.group(0)
            c.get(extracted_url)
            print("Success Confirm Mail")
        else:
            print("URL not found.")
        return
    except imaplib.IMAP4.error as e: # Catch imap errors specifically.
        print(f"IMAP Error retrieving emails: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    

def to_text(base64_string):
    try:
        base64_data = base64_string.split(',')[1]
        img_bytes = base64.b64decode(base64_data)
        img = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        print(f"Error processing base64 image: {e}")
        return None

def display(base64_string):
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as f:
            html_content = f"""
            <html>
            <body>
                <img src="{base64_string}">
            </body>
            </html>
            """
            f.write(html_content)
            temp_filename = f.name
        webbrowser.open('file://' + os.path.realpath(temp_filename))
    except Exception as e:
        print(f"Error opening base64 image in browser: {e}")

def regist():
    username = generate_username()
    mails = f"{mail.lower().replace("@gmail.com","")}+{generate_num()}@gmail.com"
    print(f"{Fore.GREEN}Username: {Fore.CYAN}{username}")
    print(f"{Fore.GREEN}Password: {Fore.CYAN}PandaEverX1337")
    print(f"{Fore.GREEN}Email: {Fore.CYAN}{mails}")
    signup_url = "https://windscribe.com/signup"
    payload = {
        "signup": "1",
        "username": username,
        "password": "PandaEverX1337",
        "password2": "PandaEverX1337",
        "email": f"{mails}",
        "voucher_code": "",
        "captcha": "",
        "robert_status": "0",
        "unlimited_plan": "0"
    }    
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.5",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "_pk_id.3.2e1e=996db2ffaea89280.1732726027.2.1732748765.1732748203.; cpid=app_windows; i_can_has_cookie=1; pcpid=website_post_signup; ref=https%3A%2F%2Fwindscribe.com%2Fsignup%3Fcpid%3Dapp_windows; _pk_id.5.2e1e=167a6e953e021a09.1732726384.1.1732726384.1732726384.; PHPSESSID=daf26423df48fcae85a6cd39fed904aa; _pk_ses.3.2e1e=*",
        "DNT": "1",
        "Host": "windscribe.com",
        "Origin": "https://windscribe.com",
        "Priority": "u=0",
        "Referer": "https://windscribe.com/signup",
        "sec-ch-ua": '"Google Chrome";v="112", "Chromium";v="112", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1", 
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-A037U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36 uacq"
    }
    try:
        response = c.post(signup_url, data=payload, headers=headers)
        response_data = response.json()
        if response_data.get("errorCode") == 707:
            print(response_data["errorMessage"]+"\nSleep 30 seconds")
            time.sleep(30)
            return
        if response_data.get("errorCode") == 909:
            captcha_url = f"https://windscribe.com{response_data['captcha']}"
            captcha_response = c.get(captcha_url, headers=headers)
            if captcha_response.status_code == 200:
                base64_i = base64.b64encode(captcha_response.content)
                base64_image = f'data:image/png;base64,{base64_i.decode('utf-8')}'
                payload["captcha"] = to_text(base64_image)
                if payload["captcha"] == "":
                    display(base64_image)
                    payload["captcha"] = input("Failed Solve, captcha code? ")
                final_response = c.post(signup_url, data=payload, headers=headers).json()
                if final_response.get("errorCode") == 909:
                    display(base64_image)
                    payload["captcha"] = input("Failed Solve, captcha code? ")
                final_response = c.post(signup_url, data=payload, headers=headers).json()
                if final_response.get("errorCode") == 707:
                    print(final_response["errorMessage"]+"\nSleep 30 seconds")
                    time.sleep(30)
                    return
                registered = final_response["data"]['username']
                if(username == registered):
                    with open("windscribe.txt","a+") as f:
                        f.write(f"{registered}|PandaEverX1337\n")
                    print(f"Registration successful, Please Wait.")
                    time.sleep(10)
                    login_mail(mail, password)
            else:
                print("Failed to fetch the captcha image.")
        else:
            print(response.text)
    except c.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
n = 0
i = input("how many account? ")
while n < int(i):
    regist()
    n += 1
