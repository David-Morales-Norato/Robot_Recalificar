
"""
By David M. Norato (2019)
5. Install ChromeDriver for Chrome V.77: 
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import time

class Robot:
    
    def __init__(self, CHROME_DRIVER_PATH):
        self.log = ''
        self.driver = webdriver.Chrome(executable_path = CHROME_DRIVER_PATH)
        self.__RESCORE_STRING = "Escribir comentario o corregir la calificación"
        self.__LOGS = ["|[-1] Fallo Al hacer autenticación| EXCEPTION: ",
                        "|[1] Curso a modificar: ",
                        "|[-2] Error en el camino al Cuestionario| Exception: ",
                        "|[2] Se va a modificar: ",
                        "|[3] Pregunta modificada satisfactoriamente ",
                        "|[-3] Fallo al recalificar pregunta| EXCEPTION: ",
                        "|[4] Curso terminado satisfactoriamente",
                        "|[-4] Error al procesar curso: "]


    def autenticacion_tic(self, nickName, password):
        try:
            self.driver.get('https://tic.uis.edu.co/ava/login/index_ingreso.php')
            self.driver.maximize_window() 
            time.sleep(7)
            pregrado = self.driver.find_element_by_id('pregrado-head')
            pregrado.click()
            userName = self.driver.find_element_by_name('username')
            passWord = self.driver.find_element_by_name('password')

            userName.send_keys(nickName)
            passWord.send_keys(password)

            login_attempt = self.driver.find_element_by_xpath("//*[@id='send']")
            login_attempt.submit()
            ##########################
        except Exception as e:
            self.log += self.__LOGS[0]+ str(e)

    def recalificar_pregunta(self,links_cursos,camino_cpl,questioin_id, nota):
        nodes = camino_cpl#.split("/")
        for link_curse in links_cursos:
            try:

                self.driver.get(link_curse)
                curse_title = self.driver.title
                self.log += self.__LOGS[1] + curse_title
                for node in nodes:
                    try:
                        self.driver.find_element_by_partial_link_text(node).click()
                    except Exception as e:
                        self.log +=self.__LOGS[2]+ str(e)
                        break
                table = self.driver.find_element_by_id("attempts")
                main_window = self.driver.current_window_handle
                questions = table.find_elements_by_xpath(".//*[@title = 'Revisar respuesta']")
                for question in questions:
                    question.click()
                    handles = self.driver.window_handles
                    self.driver.switch_to.window(handles[-1])
                    quest_window = self.driver.current_window_handle
                    if(questioin_id in self.driver.title):
                        try:
                            self.log += self.__LOGS[3] + self.driver.title
                            self.driver.find_element_by_link_text(self.__RESCORE_STRING).click()
                            self.driver.switch_to.window(self.driver.window_handles[-1])
                            input_score = self.driver.find_element_by_xpath(".//div[@class = 'felement ftext']//input[@type = 'text']")
                            input_score.clear()
                            input_score.send_keys(nota)
                            self.driver.find_element_by_id("id_submitbutton").click()
                            time.sleep(5)
                            self.log += self.__LOGS[4]
                            self.driver.switch_to.window(quest_window)
                        except Exception as e:
                            self.log +=self.__LOGS[5] + str(e)
                    self.driver.close()
                    self.driver.switch_to.window(main_window)
                    self.log+=self.__LOGS[6]
            except Exception as e:
                self.log+=self.__LOGS[7]+curse_title +"| EXCEPTION: "+ str(e)

        
    def revisar_log(self):
        cursos_procesados = self.log.count("[1]")
        preguntas_procesadas = self.log.count("[2]")
        preguntas_exitosas = self.log.count("[3]")
        cursos_exitosos = self.log.count("[4]")
        fallos_camino = self.log.count("[-2]")
        preguntas_fallidas = self.log.count("[-3]")
        cursos_fallidos = self.log.count("[-4]")
        print("Total cursos procesados: "+ str(cursos_procesados))
        print("Total cursos recorridos exitosamente: "+ str(cursos_exitosos))
        print("Total cursos recorridos incorrectamente: "+ str(cursos_fallidos))
        print("Total cursos con fallo en el camino a resultados: "+ str(fallos_camino))
        print("Total preguntas procesadas: "+ str(preguntas_procesadas))
        print("Total preguntas fallidas a procesar: "+ str(preguntas_fallidas))
        print("Total preguntas modificadas correctamente: "+ str(preguntas_exitosas))
        
