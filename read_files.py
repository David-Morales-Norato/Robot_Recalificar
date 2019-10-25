import pandas as pd

def leer_datos(file_name):
    log = ''
    try:
        data = pd.read_csv(file_name)
        try:
            usuario = data["Usuario"].dropna().tolist()
            if(len(usuario) != 1):
                raise Exception("Fallo al leer el usuario")
            else:
                pass
        except Exception as e:
            log += str(e)
            usuario = None

        try:
            password = data["Contraseña"].dropna().tolist()
            if(len(password) != 1):
                raise Exception("Fallo al leer la Contraseña")
            else:
                pass
        except Exception as e:
            log += str(e)
            password = None

        try:
            cursos = data["Cursos"].dropna().tolist()
            if(len(cursos)==0):
                raise Exception("Fallo, no hay cursos que recorrer")    
            else:
                pass
        except Exception as e:
            log += str(e)
            cursos = None
        
        try:
            camino = data["Camino"].dropna().tolist()
            if(len(camino) == 0):
                raise Exception("Cuidado, no hay camino que recorrer")
            else:
                pass
        except Exception as e:
            log += str(e)
            camino = None

        try: 
            id_pregunta = data["Id pregunta"].dropna().tolist()
            if(len(id_pregunta) != 1):
                raise Exception("Fallo al leer Id pregunta")
            else:
                pass
        except Exception as e:
            log += str(e)
            id_pregunta = None
    except Exception as e:
        log += str(e)

    return [usuario, password, cursos, camino, id_pregunta, log]

