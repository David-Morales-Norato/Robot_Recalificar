from robot import Robot
from read_files import leer_datos
CHROME_DRIVER_PATH = "/home/david-norato/Documentos/EXPERTIC/QuimicaRobot/chromedriver_linux64/chromedriver"
path = '/home/david-norato/Documentos/EXPERTIC/QuimicaRobot/datos.csv'
datos = leer_datos(path)

NICKNAME = datos[0][0]
PASSWORD = datos[1][0]
links_cursos = datos[2]
camino_cpl = datos[3]
QUESTION_ID = datos[4][0]
log = datos[5]
rob = Robot(CHROME_DRIVER_PATH)
rob.autenticacion_tic(NICKNAME,PASSWORD)
rob.recalificar_pregunta(links_cursos,camino_cpl,QUESTION_ID,"1")
print(rob.log)


