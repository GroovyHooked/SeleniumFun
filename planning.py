import smtplib
import time
from email.message import EmailMessage

from selenium import webdriver
from selenium.webdriver.common.by import By

import config
from logic import getFinalData

# from var_dump import var_dump

# Option headless / Commenter cette section pour visualiser l'execution du script (supp options=options)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
# options.add_argument("window-size=700,1000")

# Choix du driver installé
driver = webdriver.Chrome("/Applications/MAMP/htdocs/selenium/chromedriver", options=options)

# On ouvre le navigateur à l'adresse voulue
driver.get('https://extranet.ynov.com/')

# Selection du champs email et insertion des données
emailXpath = driver.find_element(By.XPATH, "//*[@id=\"username\"]")
emailXpath.send_keys(config.ynov_mail)

# Selection du champs Mot de passe et insertion des données
passwordXpath = driver.find_element(By.XPATH, "//*[@id=\"password\"]")
passwordXpath.send_keys(config.ynov_password)

# Click sur le bouton de connexion
submitXpath = driver.find_element(By.XPATH, "//*[@id=\"login\"]/div[3]/div/input[4]")
submitXpath.click()
time.sleep(0.5)
# Click sur la section hyperPlanning
planingXpath = driver.find_element(By.XPATH, "//*[@id=\"2-2\"]/div[1]/div[1]")
planingXpath.click()

# Choix du campus dans le menu déroulant
selection_campus = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div/div[2]/div[2]/div/div/select")
selection_campus.click()
select_campus = driver.find_element(By.XPATH,
                                    "/html/body/main/div/div/div/div[2]/div/div[2]/div[2]/div/div/select/option[8]")
select_campus.click()

# On laisse la page se charger
time.sleep(2)
# week_test = driver.find_element(By.ID, 'GInterface.Instances[1].Instances[4]_j_11')
# week_test.click()
# time.sleep(1)
week = driver.find_element(By.ID, 'GInterface.Instances[1].Instances[4]_j_10').text
new_layout = 'Semaine ' + week + '\n\n'

first_class = getFinalData('id_98_coursInt_0', 'id_98_cours_0', driver)
if first_class is not False:
    new_layout += first_class
second_class = getFinalData('id_98_coursInt_1', 'id_98_cours_1', driver)
if second_class is not False:
    new_layout += second_class
third_class = getFinalData('id_98_coursInt_2', 'id_98_cours_2', driver)
if third_class is not False:
    new_layout += third_class
fourth_class = getFinalData('id_98_coursInt_3', 'id_98_cours_3', driver)
if fourth_class is not False:
    new_layout += fourth_class
fifth_class = getFinalData('id_98_coursInt_4', 'id_98_cours_4', driver)
if fifth_class is not False:
    new_layout += fifth_class
sixth_class = getFinalData('id_98_coursInt_5', 'id_98_cours_5', driver)
if sixth_class is not False:
    new_layout += sixth_class
seventh_class = getFinalData('id_98_coursInt_6', 'id_98_cours_6', driver)
if seventh_class is not False:
    new_layout += seventh_class

# Agencement du mail
# Se rendre sur https://myaccount.google.com/lesssecureapps pour autoriser son compte à être manipulé par des services tiers
# Config sans 2FA activé
msg = EmailMessage()
msg['Subject'] = "Planning de la semaine"
msg['From'] = config.mail_server
msg['To'] = config.ynov_mail
msg.set_content(new_layout)

# Envoi du mail

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(config.mail_server, config.server_password)
    smtp.send_message(msg)

"""         
def testData(data):
    return False if data == '' else True
    
height: 79 = 4h // height: 39 = 2h // height: 59 = 3h
left: 209 = mercredi // left: 314 = jeudi // left: 419 = vendredi
"""
