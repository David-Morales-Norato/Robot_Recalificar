from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
#import robot
import time

# CELLS = ["mod-quiz-report-overview-report_r0_c10",
# "mod-quiz-report-overview-report_r0_c11",
# "mod-quiz-report-overview-report_r0_c12",
# "mod-quiz-report-overview-report_r0_c13"]

CELLS = ["cell c10",
        "cell c11",
        "cell c12",
        "cell c13"]

QUESTION_TITLE = 'T02.01.01_B002_N0'

CURSES_LINK = "https://tic.uis.edu.co/ava/course/index.php?categoryid=926"

CHROME_DRIVER_PATH = "/home/david-norato/Documentos/EXPERTIC/QuimicaRobot/chromedriver_linux64/chromedriver"
wb = webdriver.Chrome(executable_path = CHROME_DRIVER_PATH)

nickName = "exper-tic"
password = "exper-tic"
wb.get('https://tic.uis.edu.co/ava/login/index_ingreso.php')
wb.maximize_window() 
time.sleep(7)
pregrado = wb.find_element_by_id('pregrado-head')
pregrado.click()
userName = wb.find_element_by_name('username')
passWord = wb.find_element_by_name('password')

userName.send_keys(nickName)
passWord.send_keys(password)

login_attempt = wb.find_element_by_xpath("//*[@id='send']")
login_attempt.submit()

wb.get(CURSES_LINK)
curses_page = wb.current_window_handle
curses = wb.find_elements_by_partial_link_text("QUIMICA I: 2019-2-")
for curse in curses:
    try:
        curse_name = curse.text
        print("Se va a modificar el curso:" + curse_name)
        wb.execute_script("window.open('"+curse.get_attribute("href") +"')")
        wb.switch_to.window(wb.window_handles[-1])
        wb.find_element_by_link_text("Módulo 1").click()
        wb.find_element_by_link_text("CPS1.4").click()
        wb.find_element_by_partial_link_text("Intentos: ").click()
        table = wb.find_element_by_id("attempts")
        main_window = wb.current_window_handle
        questions = table.find_elements_by_xpath(".//*[@title = 'Revisar respuesta']")
        for question in questions:
            question.click()
            handles = wb.window_handles
            wb.switch_to.window(handles[-1])
            quest_window = wb.current_window_handle
            print(QUESTION_TITLE)
            print(wb.title)
            if(QUESTION_TITLE in wb.title):
                find = True
                try:
                    print("Se va a modificar: " + wb.title)
                    wb.find_element_by_link_text("Escribir comentario o corregir la calificación").click()
                    wb.switch_to.window(wb.window_handles[-1])
                    wb.close()
                    #Modificar calificación
                    # input_score = wb.find_element_by_xpath(".//div[@class = 'felement ftext']//input[@type = 'text']")
                    # input_score.clear()
                    # input_score.send_keys("1")
                    # wb.find_element_by_id("id_submitbutton").click()
                    # time.sleep(5)
                    wb.switch_to.window(quest_window)
                except NoSuchElementException as e:
                    print("Fallo al recalificar pregunta")
                except Exception as e:
                    print(e)
            wb.close()
            wb.switch_to.window(main_window)
    except NoSuchElementException as e:
        print("Error al procesar curso: "+curse_name)
    except StaleElementReferenceException as e:
        wb.close()
        wb.switch_to.window(curses_page)


#time.sleep(10)
print("Salida del programa")
wb.close()
        
#         for row in rows:
#             try:
#                 find = False
#                 for cell in CELLS:
#                     str_cell = 'r'+str(contador)
#                     cell = cell.replace('r0',str_cell)
#                     row.find_element_by_id(cell).click()
#                     handles = wb.window_handles
#                     if handles[-1] != main_window:
#                         wb.switch_to.window(handles[-1])
#                         quest_window = wb.current_window_handle
#                         if(QUESTION_TITLE in wb.title):
#                             find = True
#                             try:
#                                 print("Se va a modificar: " + wb.title)
#                                 wb.find_element_by_link_text("Escribir comentario o corregir la calificación").click()
#                                 wb.switch_to.window(wb.window_handles[-1])
#                                 #Modificar calificación
#                                 input_score = wb.find_element_by_xpath(".//div[@class = 'felement ftext']//input[@type = 'text']")
#                                 input_score.clear()
#                                 input_score.send_keys("1")
#                                 wb.find_element_by_id("id_submitbutton").click()
#                                 time.sleep(5)
#                                 wb.switch_to.window(quest_window)
#                             except NoSuchElementException as e:
#                                 print("Fallo al recalificar pregunta")
#                             except Exception as e:
#                                 print(e)
#                     wb.close()
#                     wb.switch_to.window(main_window)
#                 contador +=1
#                 if(not find):
#                     print("No ha encontrado para este estudiante")
#             except NoSuchElementException as e:
#                 print("Final curso")
#             except Exception as e:
#                 print(e)
#         print("Curso finalizado")
#         wb.close()
#         wb.switch_to.window(curses_page)
#     except NoSuchElementException as e:
#         print("Error al procesar curso: "+curse_name)
#     except Exception as e:
#         print(e)
# #time.sleep(10)
# print("Salida del programa")
# wb.close()