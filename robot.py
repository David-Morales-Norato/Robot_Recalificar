# -*- coding: utf-8 -*-
"""
By David M. Norato (2019)
5. Install ChromeDriver for Chrome V.77: 
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import time

RESCORE_STRING = "Escribir comentario o corregir la calificación"
def get_nuevo_driver_chrome(CHROME_DRIVER_PATH):
    return webdriver.Chrome(executable_path = CHROME_DRIVER_PATH)

def autenticacion_tic(driver, nickName, password):
    log = ''
    try:
        driver.get('https://tic.uis.edu.co/ava/login/index_ingreso.php')
        driver.maximize_window() 
        time.sleep(7)
        pregrado = driver.find_element_by_id('pregrado-head')
        pregrado.click()
        userName = driver.find_element_by_name('username')
        passWord = driver.find_element_by_name('password')

        userName.send_keys(nickName)
        passWord.send_keys(password)

        login_attempt = driver.find_element_by_xpath("//*[@id='send']")
        login_attempt.submit()
        ##########################
    except Exception as e:
        log += '| Fallo Al hacer autenticación| EXCEPTION: '+ str(e)
    return log

def recalificar_pregunta(driver,links_cursos,camino_cpl, CELLS,QUESTION_TITLE):
    log = ''
    nodes = camino_cpl.split("/")
    for link_curse in links_cursos:
        try:

            driver.get(link_curse)
            curse_title = driver.title
            log += "| Curso a modificar: " + curse_title
            for node in nodes:
                try:
                    driver.find_element_by_partial_link_text(node).click()
                except Exception as e:
                    log +="| Error en el camino al Cuestionario| Excepcion: "+ str(e)
                    break
            table = driver.find_element_by_id("attempts")
            main_window = driver.current_window_handle
            questions = table.find_elements_by_xpath(".//*[@title = 'Revisar respuesta']")
            for question in questions:
                question.click()
                handles = driver.window_handles
                driver.switch_to.window(handles[-1])
                quest_window = driver.current_window_handle
                if(QUESTION_TITLE in driver.title):
                    try:
                        log += "| Se va a modificar: " + driver.title
                        driver.find_element_by_link_text(RESCORE_STRING).click()
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.close()
                        #Modificar calificación
                        input_score = driver.find_element_by_xpath(".//div[@class = 'felement ftext']//input[@type = 'text']")
                        input_score.clear()
                        input_score.send_keys("1")
                        driver.find_element_by_id("id_submitbutton").click()
                        time.sleep(5)
                        driver.switch_to.window(quest_window)
                    except Exception as e:
                        log +="| Fallo al recalificar pregunta| EXCEPTION: " + str(e)
                driver.close()
                driver.switch_to.window(main_window)
        except Exception as e:
            log+="| Error al procesar curso: "+curse_title +"| EXCEPTION: "+ str(e)
    revisar_log(log)

def revisar_log(log):
    iter_ = log.split("|")
    for i in iter_:
        print(i)