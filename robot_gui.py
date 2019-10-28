import tkinter as tk
import tkinter.filedialog
from Robot import Robot
from read_files import leer_datos
import os
import sys

class robot_gui():
    def __init__(self,CHROME_DRIVER_PATH):
        #Inicializaciones
        self.LOGS = [" No ha sido posible cargar el archivo: ",
                     " Ingrese usuario y contraseña antes de correr el robot",
                     " Cargue el archivo primero antes de correr el robot",
                     " Error de autenticación "]
        self.log = ''
        self.archivo_cargado = False
        self.links_cursos = ""
        #Es necesaria una verificación 
        self.DRIVER_PATH = CHROME_DRIVER_PATH
        #Es necesaria una verificación

        self.file_path = ''


        #Ventana principal.
        self.root = tk.Tk()
        self.root.title("Robot para recalificar preguntas")
        self.root.resizable(False, False)

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

        #Frame derecho
        frame_right = tk.Frame(self.root)
        frame_right.pack(side = "right")

        #Label donde se van a imprimir los logs
        self.label_logs_result = tk.Label(frame_right, text="", padx = 20, pady = 40)  # Label para escribir mensajes
        self.label_logs_result.grid(row = 0, column = 0)


        self.root.mainloop()
    def pre_run(self):
            log = ''
            if(len(self.input_user_entry.get()) == 0 or len(self.input_pass_entry.get()) == 0):
                log += self.LOGS[1]
                
            if(not self.archivo_cargado):
                log += '\n'+ self.LOGS[2]
                
            self.label_logs_result.config(text = log)
            if(len(log)>1): return
            if(self.archivo_cargado):
                datos = leer_datos(self.file_path)
                if(len(datos[4])<1):
                    self.run_robot(datos[0],datos[1][0],datos[2][0],datos[3][0])
                else:
                    self.log += datos[4]

    def run_robot(self,links_cursos,CPL,QUESTION_ID,CALIFICACION):
        self.robot = Robot(self.DRIVER_PATH)

        self.robot.autenticacion_tic(self.input_user_entry.get(),self.input_pass_entry.get())
        log = self.robot.log
        print(log)
        if(len(log)>1):
            self.robot.cerrar()
            self.log += log
            self.label_logs_result.config(text = self.LOGS[0])
        self.robot.recalificar_pregunta(links_cursos,CPL,QUESTION_ID,CALIFICACION)

    def open_file(self):
        file_path = tk.filedialog.askopenfilename(filetypes =(("Archivo CSV", "*.csv"),("Todos los archivos","*.*")),
                           title = "Escoge el archivo .csv")
        try:
            with open(file_path,'r'):
                self.file_path = file_path
                self.archivo_cargado = True
        except:
            self.archivo_cargado = False
            self.log += self.LOGS[0] + str(self.file_path)
            self.label_logs_result.config(text = self.LOGS[0])
        


