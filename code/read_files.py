import pandas as pd

def leer_datos(file_path, tipo_lectura):
    log = ''
    try:
        # Lee el archivo csv por su ubicación
        data = pd.read_csv(file_path)

        # Si desean hacer una recalificación completa
        if(tipo_lectura == 1):
            datos = lectura_recalificar_todo(data)

        # Si desean hacer una recalificación para una pregunta de emparejamiento
        elif(tipo_lectura == 2):
            datos = lectura_tipo_recalificar_emparejamiento(data)

        else: 
            datos = None
        return datos
    except Exception as e:
        log += str(e)
        return None
    


def lectura_tipo_cambiar_fechas(data):
    # Coming soon
    pass


def lectura_tipo_recalificar_emparejamiento(data):
    datos_previos = lectura_recalificar_todo(data)
    log = datos_previos[-1]
    cursos = datos_previos[0]
    CPS = datos_previos[1]

    try:
        # Intenta encontrar la columna 
 
        id_pregunta = data["Id pregunta"].dropna().tolist()

        if(len(id_pregunta) != 1):# Si no encuentra bota error o encuentra más de una
            raise Exception("Id pregunta filas")
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        id_pregunta = None
    
    try:# Intenta encontrar la columna
        enunciados = data["Enunciados"].dropna().tolist()

        if(len(enunciados) == 0):# Si no encuentra bota error
            raise Exception("Fallo al leer los Enunciados")
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        enunciados = None

    try:
        # Intenta encontrar la columna
        respuestas = data["Respuestas"].dropna().tolist()

        if(len(respuestas) == 0):# Si no encuentra bota error
            raise Exception("Fallo al leer los respuestas")
        else:
            pass

    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        respuestas = None

    return [cursos, CPS, id_pregunta,enunciados,respuestas,log]


def lectura_recalificar_todo(data):
    log = ''
    try:
        # Intenta encontrar la columna
        cursos = data["Cursos"].dropna().tolist()

        if(len(cursos)==0): # Si no encuentra bota error
            raise Exception("Fallo, no hay cursos que recorrer")    
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        cursos = None

    try:
        # Intenta encontrar la columna 
        CPS = data["CPS"].dropna().tolist()
        if(len(CPS) == 0):# Si no encuentra bota error
            raise Exception("Cuidado, no hay CPS que recalificar")
        else:
            pass
    except Exception as e:
        log += "Fallo al leer columna: " + str(e) + "\n"
        CPS = None

    return [cursos,CPS, log]