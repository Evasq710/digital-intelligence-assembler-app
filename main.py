from tkinter import font
from xml.etree import ElementTree as ET
from tkinter import *
from tkinter import filedialog, ttk
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
        title1= Label(self.frame4_no_file, text="No se ha cargado ninguna máquina al programa.", font=("Consolas", 20), bg="white")
        title1.place(x=320, y=200)

        self.frame3 = LabelFrame(self.window,bg="white", text="Ensamblar productos")
        self.frame3_no_file = Frame(self.frame3, bg="white")
        self.frame3_no_file.place(x=0, y=0, relheight=1, relwidth=1)
        load_img3 = PhotoImage(file="images/question1.png")
        load_lb3 = Label(self.frame3_no_file, image=load_img3, bg="white")
        load_lb3.photo = load_img3
        load_lb3.place(x=10, y=50, width=300, height=300)
        title1= Label(self.frame3_no_file, text="No se ha cargado ninguna máquina al programa.", font=("Consolas", 20), bg="white")
        title1.place(x=320, y=200)
        self.frame_ensamble = None

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

        self.ensamblar_btn = Button(frame_btn, text="Ensamblar productos", font=("Consolas", 15), bg="light sea green", command = lambda:[self.frame3.tkraise(), self.ensamblar_productos()])
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
            title1= Label(self.frame_file, text="El programa ha cargado archivos de máquinas exitosamente.", font=("Consolas", 20), bg="white")
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
            title1= Label(self.frame2_file, text="El programa ha cargado archivos de simulación exitosamente.", font=("Consolas", 20), bg="white")
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

    def ensamblar_productos(self):
        global lista_global_maquinas
        if lista_global_maquinas.primer_maquina is not None:
            self.frame3_file = Frame(self.frame3, bg="white")
            self.frame3_file.place(x=0, y=0, relheight=1, relwidth=1)
            load_img1 = PhotoImage(file="images/assembling.png")
            load_lb = Label(self.frame3_file, image=load_img1, bg="white")
            load_lb.photo = load_img1
            load_lb.place(x=300, y=20, width=450, height=450)
            self.frame_btn_ensamblaje = Frame(self.frame3_file, bg="white")
            self.frame_btn_ensamblaje.place(x=200, y=10)
            self.btn_producto= Button(self.frame_btn_ensamblaje, text="Ensamblar producto precargado", font=("Consolas", 14), bg="aquamarine", command= lambda:[self.ensamblar_producto_precargado()])
            self.btn_producto.grid(row=0, column=0, padx=20)
            self.btn_simulacion = Button(self.frame_btn_ensamblaje, text="Ensamblar simulación precargada", font=("Consolas", 14), bg="aquamarine", command=lambda:[self.ensamblar_simulacion_precargada()])
            self.btn_simulacion.grid(row=0, column=1, padx=20)
            if self.frame_ensamble is not None:
                self.frame_ensamble = None
        else:
            print("-> No se ha cargada ninguna máquina al programa")

    def ensamblar_producto_precargado(self):
        global lista_global_maquinas
        self.frame_ensamble = Frame(self.frame3_file, bg="white")
        self.frame_ensamble.place(x=50, y=60, width=950, height=390)
        lb = Label(self.frame_ensamble, text="Productos cargados al programa:", font=("Consolas", 14), bg="white")
        lb.place(x=10, y=10)
        self.frame3_listbox_productos = Frame(self.frame_ensamble)
        self.frame3_listbox_productos.place(x=40, y=50, width=250, height=250)
        scroll = Scrollbar(self.frame3_listbox_productos, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)
        listbox_productos = Listbox(self.frame3_listbox_productos, font=("Consolas", 12), yscrollcommand=scroll.set, width=250, height=250)
        listbox_productos.pack()
        scroll.config(command=listbox_productos.yview)
        lista_global_maquinas.listbox_productos_cargados(listbox_productos)
        ensamblar_btn = Button(self.frame_ensamble, text="Ensamblar producto", font=("Consolas", 14), bg="green yellow", command=lambda:[self.ensamblar_producto_individual(listbox_productos.get(ANCHOR))])
        ensamblar_btn.place(x=50, y=320)
        as_img = PhotoImage(file="images/assembling2.png")
        self.as_lb = Label(self.frame_ensamble, image=as_img, bg="white")
        self.as_lb.photo = as_img
        self.as_lb.place(x=450, y=50, width=300, height=300)
        self.lb_producto = None
        self.lb_tiempo_total = None

    def ensamblar_producto_individual(self, nombre_producto):
        global lista_global_maquinas
        if nombre_producto != "":
            lineas = lista_global_maquinas.cantidad_lineas(nombre_producto)
            if lineas is not False:
                self.as_lb.destroy()
                if self.lb_producto is not None:
                    self.lb_producto.destroy()
                self.lb_producto = Label(self.frame_ensamble, text=nombre_producto, font=("Consolas", 14, 'bold'), bg="white")
                self.lb_producto.place(x=550, y=10)
                self.frame3_treview = Frame(self.frame_ensamble)
                self.frame3_treview.place(x=300, y=50, width=650, height=250)
                estilos = ttk.Style()
                estilos.theme_use('default')
                estilos.configure("Treeview", font=("Consolas", 10))
                estilos.layout("Treeview.Heading")
                estilos.configure("Treeview.Heading", font=("Consolas", 10, 'bold'), background="black", foreground="white")
                treeview_ensamblaje = ttk.Treeview(self.frame3_treview, columns=[f"#{n}" for n in range(1, lineas + 1)], style="Treeview", height=250)
                if lista_global_maquinas.boolean_producto_ensamblado(nombre_producto):
                    print("->Producto ya ensamblado con anterioridad")
                    segundos_ensamblaje = lista_global_maquinas.treeview_producto_ensamblado(nombre_producto, treeview_ensamblaje)
                else:
                    print("->Producto no ha sido ensamblado")
                    segundos_ensamblaje = lista_global_maquinas.ensamblar_producto(nombre_producto, treeview_ensamblaje)
                scroll_vertical = Scrollbar(self.frame3_treview, orient=VERTICAL, command=treeview_ensamblaje.yview)
                scroll_vertical.pack(side=RIGHT, fill=Y)
                scroll_horizontal = Scrollbar(self.frame3_treview, orient=HORIZONTAL, command=treeview_ensamblaje.xview)
                scroll_horizontal.pack(side=BOTTOM, fill=X)
                treeview_ensamblaje.configure(yscrollcommand=scroll_vertical.set ,xscrollcommand = scroll_horizontal.set)
                treeview_ensamblaje.pack()
                if self.lb_tiempo_total is not None:
                    self.lb_tiempo_total.destroy()
                self.lb_tiempo_total = Label(self.frame_ensamble, text=f"Tiempo óptimo de ensamblaje: {segundos_ensamblaje} segundos", font=("Consolas", 14), bg="white")
                self.lb_tiempo_total.place(x=300, y=330)
            else:
                print("-> Ocurrió un error, no se encontró el producto seleccionado en la lista de máquinas cargadas")

    def ensamblar_simulacion_precargada(self):
        global lista_global_simulaciones
        self.frame_ensamble_simulacion = Frame(self.frame3_file, bg="white")
        self.frame_ensamble_simulacion.place(x=50, y=60, width=950, height=390)
        lb = Label(self.frame_ensamble_simulacion, text="Simulaciones cargadas al programa:", font=("Consolas", 14), bg="white")
        lb.place(x=10, y=10)
        self.frame3_listbox_simulaciones = Frame(self.frame_ensamble_simulacion)
        self.frame3_listbox_simulaciones.place(x=50, y=50, height=250, width=250)
        scroll = Scrollbar(self.frame3_listbox_simulaciones, orient=VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)
        listbox_simulaciones = Listbox(self.frame3_listbox_simulaciones, font=("Consolas", 12), yscrollcommand=scroll.set, width=250, height=250)
        listbox_simulaciones.pack()
        scroll.config(command=listbox_simulaciones.yview)
        lista_global_simulaciones.listbox_simulaciones(listbox_simulaciones)
        ensamblar_btn = Button(self.frame_ensamble_simulacion, text="Ensamblar productos en simulación", font=("Consolas", 14), bg="green yellow", command=lambda:[self.ensamblar_productos_simulacion(listbox_simulaciones.get(ANCHOR))])
        ensamblar_btn.place(x=0, y=320)
        as_img = PhotoImage(file="images/assembling2.png")
        self.as_lb_sim = Label(self.frame_ensamble_simulacion, image=as_img, bg="white")
        self.as_lb_sim.photo = as_img
        self.as_lb_sim.place(x=450, y=50, width=300, height=300)
        self.lb_simulacion = None
    
    def ensamblar_productos_simulacion(self, nombre_simulacion):
        global lista_global_simulaciones
        global lista_global_maquinas
        if nombre_simulacion != "":
            simulacion_escogida = lista_global_simulaciones.retornar_simulacion(nombre_simulacion)
            productos_no_encontrados = Lista_Nombres_Productos()
            
            self.as_lb_sim.destroy()
            canvas_resultados = Canvas(self.frame_ensamble_simulacion, bg="white")
            scrollbar = ttk.Scrollbar(canvas_resultados, orient="vertical", command=canvas_resultados.yview)
            frame_con_scroll = Frame(canvas_resultados, bg="white")
            frame_con_scroll.bind(
                "<Configure>",
                lambda e: canvas_resultados.configure(
                    scrollregion=canvas_resultados.bbox("all")
                )
            )
            canvas_resultados.create_window((0, 0), window=frame_con_scroll, anchor="nw", width=580)
            canvas_resultados.configure(yscrollcommand=scrollbar.set)
            
            Label(frame_con_scroll, text=simulacion_escogida.nombre, font=("Consolas", 14, 'bold'), bg="black", fg="white").pack()
            Label(frame_con_scroll, text="", font=("Consolas", 14, 'bold'), bg="white").pack()

            try:
                xml_generado = simulacion_escogida.listado_nombres_productos.ensamblar_productos(lista_global_maquinas, productos_no_encontrados, frame_con_scroll, simulacion_escogida.nombre)
            except:
                traceback.print_exc()
                print("->Ocurrió un error en el ensamblaje de la simulación " + nombre_simulacion)
            
            if productos_no_encontrados.primer_nombre is not None:
                Label(frame_con_scroll, text="Productos no encontrados (deben cargarse a una máquina)", font=("Consolas", 14, 'bold'), bg="red", fg="white").pack()
                productos_no_encontrados.lb_productos_no_encontrados(frame_con_scroll)
                Label(frame_con_scroll, text="", font=("Consolas", 14, 'bold'), bg="white").pack()
            else:
                Label(frame_con_scroll, text="¡Todos los productos han sido ensamblados correctamente!", font=("Consolas", 14, 'bold'), bg="green", fg="white").pack()
                Label(frame_con_scroll, text="", font=("Consolas", 14, 'bold'), bg="white").pack()

            if xml_generado:
                Label(frame_con_scroll, text="¡Se ha generado el reporte XML con éxito!", font=("Consolas", 14, 'bold'), bg="green", fg="white").pack()
                Label(frame_con_scroll, text="", font=("Consolas", 14, 'bold'), bg="white").pack()
            else:
                Label(frame_con_scroll, text="Ocurrió un error en la generación del reporte XML :(", font=("Consolas", 14, 'bold'), bg="green", fg="white").pack()
                Label(frame_con_scroll, text="", font=("Consolas", 14, 'bold'), bg="white").pack()

            canvas_resultados.place(x=350, y=50, width=600, height=250)
            scrollbar.pack(side="right", fill="y")

if __name__ == '__main__':
    ventana = Tk()
    app = Interfaz(ventana)
    ventana.mainloop()