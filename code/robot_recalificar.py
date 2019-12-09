from Robot import Robot
import numpy as np
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

class robot_recalificar(Robot):
    def __init__(self, DRIVER_PATH):
        super().__init__(DRIVER_PATH)

        logs_recalificacion_preguntas = [ "\n [3] Pregunta modificada satisfactoriamente ",
                 "\n [-3] Fallo al recalificar pregunta| EXCEPTION: "]
        self._LOGS = self._LOGS + logs_recalificacion_preguntas
        # Texto para recalificar una pregunta
        self.__RESCORE_STRING = "Escribir comentario o corregir la calificación"

    def tratamiento_curso(self,datos, variables_de_control):

        # Eleccion es el primer elemento
        eleccion = variables_de_control[0]
        # Contador el segundo elemento
        contador = variables_de_control[1]
        
        # Escogió recalificar todo
        if(eleccion == 1):
            primera_hoja = np.array(datos)
            # Se separan los datos
            fila = primera_hoja[:,contador]
            # Adquirimos la actividar a recalificar
            ACTIVIDAD = fila[1] 
            # Si la elección es 1 o 2 los datos vienen empaquetados de fomra similar

        else: # Recalificar pregunta de emparejamiento
            # Obtenemos las dos primeras hojas
            primera_hoja = np.array(datos[1][1:])
            segunda_hoja = datos[2]

            # Se separan los datos
            fila = primera_hoja[:,contador]
            # Adquirimos la actividar a recalificar
            ACTIVIDAD = fila[0] 
            # Si la elección es 1 o 2 los datos vienen empaquetados de fomra similar

        if(eleccion ==2):
            QUESTION_ID = fila[1] # Adquirimos el id de la pregunta a  recalificar
            enunciados = segunda_hoja[0] # Adquirimos los enunciados
            resultados = segunda_hoja[1] # Adquirimos las respuestas
        else: 
            QUESTION_ID = None
            enunciados = None
            resultados = None
        try:
            # Se busca el CPS a calificar
            actividad = self.driver.find_element_by_partial_link_text(ACTIVIDAD)
            actividad.location_once_scrolled_into_view
            actividad.click() 

        except Exception as e:
            # En caso de no ser encontrado se captura la excepción y  se registra en el log
            self.log +=self._LOGS[2]+ str(e)
        
        # Entramos a los resultados del cuestionario
        self.driver.find_element_by_partial_link_text("Resultados").click()
        if(eleccion == 1): # En caso de recalificar todo

            self.driver.find_element_by_xpath("//input[@value='Recalificar todo']").click()
            self.driver.find_element_by_xpath("//input[@value = 'Continuar']").click()

        elif(eleccion == 2): # En caso de recalificar emparejamiento
            # Preparación para llegar a las preguntas
            table = self.driver.find_element_by_id("attempts")
            main_window = self.driver.current_window_handle

            #Recorremos las preguntas en caso de que sean de emparejamiento
            self.recorrer_preguntas(table, main_window, QUESTION_ID,enunciados,resultados)

        #Si no ha saltado alguna excepción, se guarda que fue un curso exitoso
        self.log+=self._LOGS[4]

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
            self.log += self._LOGS[3] + self.driver.title

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
#            input_score.clear()
#            input_score.send_keys(str(nota))

            # Se envía y la ventana cierra sola
            guardar = self.driver.find_element_by_xpath("//input[@id = 'id_submitbutton']")
            guardar.location_once_scrolled_into_view
            guardar.click()

            # guarda que modificó correctamente la pregunta y vuelve a la pestaña la pregunta
            self.log += self._LOGS[6]
            self.driver.switch_to.window(quest_window)
        except Exception as e:
            # Si hay algún error guarda el fallo
            self.log +=self._LOGS[7] + str(e)
        
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

