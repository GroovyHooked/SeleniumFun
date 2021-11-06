import smtplib
import config
from email.message import EmailMessage

from selenium import webdriver

import time

# from var_dump import var_dump
from selenium.webdriver.common.by import By

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
emailXpath.send_keys(config.send_to)

# Selection du champs Mot de passe et insertion des données
passwordXpath = driver.find_element(By.XPATH, "//*[@id=\"password\"]")
passwordXpath.send_keys(config.pass_to)

# Click sur le bouton de connexion
submitXpath = driver.find_element(By.XPATH, "//*[@id=\"login\"]/div[3]/div/input[4]")
submitXpath.click()

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


# Changement de semaine à des fins de test
# week = driver.find_element(By.ID, 'GInterface.Instances[1].Instances[4]_j_5')
# week.click()
# time.sleep(2)

# retourne top, left height
def getPositionValues(id):
    element = ''
    try:
        element = driver.find_element(By.ID, id)
    finally:
        if element != '':
            element_style = element.get_attribute('style')
            split_string = element_style.split(';')
            # print(split_string)
            left_px = split_string[3]
            left_px_int = int(''.join(filter(str.isdigit, left_px)))

            top_px = split_string[4]
            top_px_int = int(''.join(filter(str.isdigit, top_px)))

            height_px = split_string[6]
            height_px_int = int(''.join(filter(str.isdigit, height_px)))
            return (left_px_int, top_px_int, height_px_int)
        else:
            return ''


# Extrait les horaires et le contenu des cours
def handlingClasses(id):
    class_infos = ''
    try:
        class_infos = driver.find_element(By.ID, id)
    finally:
        if (class_infos != ''):
            class_infos = driver.find_element(By.ID, id)
            class_hours = class_infos.get_attribute('title')
            return class_hours, class_infos.text
        else:
            return False


# retourne (top, left, height, horaire, infos cours)
def compileData(class_id, position_id):
    course = handlingClasses(class_id)

    if course is not False:
        data = getPositionValues(position_id)
        return data + course
    else:
        return False


# Mise en page des données récupérées
def getLayout(course):
    if course is not False:
        left = course[0]
        top = course[1]
        height = course[2]
        timetable = course[3]
        infos = course[4]

        if left == 209:
            day = 'Mercredi'
        elif left == 314:
            day = 'Jeudi'
        elif left == 419:
            day = 'Vendredi'
        else:
            day = 'Jour inconnu '

        if top < 100:
            part_of_day = 'Matin'
        else:
            part_of_day = 'Après midi'

        if height == 79:
            duration = '(4h)'
        elif height == 59:
            duration = '(3h)'
        elif height == 39:
            duration = '(2h)'
    else:
        error = 'Un problème est survenu !'

    if day:
        layout = day + ' ' + part_of_day + ' ' + duration + '\n\n' + timetable + '\n\n' + infos + \
                 '\n _______________________________________ \n\n'
        return layout
    else:
        return error


# cours_0 = compileData('id_98_coursInt_0', 'id_98_cours_0')
def getFinalData(class_id, position_id):
    layout = getLayout(compileData(class_id, position_id))
    if layout is not False:
        return layout


new_layout = ''
first_class = getFinalData('id_98_coursInt_0', 'id_98_cours_0')
if first_class is not None:
    new_layout += first_class
second_class = getFinalData('id_98_coursInt_1', 'id_98_cours_1')
if second_class is not None:
    new_layout += second_class
third_class = getFinalData('id_98_coursInt_2', 'id_98_cours_2')
if third_class is not None:
    new_layout += third_class
fourth_class = getFinalData('id_98_coursInt_3', 'id_98_cours_3')
if fourth_class is not None:
    new_layout += fourth_class
fifth_class = getFinalData('id_98_coursInt_4', 'id_98_cours_4')
if fifth_class is not None:
    new_layout += fifth_class
sixth_class = getFinalData('id_98_coursInt_5', 'id_98_cours_5')
if sixth_class is not None:
    new_layout += sixth_class

# Agencement du mail
# Se rendre sur https://myaccount.google.com/lesssecureapps pour autoriser son compte à être manipulé par des services tiers
# Config sans 2FA activé

msg = EmailMessage()
msg['Subject'] = "Planning de la semaine"
msg['From'] = config.mail_server
msg['To'] = config.send_to
msg.set_content(new_layout)

# Envoi du mail
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(config.mail_server, config.password)
    smtp.send_message(msg)

"""         
def testData(data):
    return False if data == '' else True
    
week = driver.find_element(By.ID, 'GInterface.Instances[1].Instances[4]_j_8')
week.click()
time.sleep(2)


cours_0 = left: 209; top: 19; height: 79;
cours_1 = left: 209; top: 119; height: 79;
cours_2 = left: 314; top: 19; height: 79;
cours_3 = left: 314; top: 119; height: 79;
cours_4 = left: 419; top: 19; height: 79;
cours_5 = left: 419; top: 119; height: 79;
height: 79 = 4h // height: 39 = 2h // height: 59 = 3h
left: 209 = mercredi // left: 314 = jeudi // left: 419 = vendredi
"""
