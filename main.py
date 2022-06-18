from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import string
from selenium.webdriver.common.action_chains import ActionChains
import re
import requests
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool
from licensing.models import *
from licensing.methods import Key, Helpers
import sys
from datetime import date
import os
from colorama import Fore, Back, Style
#from geoip import geolite2
global regionsBRUH
regionsBRUH = []
totalcounter = 0
failedaccounts = 0
chrome_options = Options()
os.system(f"title LeagueKingdom Account Creator ({totalcounter} Accounts Created, {failedaccounts} Accounts Failed)")
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--silent")
PATH = r"chromedriver.exe"
naURL = r"https://signup.na.leagueoflegends.com/en/signup/index#/"
euwURL = r"https://signup.euw.leagueoflegends.com/en/signup/index#/"
euneURL = r"https://signup.eune.leagueoflegends.com/en/signup/index"
lanURL = r"https://signup.lan.leagueoflegends.com/"
lasURL = r"https://signup.las.leagueoflegends.com/"
ruURL = r"https://signup.ru.leagueoflegends.com/"
trURL = r"https://signup.tr.leagueoflegends.com/"
oceURL = r"https://signup.oce.leagueoflegends.com/"
brURL = r"https://signup.br.leagueoflegends.com/"
capKEY = open('2captchakey.txt', 'r')
capKEY = capKEY.readline()
capKEY = capKEY.strip()
logo = r"""
   _            _  __                _   _     ____   ____      U  ___ u  __  __   
  |"|          |"|/ /       ___     | \ |"| U /"___|u|  _"\      \/"_ \/U|' \/ '|u 
U | | u        | ' /       |_"_|   <|  \| |>\| |  _ /| | | |     | | | |\| |\/| |/ 
 \| |/__     U/| . \\u      | |    U| |\  |u | |_| |U| |_| |\.-,_| |_| | | |  | |  
  |_____|      |_|\_\     U/| |\u   |_| \_|   \____| |____/ u \_)-\___/  |_|  |_|  
  //  \\     ,-,>> \\,-.-,_|___|_,-.||   \\,-._)(|_   |||_         \\   <<,-,,-.
 (_")("_)     \.)   (_/ \_)-' '-(_/ (_")  (_/(__)__) (__)_)       (__)   (./  \.)
 """
def passCreate(stringLength):
    letters = string.ascii_letters
    bruh5 = ''.join(random.choice(letters) for i in range(stringLength))
    bruh5 = bruh5+str(random.randint(1,9))
    return bruh5
def generateName():
    s = open("names.txt", "r")
    m=s.readlines()
    l = []
    for i in range(0,len(m)-1):
        x=m[i]
        z=len(x)
        a=x[:z-1]
        l.append(a)
    l.append(m[i+1])
    o=random.choice(l)
    s.close()

    return o
def getName():
    wordFirst = generateName()
    wordSecond = generateName()
    name = (wordFirst+wordSecond+str(random.randint(100,999)))
    return name

def sendRequest(p):
        result = re.search("k=(.*)&amp;co", p)

        kKey = (result.group(1))
        print ("Found Captcha Key")
        captchaURL = 'https://2captcha.com/in.php?key='+capKEY+'&method=userrecaptcha&googlekey='+kKey+'&pageurl=https://signup.na.leagueoflegends.com/en/signup/index#/registration'
        #print (captchaURL)
        captchaGet = requests.get(captchaURL)
        #print(captchaGet)
        print("Sending Request to 2Captcha Servers")
        pogID = captchaGet.content
        pogID = str(pogID)
        pogID = pogID.split('|')
        pogID = pogID[1]
        pogID = pogID.replace("'",'')
        return pogID

cls = lambda: os.system('cls')
           
