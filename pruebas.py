from robot import Robot

NICKNAME = "exper-tic"
PASSWORD = "exper-tic"

QUESTION_TITLE = 'T02.01.01_B002_N0'

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

rob = Robot(CHROME_DRIVER_PATH)

rob.autenticacion_tic(NICKNAME,PASSWORD)
rob.recalificar_pregunta(links_cursos,camino_cpl,QUESTION_TITLE,"1")


