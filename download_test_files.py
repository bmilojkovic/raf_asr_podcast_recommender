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
path_dataset = r'C:\Users\Luka\Desktop\dataset' # ovde staviti gde zelite da sacuvate podatke

#Izbor reci za testiranje
lista_reci = []

#Imati na umu da se moze desiti da neka rec nema zeljeni broj snimaka
limit_downloads = True  #ako stavite false skinuce sve snimke za rec
max_downloads_per_world = 2


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

#prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
#chrome_options.add_experimental_option("prefs", prefs)
path_download = path_dataset +"\download_folder"

if not os.path.exists(path_download):
    os.makedirs(path_download)
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1200x600')
chrome_options.add_argument("--silent")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument('--disable-gpu') 
prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": 
                        path_download+"\\",
             "directory_upgrade": True,
             'profile.default_content_setting_values.automatic_downloads': 1}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(executable_path=path_chromedriver,chrome_options=chrome_options)

driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': path_download}}
command_result = driver.execute("send_command", params)

print("LOGIN ON: https://forvo.com/login/")
driver.get("https://forvo.com/login/")
print("ENTERING USERNAME")
driver.find_element_by_id("login").send_keys(username)
print("ENTERING PASSWORD")
driver.find_element_by_id("password").send_keys(password)

e = driver.find_element_by_class_name("button")
driver.execute_script("arguments[0].click();", e)



url_words = "https://forvo.com/languages-pronunciations/en/"
print("LOGGED IN")
print("GATHERING WORDS")
page_delimiter = "page-"
driver.get(url_words)
re = requests.get(url_words)
searchsoup = BeautifulSoup(re.text,"html.parser")
c = searchsoup.find_all("a", {"class": "word"})
for k in c:
    if " " not in k.text:
        lista_reci.append(k.text)
for i in range(2,21):
    url_tmp = url_words + page_delimiter + str(i)
    driver.get(url_tmp)
    re = requests.get(url_tmp)
    searchsoup = BeautifulSoup(re.text,"html.parser")
    c = searchsoup.find_all("a", {"class": "word"})
    for k in c:
        lista_reci.append(k.text)
print("GATHERING FINISHED")
print("DOWNLOADING WORDS")
for r in range(len(lista_reci)):

    url_word = lista_reci[r].strip().lower().replace(" ", "_")
    url = "https://forvo.com/word/" + url_word + "/"
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
        
        file_path = max([path_download + '\\' + f for f in os.listdir(path_download)],key=os.path.getctime)
        file_name = file_path.replace(path_download+"\\","")
        file_name = file_name.replace(".mp3","") + " " + str(k) + ".mp3"
        os.rename(file_path, path_download +"\\"+ file_name)
        
        info = splitter(str(a))
        gender = info[0]
        location = info[1]
        
        if not os.path.exists(path_dataset + "\\" + lista_reci[r] + "\\" + gender + "\\" + location):
           os.makedirs(path_dataset + "\\" + lista_reci[r] + "\\" + gender + "\\" + location)  
        
        os.replace(path_download  +"\\"+ file_name, path_dataset + "\\" + lista_reci[r] + "\\" + gender + "\\" + location + "\\" + file_name)

        print("--->CREATED " + path_dataset + "\\" + lista_reci[r] + "\\" + gender + "\\" + location + "\\" + file_name)

os.rmdir(path_download)
print("----->FINISHED<-----")
driver.quit()
