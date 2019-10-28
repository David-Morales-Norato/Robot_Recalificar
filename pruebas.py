from Robot import Robot
from read_files import leer_datos
from robot_gui import robot_gui
CHROME_DRIVER_PATH = "/home/david-norato/Documentos/EXPERTIC/QuimicaRobot/chromedriver_linux64/chromedriver"
# NICKNAME = datos[0][0]
# PASSWORD = datos[1][0]
robot_gui(CHROME_DRIVER_PATH)
# rob = Robot(CHROME_DRIVER_PATH)
# rob.autenticacion_tic(NICKNAME,PASSWORD)
# rob.recalificar_pregunta(links_cursos,CPS,QUESTION_ID,"1")


