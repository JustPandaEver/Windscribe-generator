import random, base64, string, requests, pytesseract, io, os, webbrowser, tempfile
from PIL import Image
from colorama import init, Fore

init(autoreset=True)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
c = requests.session()
os.system('cls' if os.name == 'nt' else 'clear')

def generate_username():
    username_length = random.randint(4, 7)
    return 'PandaEver' + ''.join(random.choices(string.ascii_letters + string.digits, k=username_length))

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
    print(f"{Fore.GREEN}Username: {Fore.CYAN}{username}")
    print(f"{Fore.GREEN}Password: {Fore.CYAN}PandaEverX1337")
    signup_url = "https://windscribe.com/signup"
    payload = {
        "signup": "1",
        "username": username,
        "password": "PandaEverX1337",
        "password2": "PandaEverX1337",
        "email": "",
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
                final_response = c.post(signup_url, data=payload, headers=headers)
                if("captcha" in final_response.text):
                    display(base64_image)
                    payload["captcha"] = input("Failed Solve, captcha code? ")
                final_response = c.post(signup_url, data=payload, headers=headers)
                registered = final_response.json()["data"]['username']
                if(username == registered):
                    with open("windscribe.txt","a+") as f:
                        f.write(f"{registered}|PandaEverX1337\n")
                    print(f"Registration successful.")
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
