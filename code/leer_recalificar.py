from read_files import leer_datos,pd

class leer_datos_recalificar(leer_datos):
    def __init__(self):
        self.NOMBRES_HOJAS = ["CURSOS_ACTIVIDADES", "PREGUNTAS_ENUNCIADOS"]
        super().__init__()

    def lectura_especifica(self,file_path, tipo_lectura):
        try:


            # Si desean hacer una recalificación completa
            if(tipo_lectura == 1):
                # Se lee el archivo xlsx
                archivo_excel = pd.read_excel(file_path)
                datos = self.lectura_cursos_actividad(archivo_excel)

            # Si desean hacer una recalificación para una pregunta de emparejamiento
            elif(tipo_lectura == 2):
                # Se lee el archivo xlsx 
                archivo_excel = pd.read_excel(file_path, sheet_name=None)
                datos = self.lectura_tipo_recalificar_emparejamiento(archivo_excel)

            else: 
                datos = None
            return datos
        except Exception as e:
            self.log += str(e)
            return None

    def lectura_tipo_recalificar_emparejamiento(self, archivo_excel):
        # Leemos las hojas
        cursos_actividades = archivo_excel[self.NOMBRES_HOJAS[0]]
        enunciados_preguntas = archivo_excel[self.NOMBRES_HOJAS[1]]

        # Leemos cursos y actividades
        [cursos,actividad] = self.lectura_cursos_actividad(cursos_actividades)

        # Leemos el id de la pregunta a recalificar
        id_pregunta = self.leer_columna(cursos_actividades,"ID_PREGUNTA")
        

        # Leemos los enunciados de la pregunta en la segunda hoja
        enunciados = self.leer_columna(enunciados_preguntas,"ENUNCIADOS")

        # Leemos las respuestas de la pregunta
        respuestas = self.leer_columna(enunciados_preguntas,"RESPUESTAS")

        primera_hoja = [cursos,actividad,id_pregunta]
        segunda_hoja = [enunciados,respuestas]
        return [cursos,primera_hoja,segunda_hoja]

    def get_log(self):
        return self.log