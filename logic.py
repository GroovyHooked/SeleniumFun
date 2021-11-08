from selenium.webdriver.common.by import By


# retourne top, left height
def getPositionValues(id, driver):
    element = ''
    try:
        element = driver.find_element(By.ID, id)
    finally:
        if element != '':
            element_style = element.get_attribute('style')
            split_string = element_style.split(';')
            left_px = split_string[3]
            left_px_int = int(''.join(filter(str.isdigit, left_px)))

            top_px = split_string[4]
            top_px_int = int(''.join(filter(str.isdigit, top_px)))

            height_px = split_string[6]
            height_px_int = int(''.join(filter(str.isdigit, height_px)))
            return (left_px_int, top_px_int, height_px_int)
        else:
            return False


# Extrait les horaires et le contenu des cours
def handlingClasses(id, driver):
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


# Compilation de toutes les données, retourne (top, left, height, horaire, infos cours)
def compileData(class_id, position_id, driver):
    course = handlingClasses(class_id, driver)

    if course is not False:
        data = getPositionValues(position_id, driver)
        return data + course
    else:
        return False


# Mise en page des données récupérées
def getLayout(course):
    global day, part_of_day, duration, timetable, infos, error
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
            duration = 'Durée inconnue'
    else:
        error = 'Un problème est survenu !'

    if course is not False:
        layout = day + ' ' + part_of_day + ' ' + duration + '\n\n' + timetable + '\n\n' + infos + \
                 '\n _______________________________________ \n\n'
        return layout
    else:
        return error


def getFinalData(class_id, position_id, driver):
    layout = getLayout(compileData(class_id, position_id, driver))
    if layout is not False:
        return layout
