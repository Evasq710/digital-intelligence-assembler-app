from xml.etree import ElementTree as ET
from tkinter import *
from tkinter import filedialog
from clases import *
import traceback, os

lista_global_maquinas = Lista_Maquinas()
lista_global_simulaciones = Lista_Simulaciones()

class Interfaz:
    def __init__(self, ventana):
        self.window = ventana
        self.window.title('Digital Intelligence Assembler')        
        self.window.state('zoomed')
        
        imagen = PhotoImage(file = "images/fondo.png")
        fondo = Label(self.window, image = imagen, bg="black")
        fondo.photo = imagen
        fondo.place(x=0, y=0, relwidth=1, relheight=1)

        title = Label(self.window, text="Digital Intelligence Assembler", font=("Consolas", 50, "bold"), bg="white")
        title.place(x=200, y=70)

        self.frame4 = LabelFrame(self.window,bg="white", text="Reporte de cola de secuencia")
        self.frame4_no_file = Frame(self.frame4, bg="white")
        self.frame4_no_file.place(x=0, y=0, relheight=1, relwidth=1)
        load_img4 = PhotoImage(file="images/question2.png")
        load_lb4 = Label(self.frame4_no_file, image=load_img4, bg="white")
        load_lb4.photo = load_img4
        load_lb4.place(x=10, y=50, width=300, height=300)
        title1= Label(self.frame4_no_file, text="No se ha cargado ningún archivo al programa.", font=("Consolas", 20), bg="white")
        title1.place(x=320, y=200)

        self.frame3 = LabelFrame(self.window,bg="white", text="Ensamblar productos")
        self.frame3_no_file = Frame(self.frame3, bg="white")
        self.frame3_no_file.place(x=0, y=0, relheight=1, relwidth=1)
        load_img3 = PhotoImage(file="images/question1.png")
        load_lb3 = Label(self.frame3_no_file, image=load_img3, bg="white")
        load_lb3.photo = load_img3
        load_lb3.place(x=10, y=50, width=300, height=300)
        title1= Label(self.frame3_no_file, text="No se ha cargado ningún archivo al programa.", font=("Consolas", 20), bg="white")
        title1.place(x=320, y=200)

        self.frame2 = LabelFrame(self.window,bg="white", text="Cargar Archivo - Simulación")
        self.frame2_no_file = Frame(self.frame2, bg="white")
        self.frame2_no_file.place(x=0, y=0, relheight=1, relwidth=1)
        load_img2 = PhotoImage(file="images/load2.png")
        load_lb2 = Label(self.frame2_no_file, image=load_img2, bg="white")
        load_lb2.photo = load_img2
        load_lb2.place(x=10, y=50, width=300, height=300)
        title1= Label(self.frame2_no_file, text="No se ha cargado ningún archivo al programa.", font=("Consolas", 20), bg="white")
        title1.place(x=320, y=200)

        self.frame1 = LabelFrame(self.window,bg="white", text="Cagar Archivo - Máquina")
        self.frame1_no_file = Frame(self.frame1, bg="white")
        self.frame1_no_file.place(x=0, y=0, relheight=1, relwidth=1)
        load_img1 = PhotoImage(file="images/load1.png")
        load_lb = Label(self.frame1_no_file, image=load_img1, bg="white")
        load_lb.photo = load_img1
        load_lb.place(x=10, y=40, width=300, height=300)
        title1= Label(self.frame1_no_file, text="No se ha cargado ningún archivo al programa.", font=("Consolas", 20), bg="white")
        title1.place(x=320, y=200)
        
        for frame in (self.frame1, self.frame2, self.frame3, self.frame4):
            frame.place(x=250, y=280, width=1050, height=480)
        
        frame_btn = Frame(self.window, bg="black")
        frame_btn.place(x=75, y=200)

        self.cargar_maquina_btn = Button(frame_btn, text="Cargar Archivo - Máquina", font=("Consolas", 15), bg="light sea green", command = lambda:[self.frame1.tkraise(), self.cargar_maquina()])
        self.cargar_maquina_btn.grid(row=0, column=0, padx=20)

        self.cargar_simulacion_btn = Button(frame_btn, text="Cargar Archivo - Simulación", font=("Consolas", 15), bg="light sea green", command = lambda:[self.frame2.tkraise(), self.cargar_simulacion()])
        self.cargar_simulacion_btn.grid(row=0, column=1, padx=20)

        self.ensamblar_btn = Button(frame_btn, text="Ensamblar productos", font=("Consolas", 15), bg="light sea green", command = lambda:[self.frame3.tkraise()])
        self.ensamblar_btn.grid(row=0, column=2, padx=20)

        self.reporte_cola_btn = Button(frame_btn, text="Reporte de cola de secuencia", font=("Consolas", 15), bg="light sea green", command = lambda:[self.frame4.tkraise()])
        self.reporte_cola_btn.grid(row=0, column=3, padx=20)

        self.ayuda_btn = Button(frame_btn, text="Ayuda", font=("Consolas", 15), bg="light sea green", command = lambda:[])
        self.ayuda_btn.grid(row=0, column=4, padx=20)

    def cargar_maquina(self):
        global lista_global_maquinas
        name_file = filedialog.askopenfilename(
            title = "Seleccionar archivo XML",
            initialdir = "./",
            filetypes = {
                ("Archivos XML", "*.xml"),
                ("Todos los archivos", "*.*")
            }
        )
        try:
            archivo = open(name_file)

            self.frame_file = Frame(self.frame1, bg="white")
            self.frame_file.place(x=0, y=0, relheight=1, relwidth=1)
            load_img1 = PhotoImage(file="images/load1.png")
            load_lb = Label(self.frame_file, image=load_img1, bg="white")
            load_lb.photo = load_img1
            load_lb.place(x=10, y=40, width=300, height=300) 
            title1= Label(self.frame_file, text="El archivo se encuentra cargado al programa.", font=("Consolas", 20), bg="white")
            title1.place(x=320, y=100)
            print("->Archivo leído con éxito")

            try:
                title2= Label(self.frame_file, text="Guardando la configuración de la máquina...", font=("Consolas", 20), bg="white")
                title2.place(x=320, y=150)

                maquina_configurada = self.configurar_maquina(os.path.basename(name_file), name_file)
                if maquina_configurada:
                    title2.config(text="Máquina configurada correctamente.")
                    title2.place(x=320, y=150)
                else:
                    title2.config(text="Ocurrió un error en el análisis del archivo. Revisar etiquetas.")
                    title2.place(x=320, y=150)
                title3= Label(self.frame_file, text="Máquinas cargadas en el programa:", font=("Consolas", 20), bg="white")
                title3.place(x=320, y=200)
                self.frame_listbox = Frame(self.frame_file)
                self.frame_listbox.place(x=350, y=250)
                scroll = Scrollbar(self.frame_listbox, orient=VERTICAL)
                scroll.pack(side=RIGHT, fill=Y)
                listbox_maquinas = Listbox(self.frame_listbox, width=50, font=("Consolas", 12), yscrollcommand=scroll.set)
                listbox_maquinas.pack()
                scroll.config(command=listbox_maquinas.yview)
                lista_global_maquinas.listbox_maquinas(listbox_maquinas)
            except Exception:
                traceback.print_exc()
                title2= Label(self.frame_file, text="Ocurrió un error inesperado. Ver consola :(", font=("Consolas", 20), bg="white")
                title2.place(x=320, y=150)
                print("-> Ocurrió un error inesperado, ver traceback.")

            archivo.close()

        except Exception:
            traceback.print_exc()
            print("->No se seleccionó un archivo")

    def is_number(self, caracter):
        if ord(caracter) >= 48 and ord(caracter) <= 57:
            return True
        return False

    def configurar_maquina(self, nombre_xml, ruta_xml):
        global lista_global_maquinas
        try:
            tree_xml_maquina = ET.parse(ruta_xml)
            root_original = tree_xml_maquina.getroot()
            root_string = ET.tostring(root_original)
            root_string = root_string.lower()
            root_maquina = ET.fromstring(root_string)
            cantidad_lineas = root_maquina.find('cantidadlineasproduccion').text
            cantidad_lineas = cantidad_lineas.replace('\n', '').replace('\t', '').replace(' ', '')
            cantidad_lineas = int(cantidad_lineas)
            listado_lineas = Lista_Lineas()
            for linea in root_maquina.find('listadolineasproduccion'):
                numero = linea.find('numero').text
                numero = numero.replace('\n', '').replace('\t', '').replace(' ', '')
                numero = int(numero)
                cantidad_componentes = linea.find('cantidadcomponentes').text
                cantidad_componentes = cantidad_componentes.replace('\n', '').replace('\t', '').replace(' ', '')
                cantidad_componentes = int(cantidad_componentes)
                tiempo_ensamblaje = linea.find('tiempoensamblaje').text
                tiempo_ensamblaje = tiempo_ensamblaje.replace('\n', '').replace('\t', '').replace(' ', '')
                tiempo_ensamblaje = int(tiempo_ensamblaje)
                listado_lineas.insertar(Linea(numero, cantidad_componentes, tiempo_ensamblaje))
            listado_productos = Lista_Productos()
            for producto in root_maquina.find('listadoproductos'):
                nombre = producto.find('nombre').text
                nombre = nombre.replace('\n', '').replace('\t', '')
                comandos = producto.find('elaboracion').text
                comandos = comandos.replace('\n', '').replace('\t', '')
                listado_comandos = Lista_Comandos()
                com = 0
                estado = ""
                num_actual = ""
                num_linea = 0
                num_componente = 0
                for caracter in comandos:
                    if com == 0:
                        if estado == "":
                            if caracter == "l":
                                estado = "linea"
                        elif estado == "linea":
                            if self.is_number(caracter):
                                num_actual += caracter
                            elif caracter == "p":
                                num_linea = int(num_actual)
                                num_actual = ""
                                estado = "componente"
                        elif estado == "componente":
                            if self.is_number(caracter):
                                num_actual += caracter
                            elif caracter == "p":
                                num_componente = int(num_actual)
                                listado_comandos.insertar(Comando(num_linea, num_componente, requiere_ensamblar=True))
                                com += 1
                                num_actual = ""
                                estado = ""
                    else:
                        if estado == "":
                            if caracter == "l":
                                estado = "linea"
                        elif estado == "linea":
                            if self.is_number(caracter):
                                num_actual += caracter
                            elif caracter == "p":
                                num_linea = int(num_actual)
                                num_actual = ""
                                estado = "componente"
                        elif estado == "componente":
                            if self.is_number(caracter):
                                num_actual += caracter
                            elif caracter == "p":
                                num_componente = int(num_actual)
                                listado_comandos.insertar(Comando(num_linea, num_componente))
                                com += 1
                                num_actual = ""
                                estado = ""
                listado_comandos.ultimo_true()
                listado_productos.insertar(Producto(nombre, listado_comandos))
            lista_global_maquinas.insertar(Maquina(nombre_xml, cantidad_lineas, listado_lineas, listado_productos))
            return True
        except:
            traceback.print_exc()
            return False

    def cargar_simulacion(self):
        global lista_global_simulaciones
        name_file = filedialog.askopenfilename(
            title = "Seleccionar archivo XML",
            initialdir = "./",
            filetypes = {
                ("Archivos XML", "*.xml"),
                ("Todos los archivos", "*.*")
            }
        )
        try:
            archivo = open(name_file)

            self.frame2_file = Frame(self.frame2, bg="white")
            self.frame2_file.place(x=0, y=0, relheight=1, relwidth=1)
            load_img1 = PhotoImage(file="images/load2.png")
            load_lb = Label(self.frame2_file, image=load_img1, bg="white")
            load_lb.photo = load_img1
            load_lb.place(x=10, y=60, width=300, height=300)
            title1= Label(self.frame2_file, text="El archivo se encuentra cargado al programa.", font=("Consolas", 20), bg="white")
            title1.place(x=320, y=100)
            print("->Archivo leído con éxito")

            try:
                title2= Label(self.frame2_file, text="Guardando la nueva simulación al programa...", font=("Consolas", 20), bg="white")
                title2.place(x=320, y=150)

                simulacion_guardada = self.nueva_simulacion(name_file)
                if simulacion_guardada:
                    title2.config(text="Nueva simulación guardada correctamente.")
                    title2.place(x=320, y=150)
                else:
                    title2.config(text="Ocurrió un error en el análisis del archivo. Revisar etiquetas.")
                    title2.place(x=320, y=150)
                title3= Label(self.frame2_file, text="Simulaciones cargadas en el programa:", font=("Consolas", 20), bg="white")
                title3.place(x=320, y=200)
                self.frame2_listbox = Frame(self.frame2_file)
                self.frame2_listbox.place(x=350, y=250)
                scroll = Scrollbar(self.frame2_listbox, orient=VERTICAL)
                scroll.pack(side=RIGHT, fill=Y)
                listbox_simulaciones = Listbox(self.frame2_listbox, width=50, font=("Consolas", 12), yscrollcommand=scroll.set)
                listbox_simulaciones.pack()
                scroll.config(command=listbox_simulaciones.yview)
                lista_global_simulaciones.listbox_simulaciones(listbox_simulaciones)
            except Exception:
                traceback.print_exc()
                title2= Label(self.frame2_file, text="Ocurrió un error inesperado. Ver consola :(", font=("Consolas", 20), bg="white")
                title2.place(x=320, y=150)
                print("-> Ocurrió un error inesperado. Ver Traceback")

            archivo.close()

        except Exception:
            traceback.print_exc()
            print("->No se seleccionó un archivo")
    
    def nueva_simulacion(self, ruta_xml):
        global lista_global_simulaciones
        try:
            tree_xml_simulacion = ET.parse(ruta_xml)
            root_original = tree_xml_simulacion.getroot()
            root_string = ET.tostring(root_original)
            root_string = root_string.lower()
            root_simulacion = ET.fromstring(root_string)
            nombre_simulacion = root_simulacion.find('nombre').text
            nombre_simulacion = nombre_simulacion.replace('\n', '').replace('\t', '')
            nombres_productos = Lista_Nombres_Productos()
            for prod in root_simulacion.find('listadoproductos'):
                nombre = prod.text
                nombre = nombre.replace('\n', '').replace('\t', '')
                nombres_productos.insertar(nombre)
            lista_global_simulaciones.insertar(Simulacion(nombre_simulacion, nombres_productos))
            return True
        except:
            traceback.print_exc()
            return False

if __name__ == '__main__':
    ventana = Tk()
    app = Interfaz(ventana)
    ventana.mainloop()