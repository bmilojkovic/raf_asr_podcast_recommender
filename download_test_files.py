import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

#za pokretanje skripte skinuti:
#selenium : pip install selenium
#requests : pip install requests
#BeautifulSoup : pip install bs4
#Snikuti takodje googleChrome driver sa linka: https://chromedriver.chromium.org/downloads, a verziju chrom-a mozete videti u Help->About Google Chrome
#Dodati chromedriver.exe u path

#Sistemska podesavanja
path_chromedriver = r"C:\Users\Luka\Desktop\chromedriver\chromedriver.exe"
path_dataset = r'C:\Users\Luka\Desktop\dataset' # ovde staviti gde zelite da drzite podatke
path_download = r"C:\Users\Luka\Downloads" #ovde staviti path gde vam se skidaju fajlovi(ne gde zelite)

#Izbor reci za testiranje
lista_reci = ("water","book")

#Imati na umu da se moze desiti da neka rec nema zeljeni broj snimaka
limit_downloads = True   #ako stavite false skinuce sve snimke za rec
max_downloads_per_world = 30


#pozeljno koristiti svoj podatke da ne bismo dobili ban
username = "luxe05"
password = "ooksnp1234"
################################################################################
def splitter(string):
    s = string.split()
    pol = s[0]
    rec = ""
    if len(s) > 3:
        for i in range(2,len(s)):
            rec = rec + s[i] + " " 
    else:
        rec = s[2]    
    return [pol,rec.strip()]

chrome_options = Options()

prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path=path_chromedriver,chrome_options=chrome_options)
driver.get("https://forvo.com/login/")
driver.find_element_by_id("login").send_keys(username)
driver.find_element_by_id("password").send_keys(password)

e = driver.find_element_by_class_name("button")
driver.execute_script("arguments[0].click();", e)

if not os.path.exists(path_dataset):
   os.makedirs(path_dataset)

for r in range(len(lista_reci)):

    url = "https://forvo.com/word/" + lista_reci[r] + "/"
    driver.get(url)
    title = "Download "+ lista_reci[r] + " MP3 pronunciation"
    element = driver.find_elements_by_xpath('//*[@title="Download '+ lista_reci[r] +  ' MP3 pronunciation"]')

    
    if not os.path.exists(path_dataset + "\\" + lista_reci[r]):
       os.makedirs(path_dataset + "\\" + lista_reci[r])

    re = requests.get("https://forvo.com/word/" + lista_reci[r])
    searchsoup = BeautifulSoup(re.text,"html.parser")
    c = searchsoup.find_all("span", {"class": "from"})
    
    if limit_downloads:
        number = max_downloads_per_world
    else:
        number = len(c)
        
    for k in range(number):
        
        a = c[k].text.strip("(").strip(")")
        if "Male" not in a and "Female" not in a:
            continue
        driver.execute_script("arguments[0].click();",element[k])
        time.sleep(5)
        
        file_path = max([path_download + "\\" + f for f in os.listdir(path_download)],key=os.path.getctime)
        file_name = file_path.strip(path_download)
        file_name = file_name.strip(".mp3") + " " + str(k) + ".mp3"
        os.rename(file_path, path_download + "\\" + file_name)
        
        info = splitter(str(a))
        gender = info[0]
        location = info[1]
        
        if not os.path.exists(path_dataset + "\\" + lista_reci[r] + "\\" + gender + "\\" + location):
           os.makedirs(path_dataset + "\\" + lista_reci[r] + "\\" + gender + "\\" + location)
           
        
        os.replace(path_download + "\\"  + file_name, path_dataset + "\\" + lista_reci[r] + "\\" + gender + "\\" + location + "\\" + file_name)

        print("--->CREATED " + path_dataset + "\\" + lista_reci[r] + "\\" + gender + "\\" + location + "\\" + file_name)
driver.quit()
print("----->FINISHED<-----")
