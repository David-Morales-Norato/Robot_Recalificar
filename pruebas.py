from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import robot
import time

NICKNAME = "exper-tic"
PASSWORD = "exper-tic"

CELLS = ["mod-quiz-report-overview-report_r0_c10",
"mod-quiz-report-overview-report_r0_c11",
"mod-quiz-report-overview-report_r0_c12",
"mod-quiz-report-overview-report_r0_c13"]

QUESTION_TITLE = u'T02.01.26_B002_N0'

CURSES_LINK = "https://tic.uis.edu.co/ava/course/index.php?categoryid=926"

CHROME_DRIVER_PATH = "/home/david-norato/Documentos/EXPERTIC/QuimicaRobot/chromedriver_linux64/chromedriver"

camino_cpl = "Módulo 1/CPS1.4/Intentos: "

links_cursos = ["https://tic.uis.edu.co/ava/course/view.php?id=12123",
                "https://tic.uis.edu.co/ava/course/view.php?id=12124",
                "https://tic.uis.edu.co/ava/course/view.php?id=12095",
                "https://tic.uis.edu.co/ava/course/view.php?id=12094",
                "https://tic.uis.edu.co/ava/course/view.php?id=12093",
                "https://tic.uis.edu.co/ava/course/view.php?id=12092",
                "https://tic.uis.edu.co/ava/course/view.php?id=12091",
                "https://tic.uis.edu.co/ava/course/view.php?id=12090",
                "https://tic.uis.edu.co/ava/course/view.php?id=12089",
                "https://tic.uis.edu.co/ava/course/view.php?id=12088",
                "https://tic.uis.edu.co/ava/course/view.php?id=12087",
                "https://tic.uis.edu.co/ava/course/view.php?id=12086",
                "https://tic.uis.edu.co/ava/course/view.php?id=11605",
                "https://tic.uis.edu.co/ava/course/view.php?id=11593",
                "https://tic.uis.edu.co/ava/course/view.php?id=11586",
                "https://tic.uis.edu.co/ava/course/view.php?id=11599",
                "https://tic.uis.edu.co/ava/course/view.php?id=11598"]

wb = robot.get_nuevo_driver_chrome(CHROME_DRIVER_PATH)

robot.autenticacion_tic(wb,NICKNAME,PASSWORD)
robot.recalificar_pregunta(wb,links_cursos,camino_cpl, CELLS,QUESTION_TITLE)



# curses_page = wb.current_window_handle
# curses = wb.find_elements_by_partial_link_text("QUIMICA I: 2019-2-")
# for curse in curses:
#     try:
#         curse_name = curse.text
#         print("Se va a modificar el curso:" + curse_name)
#         wb.execute_script("window.open('"+curse.get_attribute("href") +"')")
#         wb.switch_to.window(wb.window_handles[-1])    
#         wb.find_element_by_link_text("Módulo 1").click()
#         wb.find_element_by_link_text("CPS1.4").click()
#         wb.find_element_by_partial_link_text("Intentos: ").click()
#         table = wb.find_element_by_id("attempts")
#         contador = 0
#         main_window = wb.current_window_handle
#         rows = table.find_element_by_tag_name("tbody").find_elements_by_xpath(".//tr")
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
#                         if(unicode(QUESTION_TITLE) in unicode(wb.title)):
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
# quit()
