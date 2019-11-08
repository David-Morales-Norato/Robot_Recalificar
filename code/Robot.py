
"""
By David Morales Norato (2019)

Coming soon
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
import time

class Robot:
    
    def __init__(self, CHROME_DRIVER_PATH):
        ## Inicializaciones

        self.log = ''
        # El driver del robot
        self.driver = webdriver.Chrome(executable_path = CHROME_DRIVER_PATH)
        # Link de autenticación de tic-uis
        self.__autentication_link = 'https://tic.uis.edu.co/ava/login/index_ingreso.php'
        # Texto para recalificar una pregunta
        self.__RESCORE_STRING = "Escribir comentario o corregir la calificación"

        # Link que lleva a los cuestionarios, falta el id del curso al final del link
        self.__QUESTION_LINK = "https://tic.uis.edu.co/ava/mod/quiz/index.php?id="

        # Errores
        self.__LOGS = ["\n [-1] Fallo Al hacer autenticación| EXCEPTION: ",
                        "\n [1] Curso a modificar: ",
                        "\n [-2] Error al encontrar CPS al Cuestionario| Exception: ",
                        "\n [2] Se va a modificar: ",
                        "\n [3] Pregunta modificada satisfactoriamente ",
                        "\n [-3] Fallo al recalificar pregunta| EXCEPTION: ",
                        "\n [4] Curso terminado satisfactoriamente",
                        "\n [-4] Error al procesar curso: "]


    def autenticacion_tic(self, nickName, password):
        try:
            # Tiempo de dejar cargar chrome
            time.sleep(1)
            # Carga la página inicial de tic-uis
            self.driver.get(self.__autentication_link)
            self.driver.maximize_window() 
            # Tiempo para dejar que cargue la página
            time.sleep(3)

            # da click en pregrado
            pregrado = self.driver.find_element_by_id('pregrado-head')
            pregrado.click()

            # Encuentra usuario y contraseña
            userName = self.driver.find_element_by_name('username')
            passWord = self.driver.find_element_by_name('password')
            
            # Escribe las credenciales
            userName.send_keys(nickName)
            passWord.send_keys(password)

            # Encuentra botón para enviar información
            login_attempt = self.driver.find_element_by_xpath("//*[@id='send']")
            login_attempt.submit()
            
            # Si hay un fallo en la autenticación se muestra como un errorcode en el link
            if('?' in self.driver.current_url and "errorcode" in self.driver.current_url.split("?")[1]):
                raise Exception("Error usuario o contraseña")

        except Exception as e:
            self.log = self.__LOGS[0]+ str(e)

    def recorrer_cursos(self,links_cursos,CPS,question_id, enunciados,resultados, tipo_recalificacion):

        for link_curse in links_cursos: # Para cada curso de los que se proporcionaron
            id = link_curse.split('=')[1] #Obtenemos el id del curso
            link_question = self.__QUESTION_LINK+id # links a los cuestionarios de ese curso

            try:
                self.log += self.__LOGS[1] + id # Registramos curso a modificar
                self.driver.get(link_question) # se dirige a ese link

                try:
                    # Se busca el CPS a calificar
                    cps = self.driver.find_element_by_partial_link_text(CPS)
                    cps.location_once_scrolled_into_view
                    cps.click() 

                except Exception as e:
                    # En caso de no ser encontrado se captura la excepción y  se registra en el log
                    self.log +=self.__LOGS[2]+ str(e)
                
                # Entramos a los resultados del cuestionario
                self.driver.find_element_by_partial_link_text("Resultados").click()

                if(tipo_recalificacion == 1): # En caso de recalificar todo

                    self.driver.find_element_by_xpath("//input[@value='Recalificar todo']").click()
                    self.driver.find_element_by_xpath("//input[@value = 'Continuar']").click()

                elif(tipo_recalificacion == 2): # En caso de recalificar emparejamiento
                    # Preparación para llegar a las preguntas
                    
                    table = self.driver.find_element_by_id("attempts")
                    main_window = self.driver.current_window_handle

                    #Recorremos las preguntas en caso de que sean de emparejamiento
                    self.recorrer_preguntas(table, main_window, question_id,enunciados,resultados)

                #Si no ha saltado alguna excepción, se guarda que fue un curso exitoso
                self.log+=self.__LOGS[6]

            except Exception as e:
                # Si ocurre un error se guarda el fallo
                self.log+=self.__LOGS[7]+id +"| EXCEPTION: "+ str(e)

    def recorrer_preguntas(self, table, main_window, question_id,enunciados,resultados):
        # Buscamos todas las preguntas que han sido respondidas por estudiantes
        questions = table.find_elements_by_xpath(".//*[@title = 'Revisar respuesta']")

        # Se va a revisar cada pregunta
        for question in questions:
            question.click()

            # Cambiamos a la nueva ventana que es la preunta
            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[-1])
            quest_window = self.driver.current_window_handle

            # Verifica que la pregunta sea la que se va a modificar
            if(question_id in self.driver.title):
                # La cambia
                self.cambiar_calificacion_emparejamiento(quest_window,enunciados,resultados)
                
            # Si es o no es la pregunta solicitada, cierra y vuelve a la ventana original
            self.driver.close()
            self.driver.switch_to.window(main_window)

    def cambiar_calificacion_emparejamiento(self, quest_window,enunciados,resultados):
        try:
            # Se guarda a quíen se le va a modificar
            self.log += self.__LOGS[3] + self.driver.title

            # Cambiamos a la pestaña de edición
            recal = self.driver.find_element_by_link_text(self.__RESCORE_STRING)
            recal.location_once_scrolled_into_view
            recal.click()
            self.driver.switch_to.window(self.driver.window_handles[-1])


            #Calculamos la nota que merece el estudiante 
            nota = self.calcular_nota_emparejamiento(enunciados,resultados)
            # Modificar emparejamiento

            # Encontramos donde se va a modificar la nota y se le envía la nota asignada
            input_score = self.driver.find_element_by_xpath(".//div[@class = 'felement ftext']//input[@type = 'text']")
            input_score.location_once_scrolled_into_view
            input_score.clear()
            input_score.send_keys(str(nota))

            # Se envía y la ventana cierra sola
            guardar = self.driver.find_element_by_xpath("//input[@id = 'id_submitbutton']")
            guardar.location_once_scrolled_into_view
            guardar.click()

            # guarda que modificó correctamente la pregunta y vuelve a la pestaña la pregunta
            self.log += self.__LOGS[4]
            self.driver.switch_to.window(quest_window)
        except Exception as e:
            print(e)
            # Si hay algún error guarda el fallo
            self.log +=self.__LOGS[5] + str(e)
        
    def calcular_nota_emparejamiento(self,enunciados,resultados):
        diccionario = dict(zip(enunciados,resultados))
        # Obtenemos el puntaje total de la pregunta
        max_punt = float(self.driver.find_element_by_xpath("//div[@class = 'grade']").text.split(" sobre ")[1].replace(',','.'))
        # Obtenemos los enunciados
        enunciados_html = self.driver.find_elements_by_xpath("//table[@class = 'answer']//tr//td[@class = 'text']")
        # Obtenemos las respuestas del estudiante
        respuestas_html = self.driver.find_elements_by_xpath("//table[@class = 'answer']//tr//td//option[@selected='selected']")

        num_enun = len(enunciados_html) # Número de enunciados que hay que responder.
        puntaje_por_pregunta = max_punt/num_enun # Se calcula cuanto vale cada respuesta

        contador_respuestas_bien = 0

        # Para cada enunciado de la pregunta
        for index in range(num_enun):
            
            # Comparamos la respuesta del estudiante con la que debería ser
            enun = enunciados_html[index].text
            respuesta_dada = respuestas_html[index].text
            respuesta_correcta = diccionario.get(enun)

            if(respuesta_dada == respuesta_correcta): 
                # En tal caso se aumenta el numero de respuestas bien
                contador_respuestas_bien +=1

        # Se calcula la nota que merece el estudiante
        nota = puntaje_por_pregunta*contador_respuestas_bien
        return nota



        
    def cerrar(self):
        self.driver.quit()
