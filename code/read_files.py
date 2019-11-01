import pandas as pd

def leer_datos(file_name):
    log = ''
    try:
        data = pd.read_csv(file_name)
        try:
            cursos = data["Cursos"].dropna().tolist()
            if(len(cursos)==0):
                raise Exception("Fallo, no hay cursos que recorrer")    
            else:
                pass
        except Exception as e:
            log += "Fallo al leer columna: " + str(e) + "\n"
            cursos = None

        try:
            camino = data["Camino"].dropna().tolist()
            if(len(camino) == 0):
                raise Exception("Cuidado, no hay camino que recorrer")
            else:
                pass
        except Exception as e:
            log += "Fallo al leer columna: " + str(e) + "\n"
            camino = None

        try: 
            id_pregunta = data["Id pregunta"].dropna().tolist()
            if(len(id_pregunta) != 1):
                raise Exception("Id pregunta filas")
            else:
                pass
        except Exception as e:
            log += "Fallo al leer columna: " + str(e) + "\n"
            id_pregunta = None
        
        try:
            calificacion = data["Calificacion"].dropna().tolist()
            if(len(calificacion) != 1):
                raise Exception("Fallo al leer la Calificación")
            else:
                pass
        except Exception as e:
            log += "Fallo al leer columna: " + str(e) + "\n"
            calificacion = None
    except Exception as e:
        log += str(e)

    return [cursos, camino, id_pregunta, calificacion,log]