def auth():
    aEnteredKey = open("license.txt")
    LicenseKey = aEnteredKey.read()
    LicenseKey = LicenseKey.strip()


    RSAPubKey = "<RSAKeyValue><Modulus>oSSuzYFTfCvQMSR7r8Uc+fB7teHfcVMkmMMc0bmzajll4lpFYK3E21NcA2OVsxcZXjgO3wnrsF358QOwdK7R1auAlNGBZjiRU2f+u/zNcItc/CM5p08BWK4ikpXm73cpBYWcLQTFQQtzRf3W6UjWv7q2aXM1Fzphg8gFhWJ0Dz0PBdHncqzNMZ2XHd+7xHsDKovHScF472NXQ+M31QDK7WZnZ1nGdWibOFd91ohtt+sOECDM678XPMNaC5ok6xtR0EIaLyTbBeIL15uQAnUtN2mTRYNRIq5rJdF75kMl9l97QmfKP+6+Ix6Vqmm9IVJnbQ0hFE4+bS2UM4mXOjW0hQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
    auth = "WyIyOTQyOCIsInN1UzhTSHJ2ZThWRFNNTVJQTGhsYitJdU5GeUhHb2ZURVpneHlPdUgiXQ=="

    result = Key.activate(token=auth,\
                       rsa_pub_key=RSAPubKey,\
                       product_id=7195, \
                       key=LicenseKey,\
                       machine_code=Helpers.GetMachineCode())

    if result[0] == None or not Helpers.IsOnRightMachine(result[0]):
        print("The license does not work: {0}".format(result[1]))
        time.sleep(5)
        sys.exit()
        
    else:
        Menu()
    
def runRegion(region, loop):
    region = region.lower()
    for h in range(loop):
        if region == 'euw':                
            startGEN(euwURL, 'EUW')
        elif region == 'na':
            startGEN(naURL, 'NA')
        elif region == 'eune':
            startGEN(euneURL, 'EUNE')
        elif region == 'lan':
            startGEN(lanURL, 'LAN')
        elif region == 'las':
            startGEN(lasURL, 'LAS')
        elif region == 'br':
            startGEN(brURL, 'BR')
        elif region == 'tr':
            startGEN(trURL, 'TR')
        elif region == 'ru':
            startGEN(ruURL, 'RU')
        elif region == 'oce':
            startGEN(oceURL, 'OCE')
            
        
def solve(cKEY, idPOGGER):
    captchaResult = requests.get('https://2captcha.com/res.php?key='+cKEY+'&action=get&id='+idPOGGER)
    #print (captchaResult.content)
    print ("Waiting for Captcha to be solved")
    captchaRESULT = str(captchaResult.content)
    return captchaRESULT
    
def recovery(region):
    y = open(f"{region}_GENNED/"+region+"_GENNED_RECOVERY.txt", "a")
    getDate = date.today()
    ip = requests.get('https://api.ipify.org').text

    ip_address = str(ip)
    #match = geolite2.lookup(ip_address)

    getDate = str(getDate)
    y.write(accountNAME+":"+accountPASS+":"+getDate+":"+ip_address+":"+"February 1st 2003"+"\n")
    

