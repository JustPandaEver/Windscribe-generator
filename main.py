import os
import time
import random
import pyfiglet
from colorama import init
from simple_colors import blue
from threading import Semaphore
from utils.WindscribeUtils import WindscribeCreator
from concurrent.futures import ThreadPoolExecutor

os.system("cls && title Windscribe account generator - Kaliendo")
if not os.path.exists('results'):
    os.makedirs('results')
init()
n_threads = 0
n_accs = 0
proxy = ""
proxylist = None
semaphore = Semaphore(1)
output_file = f"output-{time.strftime('%d-%m-%y--%H-%M')}.txt"

print(blue(pyfiglet.figlet_format("WindScribe Gen", font = "slant" ) + "\t\t\tgithub.com/kaliendo\n", 'bold'))

while n_accs <= 0:
    n_accs = int(input("How many accounts do you want to generate? "))
while n_threads <= 0:
    n_threads = int(input("How many threads do you want to run? "))
while proxy.upper() not in ["Y", "N"]: 
    proxy = str(input("Do you want to use proxy? (Y/N) "))
print("\n-----------------------")

if proxy.upper() == "Y":
    proxylist = [{'http':f'http://{i.strip()}', 'https':f'http://{i.strip()}'} for i in open("proxy.txt").readlines()]

processes = []
with ThreadPoolExecutor(max_workers=n_threads) as executor:
    for _ in range(n_accs):
        proxy = {}
        if proxylist:
            proxy = random.choice(proxylist)
        processes.append(executor.submit(WindscribeCreator(output_file, semaphore).register_account, proxy))
print("\nFinished!")
