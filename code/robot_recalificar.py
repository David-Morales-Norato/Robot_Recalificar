from Robot import Robot, time
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
            primera_hoja = np.array(datos[1])
            segunda_hoja = datos[2]

            # Se separan los datos
            fila = primera_hoja[:,contador]
            # Adquirimos la actividar a recalificar
            ACTIVIDAD = fila[1] 
            # Si la elección es 1 o 2 los datos vienen empaquetados de fomra similar

        if(eleccion ==2):
            QUESTION_ID = fila[2] # Adquirimos el id de la pregunta a  recalificar
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


            # Para sacar estadísticas.
            # Preparación para llegar a la tabla
            table = self.driver.find_element_by_id("attempts")
            main_window = self.driver.current_window_handle

            self.recorrer_intentos_recalificados(table,fila)


        elif(eleccion == 2): # En caso de recalificar emparejamiento
            # Preparación para llegar a las preguntas
            table = self.driver.find_element_by_id("attempts")
            main_window = self.driver.current_window_handle

            #Recorremos las preguntas en caso de que sean de emparejamiento
            self.recorrer_preguntas(table, main_window, QUESTION_ID,enunciados,resultados, fila)
            
        #Si no ha saltado alguna excepción, se guarda que fue un curso exitoso
        self.log+=self._LOGS[4]

    def recorrer_intentos_recalificados(self, table, fila):
        # Buscamos todos los intentos
        intentos = self.driver.find_elements_by_xpath(".//td//a[@title = 'Revisión del intento']")
        contador_recalificaciones = 0
        # Se va a revisar cada intento si ha sido recalificado
        

        # Contador para saber la fila de la tabla y encontrar los datos a extraer
        cont = 0

        # Nombres de los estudiantes que intentaron realizar la actividad
        nombres = self.driver.find_elements_by_xpath(".//td[@class = 'cell c2 bold']//a")[0::2]
        # Ya que retorna 2 textos por cada casilla obtenemos solo el nombre del estudiante

        for intento in intentos:
            
            # Si hay dos notas separadas por un '/'
            # Significa que hay una recalificación
            notas_intento = intento.text.replace("\n","").replace(',','.').split("/")
            if(len(notas_intento)>1):
                contador_recalificaciones += 1
                nota_anterior = notas_intento[0]
                nota_posterior = notas_intento[1]
                nombre = nombres[cont].text
                cont +=1
                self.datos_recopilados.append([fila[0], fila[1], nombre, nota_anterior, nota_posterior ])
                #actividad, id_curso, nombre_estudiante, nota_anterior, nota_posterior
            
            

    def recorrer_preguntas(self, table, main_window, question_id,enunciados,resultados, fila):
        # Buscamos todas las preguntas que han sido respondidas por estudiantes
        questions = table.find_elements_by_xpath(".//*[@title = 'Revisar respuesta']")
        cont = 0
        nombres = self.driver.find_elements_by_xpath(".//td[@class = 'cell c2 bold']//a")[0::2]

        # Se va a revisar cada pregunta
        for question in questions:
            nombre = nombres[cont].text
            question.click()

            # Cambiamos a la nueva ventana que es la preunta
            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[-1])
            quest_window = self.driver.current_window_handle
            quest_id_title = str(self.driver.title.split(" ")[4]).replace(" ","")
            # Verifica que la pregunta sea la que se va a modificar
            if(str(question_id).replace(" ","") == quest_id_title):
                # La cambia
                
                datos_notas = self.cambiar_calificacion_emparejamiento(quest_window,enunciados,resultados)
                
                self.datos_recopilados.append([fila[0], fila[1], nombre, datos_notas[0], datos_notas[1] ])
            # Si es o no es la pregunta solicitada, cierra y vuelve a la ventana original
            self.driver.close()
            self.driver.switch_to.window(main_window)
            cont += 1

    def cambiar_calificacion_emparejamiento(self, quest_window,enunciados,resultados):
        datos_cambio = []
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
            nota_anterior = input_score.get_attribute("value")
            print(nota_anterior)
            input_score.clear()
            input_score.send_keys(str(nota))

            # Se envía y la ventana cierra sola
            guardar = self.driver.find_element_by_xpath("//input[@id = 'id_submitbutton']")
            guardar.location_once_scrolled_into_view
            guardar.click()

            time.sleep(3)
            # guarda que modificó correctamente la pregunta y vuelve a la pestaña la pregunta
            self.log += self._LOGS[6]
            self.driver.switch_to.window(quest_window)

            #nota anterior, y nueva nota
            datos_cambio = [nota_anterior, nota]
            return datos_cambio
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
            enun = eliminar_ultimo_espacio(enunciados_html[index].text)
            respuesta_dada = respuestas_html[index].text
            respuesta_correcta = diccionario.get(enun)
            if(respuesta_dada == respuesta_correcta): 
                # En tal caso se aumenta el numero de respuestas bien
                contador_respuestas_bien +=1

        # Se calcula la nota que merece el estudiante
        nota = puntaje_por_pregunta*contador_respuestas_bien
        return nota

def eliminar_ultimo_espacio(cadena):
    while(' ' == cadena[-1]):
        cadena = cadena[:-1]
    return cadena