def startGEN(URLURL, region):
    try:
        cls()
        global totalcounter

        global failedaccounts
        os.system(f"title LeagueKingdom Account Creator ({totalcounter} Accounts Created, {failedaccounts} Accounts Failed)")

        if not os.path.exists(f"{region}_GENNED"):
            os.makedirs(f"{region}_GENNED")
        driver = webdriver.Chrome(PATH, options=chrome_options)
        driver.get(URLURL)
        time.sleep(2)
        global accountNAME 
        global accountPASS
        accountNAME = getName()
        accountPASS = passCreate(8)
        print("Account details: "+accountNAME+":"+accountPASS)
        with open(f"{region}_GENNED/{region}_GENNED.txt", "a") as p:
            print(f"Filling out account creation forums for a(n) {regionsBRUH[0]} account")
            
            
            search = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[1]/input""")
            search.send_keys(accountNAME+'@gmail.com')
            time.sleep(2)
            search.send_keys(Keys.RETURN)
            time.sleep(2)
            dobMONTH = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[1]/div[2]/select""")
            dobMONTH.send_keys(Keys.RETURN)
            dobMONTH.send_keys(Keys.DOWN)
            dobMONTH.send_keys(Keys.DOWN, Keys.RETURN)

            dobDAY = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[1]/div[3]/select""")
            dobDAY.send_keys(Keys.RETURN)
            dobDAY.send_keys(Keys.DOWN, Keys.RETURN)
            dobYEAR = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[1]/div[4]/select""")
            dobYEAR.send_keys(Keys.RETURN)
            for bruh in range(18):
                dobYEAR.send_keys(Keys.DOWN)
            dobYEAR.send_keys(Keys.RETURN)
            nextDOB = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[2]/button""").click()
            time.sleep(1)

            enterUSER = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[1]/input""")
            enterUSER.send_keys(accountNAME)
            time.sleep(1)
            enterPASS = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[2]/input""")
            enterPASS.send_keys(accountPASS)
            time.sleep(1)
            enterPASS2 = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[3]/input""")
            enterPASS2.send_keys(accountPASS)
            time.sleep(1)
            agree1 = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[4]/label/div""").click()

            time.sleep(1)
            agree2 = driver.find_element_by_xpath("""//*[@id="root"]/div/div/div[2]/div[1]/form/div[5]/label/div""").click()
            
            time.sleep(1)

            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            kValue = soup.find("div", {"class": "grecaptcha-logo"})
            kValue = str(kValue)
            
           
            s = kValue
            
            pogID = sendRequest(s)
            print (f"2Captcha Request ID: {pogID}")
            time.sleep(20)
            resultfromcap = solve(capKEY, pogID)
            
            while "NOT_READY" in resultfromcap:
                time.sleep(10)
                resultfromcap = solve(capKEY, pogID)
             
                

                if "OK" in resultfromcap:
                    break
                else:
                    pass
                if "UNSOLVABLE" in resultfromcap:
                    print("UNSOLVABLE")
                    time.sleep(5)
                    counterbreak = 0
                    pogID = sendRequest(s)
                    print (pogID)
                    time.sleep(20)
                    resultfromcap = solve(capKEY, pogID)
                    while "NOT_READY" in resultfromcap:
                        time.sleep(10)
                        resultfromcap = solve(capKEY, pogID)
             
                

                    if "OK" in resultfromcap:
                        break
                    else:
                        pass
                
                else:
                    pass

               
            captchaSucess = str(resultfromcap)
            captchaSucess = captchaSucess.split("|")
            captchaSucess = captchaSucess[1]
            captchaSucess = captchaSucess.replace("'",'')
            captchaSuccess = ("document.getElementById(\"g-recaptcha-response\").innerHTML=""\""+captchaSucess+"\";")
            print("Captcha SOLVED")
            driver.execute_script(captchaSuccess)
            actions = ActionChains(driver)
            actions.send_keys(Keys.TAB, Keys.RETURN)
            actions.perform()
            time.sleep(5)
            soup2 = BeautifulSoup(driver.page_source, 'html.parser')
            win = soup2.find("button", {"class": "download-button"})
            try:
                win = win.text
            except:
                pass
            
            if win is not None:
                p.write(accountNAME+":"+accountPASS+"\n")#+":"+accountNAME+"@gmail.com\n")
                recovery(region)
                cls()
                totalcounter = totalcounter + 1
                os.system(f"title LeagueKingdom Account Creator ({totalcounter} Account(s) Created, {failedaccounts} Accounts Failed)")

                print(f"Account Created, {totalcounter} account(s) created so far")           
            else:
                failedaccounts = failedaccounts + 1

                print("Account Creation Failed")

            time.sleep(2)
            driver.quit()
    except:
        failedaccounts = failedaccounts + 1
        return
       


            


def Menu():
    
    

    print(Fore.CYAN)
    print(logo)
    print("-----------------------------------------------------------------------------")
    print("- NA")
    print("- EUW")
    print("- EUNE")
    print("- LAN")
    print("- LAS")
    print("- BR")
    print("- TR")
    print("- RU")
    print("- OCE")
    print("Please select the regions seperated by a comma (not capital sensitive)\neg: na, euw, eune\neg:na")
    chick = input().lower().split(',')
    loop = int(input("How many accounts would you like to create (this will apply for all regions): "))

    while len(chick) != 0:
        
        regionsBRUH.append(chick[0].replace(" ", ""))
        
        chick.pop(0)
        print (regionsBRUH)
    
    for j in range(len(regionsBRUH)):
        runRegion(regionsBRUH[0], loop)
        regionsBRUH.pop(0)
        
        
    
    



#auth()
Menu()
cls()
print(f"All accounts created, {totalcounter} successfully created and {failedaccounts} failed.")
input("Please press enter to close the program")

