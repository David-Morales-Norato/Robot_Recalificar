# -*- coding: utf-8 -*-
"""
By David M. Norato (2019)
5. Install ChromeDriver for Chrome V.77: 
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

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
        log += '/Fallo Al hacer autenticación. e: '+ str(e)
    return log

def recalificar_pregunta(driver,links_cursos,camino_cpl, CELLS,QUESTION_TITLE):
    log = ''
    nodes = camino_cpl.split("/")
    for link_curse in links_cursos:
        try:
            log+="Se va a modificar el curso:" + link_curse
            driver.get(link_curse)
            for node in nodes:
                driver.find_element_by_partial_link_text(node).click()
            table = driver.find_element_by_id("attempts")
            contador = 0
            main_window = driver.current_window_handle
            rows = table.find_element_by_tag_name("tbody").find_elements_by_xpath(".//tr")
            for row in rows:
                try:
                    find = False
                    contador_cell = -1
                    for cell in CELLS:
                        contador_cell +=1
                        str_cell = 'r'+str(contador)
                        cell = cell.replace('r0',str_cell)
                        row.find_element_by_id(cell).click()
                        if(len(driver.window_handles) <2):
                            contador_cell +=1
                            str_cell = '_c'+str(10+contador)
                            cell = cell.replace('_c',str_cell)
                            print(cell)
                            row.find_element_by_id(cell).click()
                        handles = driver.window_handles
                        driver.switch_to.window(handles[-1])
                        quest_window = driver.current_window_handle
                        if(QUESTION_TITLE in driver.title):
                            find = True
                            try:
                                print("Se va a modificar: " + driver.title)
                                driver.find_element_by_link_text("Escribir comentario o corregir la calificación").click()
                                driver.switch_to.window(driver.window_handles[-1])
                                #Modificar calificación
                                input_score = driver.find_element_by_xpath(".//div[@class = 'felement ftext']//input[@type = 'text']")
                                input_score.clear()
                                input_score.send_keys("1")
                                driver.find_element_by_id("id_submitbutton").click()
                                time.sleep(5)
                                driver.switch_to.window(quest_window)
                            except NoSuchElementException as e:
                                print("Fallo al recalificar pregunta")
                            except Exception as e:
                                print(e)
                        driver.close()
                        driver.switch_to.window(main_window)
                    contador +=1
                    if(not find):
                        print("No ha encontrado para este estudiante")
                except NoSuchElementException as e:
                    print("Final curso")
                except Exception as e:
                    print(e)
            print("Curso finalizado")
        except NoSuchElementException as e:
            print("Error al procesar curso: "+link_curse)
        except Exception as e:
            print(e)

