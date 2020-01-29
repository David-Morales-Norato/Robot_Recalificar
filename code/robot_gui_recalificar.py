from robot_gui import robot_gui, tk
from robot_recalificar import robot_recalificar
from leer_recalificar import leer_datos_recalificar
DEBUG = True
class recalificar_gui(robot_gui):
    def __init__(self):
        super().__init__()
        self.root.title("Robot para recalificar preguntas")
        # Variable de control de la opción del tipo de recalificación que se va a usar
        self.opcion = tk.IntVar()
        self.opcion.set(0) # Se setea en 0, el caso en que no ha escogido ninguna opción
        # recalificar todo valor 1
        # recalificar emparejamiento valor 2
        # Botones que son las opciones
        tk.Radiobutton(self.frame_left, text="recalificar todo",padx = 20, variable=self.opcion, value=1).grid(row=1,column=3)
        tk.Radiobutton(self.frame_left, text="recalificar emparejamiento",padx = 20, variable=self.opcion, value=2).grid(row=2,column=3)

        if(DEBUG):
            self.file_path = "/home/david-norato/Documentos/EXPERTIC/recalificar_actividades/datos/datos_recalificar_todo.xlsx"
            self.input_user_entry.insert(0,"exper-tic")
            self.input_pass_entry.insert(0,"exper-tic")
            self.archivo_cargado = True
            self.opcion.set(1)
        self.root.mainloop()


    def pre_run_especifico(self):
        # Lemos los datos del archivo xlsx
        leer_datos = leer_datos_recalificar()
        datos = leer_datos.lectura_especifica(self.file_path, self.opcion.get())
        if(len(leer_datos.get_log())<1): # Si no hay algún error al leer los datos
            # Se pasan los datos y la opción de la tarea del robot
            self.run_robot(datos,self.opcion.get())
        else:
            # Si hay por lo menos un error lo imprime en el label de la GUI
            self.log += leer_datos.get_log()
            self.label_logs_result.config(text = leer_datos.get_log())

    def get_robot(self,driver_path):
        return robot_recalificar(driver_path)

    def run_robot_especifico(self,datos, tipo_tarea):

        # Si la tarea es 1 o 2 es que se desea recorrer los cursos en los cursos

        # 1 es recalificar todo
        # 2 es recalificar emparejamiento
        tipo_recalificacion = tipo_tarea
        # Corre el robot y recorre cursos para recalificar 
        self.robot.recorrer_cursos(datos, tipo_recalificacion)


    def revisar_log(self):

        log = self.robot.log
        salida = ''


        cursos_procesados = log.count("[1]")
        cursos_exitosos = log.count("[4]")
        fallos_camino = log.count("[-2]")
        cursos_fallidos = log.count("[-4]")
        salida += "Total cursos procesados: "+ str(cursos_procesados) + '\n'
        salida += "Total cursos recorridos exitosamente: "+ str(cursos_exitosos) + '\n'
        salida += "Total cursos recorridos incorrectamente: "+ str(cursos_fallidos) + '\n'
        salida += "Total cursos con fallo en el camino a resultados: "+ str(fallos_camino) + '\n'

        if(self.opcion.get() == 2):
            
            preguntas_procesadas = log.count("[2]")
            preguntas_exitosas = log.count("[3]")
            preguntas_fallidas = log.count("[-3]")
            salida += "Total preguntas procesadas: "+ str(preguntas_procesadas) + '\n'
            salida += "Total preguntas fallidas a procesar: "+ str(preguntas_fallidas) + '\n'
            salida += "Total preguntas modificadas correctamente: "+ str(preguntas_exitosas) + '\n'
        return salida
