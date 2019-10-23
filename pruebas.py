from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import robot
import time

NICKNAME = "exper-tic"
PASSWORD = "exper-tic"

CELLS = ["mod-quiz-report-overview-report_r0_c10",
"mod-quiz-report-overview-report_r0_c11",
"mod-quiz-report-overview-report_r0_c12",
"mod-quiz-report-overview-report_r0_c13"]

QUESTION_TITLE = 'T02.01.01_B002_N0'

CURSES_LINK = "https://tic.uis.edu.co/ava/course/index.php?categoryid=926"

CHROME_DRIVER_PATH = "/home/david-norato/Documentos/EXPERTIC/QuimicaRobot/chromedriver_linux64/chromedriver"

camino_cpl = "Módulo 1/CPS1.4/Intentos: "

links_cursos = ["https://tic.uis.edu.co/ava/course/view.php?id=12123",
                "https://tic.uis.edu.co/ava/course/view.php?id=12124",
                "https://tic.uis.edu.co/ava/course/view.php?id=12095",
                "https://tic.uis.edu.co/ava/course/view.php?id=12094",
                "https://tic.uis.edu.co/ava/course/view.php?id=12093",
                "https://tic.uis.edu.co/ava/course/view.php?id=12092",
                "https://tic.uis.edu.co/ava/course/view.php?id=12091",
                "https://tic.uis.edu.co/ava/course/view.php?id=12090",
                "https://tic.uis.edu.co/ava/course/view.php?id=12089",
                "https://tic.uis.edu.co/ava/course/view.php?id=12088",
                "https://tic.uis.edu.co/ava/course/view.php?id=12087",
                "https://tic.uis.edu.co/ava/course/view.php?id=12086",
                "https://tic.uis.edu.co/ava/course/view.php?id=11605",
                "https://tic.uis.edu.co/ava/course/view.php?id=11593",
                "https://tic.uis.edu.co/ava/course/view.php?id=11586",
                "https://tic.uis.edu.co/ava/course/view.php?id=11599",
                "https://tic.uis.edu.co/ava/course/view.php?id=11598"]

#wb = webdriver.Chrome(executable_path = CHROME_DRIVER_PATH)
wb = robot.get_nuevo_driver_chrome(CHROME_DRIVER_PATH)

robot.autenticacion_tic(wb,NICKNAME,PASSWORD)
robot.recalificar_pregunta(wb,links_cursos,camino_cpl, CELLS,QUESTION_TITLE)


