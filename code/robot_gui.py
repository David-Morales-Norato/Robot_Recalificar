import tkinter as tk
import tkinter.filedialog
from Robot import Robot
from read_files import leer_datos
import os
import sys

class robot_gui():
    def __init__(self):
        #Inicializaciones

        # Errores que pueden salir 
        self.LOGS = ["\n No ha sido posible cargar el archivo: ",
                     "\n Ingrese usuario y contraseña antes de correr el robot",
                     "\n Cargue el archivo primero antes de correr el robot",
                     "\n Error de autenticación ",
                     "\n Elija una opción de recalificación"]
        self.log = ''

        # Variable de contrlo, para verificar cuando hayan cargado un archivo existente
        self.archivo_cargado = False

        # NECESARIO HACEN UN MÉTODO CON TODOS LOS DRIVERS PARA CADA PLATAFORMA
        #Es necesaria una verificación 
        self.DRIVER_PATH = self.get_path_driver()
        #Es necesaria una 
        

        self.file_path = ''


        #Ventana principal.
        self.root = tk.Tk()
        self.root.title("Robot para recalificar preguntas")
        m = self.root.maxsize()
        self.root.geometry('{}x{}+0+0'.format(*m))

        #Frame donde van a estar ubicados las entradas de usuario y contraseña.
        frame_left = tk.Frame(self.root, pady = 100, padx = 100)
        frame_left.pack(side = "left")

        #Botón para cargar los datos del csv
        button_cargar_datos = tk.Button(frame_left, text = "Cargar datos.",comman = lambda:self.open_file()) 
        button_cargar_datos.grid(row = 0, column = 1) 

        #Labels para describir
        tk.Label(frame_left, text="Nombre de usuario: ").grid(row=1,column=0) 
        tk.Label(frame_left, text="Contraseña: ").grid(row=2,column=0)

        #Campo de texto que guarda el input de el usuario.
        self.input_user_entry = tk.Entry(frame_left) 
        self.input_user_entry.grid(row = 1, column =1, pady = 20)

        #Campo de texto que guarda el input de la contraseña.
        self.input_pass_entry = tk.Entry(frame_left) 
        self.input_pass_entry.grid(row = 2, column = 1, pady = 20)

        #Label para describir que es importante
        tk.Label(frame_left, text="*", fg='red').grid(row=0,column=2)
        tk.Label(frame_left, text="*", fg='red').grid(row=1,column=2) 
        tk.Label(frame_left, text="*", fg='red').grid(row=2,column=2)

        #Botón para correr el robot
        button_run_robot = tk.Button(frame_left, text = "Correr robot.",comman = lambda:self.pre_run()) 
        button_run_robot.grid(row = 3, column = 1) 

        # Variable de control de la opción del tipo de recalificación que se va a usar
        self.opcion = tk.IntVar()
        self.opcion.set(0) # Se setea en 0, el caso en que no ha escogido ninguna opción

        # recalificar todo valor 1
        # recalificar emparejamiento valor 2
        # Botones que son las opciones
        tk.Radiobutton(frame_left, text="recalificar todo",padx = 20, variable=self.opcion, value=1).grid(row=1,column=3)
        tk.Radiobutton(frame_left, text="recalificar emparejamiento",padx = 20, variable=self.opcion, value=2).grid(row=2,column=3)

        #Frame derecho
        frame_right = tk.Frame(self.root)
        frame_right.pack(side = "right")

        #Label donde se van a imprimir las estadísticas
        self.label_logs_result = tk.Label(frame_right, text="", padx = 20, pady = 40)  # Label para escribir mensajes
        self.label_logs_result.grid(row = 0, column = 0)

        # Botón que imprime estadísticas del proceso realizado.
        # Se activa una vez que se haya terminado de ejecutar el robot
        self.button_log = tk.Button(frame_right, text = "Revisar estadisticas",state="disabled",comman = lambda:self.imprimir_estadisticas()) 
        self.button_log.grid(row = 2, column = 0) 

        self.root.mainloop()

    def get_path_driver(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/chromedriver/chromedriver"


    def pre_run(self):
            log = ''

            # Si no se ha escogido ninguna opción
            if(self.opcion.get() <1):
                log += self.LOGS[4]

            # Si No ha ingresado nada como usuario o contraseña
            if(len(self.input_user_entry.get()) == 0 or len(self.input_pass_entry.get()) == 0):
                log += self.LOGS[1]
                
            # Si no ha cargado ningún archivo
            if(not self.archivo_cargado):
                log += self.LOGS[2]
                
            # Imprime los errores en el label de la GUI
            self.label_logs_result.config(text = log)

            # Si ha salido algún error no ejecuta el robot
            if(len(log)>1): 
                return

            else:
                # Lemos los datos del archivo CSV
                datos = leer_datos(self.file_path, self.opcion.get())
                if(len(datos[-1])<1): # Si no hay algún error al leer los datos
                    self.run_robot(datos[0],datos[1][0],datos[2][0],datos[3],datos[4])
                else:
                    # Si hay por lo menos un error lo imprime en el label de la GUI
                    self.log += datos[-1]
                    self.label_logs_result.config(text = datos[-1])



    def run_robot(self,links_cursos,CPL,QUESTION_ID,enunciados,resultados):
        try:
            # intenta cargar el driver del navegador
            self.robot = Robot(self.DRIVER_PATH)
            
        except Exception as e: # Si hay algún problema cancela correr el robot e imprime un error
            self.log += "\n" + str(e)
            self.label_logs_result.config(text = "Problema al cargar el driver de Google")
            return

        # Autenticación en tic-uis
        self.robot.autenticacion_tic(self.input_user_entry.get(),self.input_pass_entry.get())
        log = self.robot.log

        # Si ha existido algún error en la autenticación
        # cierra el robot y el navegador, e imprime el error
        if(len(log)>1):
            self.cerrar_driver()
            self.log += log
            self.label_logs_result.config(text = log)
            return

        # Corre el robot
        self.robot.recorrer_cursos(links_cursos,CPL,QUESTION_ID,enunciados,resultados)

        # Activa el botón para ver las estadísticas
        self.button_log.config(state="normal")
        self.label_logs_result.config(text = "Terminado!")

        # Cierra el robot y el navegador
        self.cerrar_driver()

    def open_file(self):
        # Obtiene el path del archivo selexionado por el usuario
        file_path = tk.filedialog.askopenfilename(filetypes =(("Archivo CSV", "*.csv"),("Todos los archivos","*.*")),
                           title = "Escoge el archivo .csv")
        try:
            #Intenta abrirlo
            # Si existe puede procegir a otras verificaciones
            with open(file_path,'r'):
                self.file_path = file_path
                self.archivo_cargado = True

        # Si no existe el archivo crea error
        except:
            self.archivo_cargado = False
            self.log += self.LOGS[0] + str(self.file_path)
            self.label_logs_result.config(text = self.LOGS[0])


    def imprimir_estadisticas(self):
        # Imprime las estadísticas en el label de la GUI
        self.label_logs_result.config(text = self.robot.revisar_log())

    def cerrar_driver(self):
        #Cierra el driver
        self.robot.cerrar()


        


