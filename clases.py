from tkinter import END, Label, Text
from xml.etree import ElementTree as ET

# ========== MAQUINAS ==========
class Maquina:
    def __init__(self, nombre_archivo, cantidad_lineas, listado_lineas, listado_productos):
        self.nombre_archivo = nombre_archivo
        self.cantidad_lineas = cantidad_lineas
        self.listado_lineas = listado_lineas
        self.listado_productos = listado_productos

class Nodo_Maquina:
    def __init__(self, maquina = None, siguiente = None):
        self.maquina = maquina
        self.siguiente = siguiente

class Lista_Maquinas:
    def __init__(self):
        self.primer_maquina = None
    
    def insertar(self, nueva_maquina):
        if self.primer_maquina is None:
            self.primer_maquina = Nodo_Maquina(maquina=nueva_maquina)
        else:
            maquina_actual = self.primer_maquina
            while maquina_actual.siguiente:
                maquina_actual = maquina_actual.siguiente
            maquina_actual.siguiente = Nodo_Maquina(maquina=nueva_maquina)
    
    def listbox_maquinas(self, listbox):
        actual = self.primer_maquina
        while actual:
            listbox.insert(END, actual.maquina.nombre_archivo)
            actual = actual.siguiente

    def listbox_productos_cargados(self, listbox):
        actual = self.primer_maquina
        while actual:
            actual.maquina.listado_productos.insertar_nombre_productos_LB(listbox)
            actual = actual.siguiente
    
    def boolean_producto_ensamblado(self, nombre_producto):
        actual = self.primer_maquina
        while actual:
            encontrado = actual.maquina.listado_productos.producto_en_maquina(nombre_producto)
            if encontrado:
                return actual.maquina.listado_productos.producto_ensamblado(nombre_producto)
            actual = actual.siguiente

    def cantidad_lineas(self, nombre_producto):
        actual = self.primer_maquina
        while actual:
            encontrado = actual.maquina.listado_productos.producto_en_maquina(nombre_producto)
            if encontrado:
                return actual.maquina.cantidad_lineas
            actual = actual.siguiente
        return False
    
    def ensamblar_producto(self, nombre_producto, treeview):
        actual = self.primer_maquina
        while actual:
            product_assembling = actual.maquina.listado_productos.devolver_producto(nombre_producto)
            if product_assembling is not None:
                #Cabeceras
                for n in range(actual.maquina.cantidad_lineas + 1):
                    if n == 0:
                        treeview.column(f"#{n}", width = 50)
                        treeview.heading(f"#{n}", text = "Tiempo")
                    else:
                        treeview.column(f"#{n}", width = 150, anchor='center')
                        treeview.heading(f"#{n}", text = f"Línea {n}")
                actual.maquina.listado_lineas.pendientes_por_linea(product_assembling.listado_comandos)
                #Acciones por segundo
                segundos = 0
                while True:
                    segundos += 1
                    actual.maquina.listado_lineas.acciones_por_segundo(segundos, product_assembling)
                    if product_assembling.ensamblado:
                        product_assembling.segundos_ensamblaje_total = segundos
                        for i in range(segundos):
                            treeview.insert("", END, text=f"{i+1}", values=product_assembling.listado_acciones.devolver_acciones(i+1))
                        break
                root_salidasimulacion = "<SalidaSimulacion>"
                root_salidasimulacion += f"\n\t<Nombre>Simulación Individual {product_assembling.nombre}</Nombre>"
                root_salidasimulacion += "\n\t<ListadoProductos>"
                producto_xml = product_assembling.salida_xml()
                root_salidasimulacion += producto_xml
                root_salidasimulacion += "\n\t</ListadoProductos>"
                root_salidasimulacion += "\n</SalidaSimulacion>"

                html_simulacion = '''<!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">'''
                html_simulacion += f'\n<link rel="stylesheet" href="{product_assembling.nombre}.css" type="text/css" />'
                html_simulacion += '''\n    <title>Reporte HTML</title>
                </head>
                <body>
                    <li style="float: left; padding-left: 3%; padding-right: 20px;"><span class="material-icons md-light md-100">precision_manufacturing</span></li>
                    <h1>Reporte Simulación individual</h1>'''
                producto_html = product_assembling.salida_html(actual.maquina.cantidad_lineas)
                html_simulacion += producto_html
                html_simulacion += '''\n    <footer>
                        <p>Elías Abraham Vasquez Soto - 201900131</p>
                        <p>Proyecto 1 - Laboratorio Introducción a la Programación y Computación 2 E</p>        
                        <img src="images/logo_usac.png" width="220" height="60"/>
                    </footer>

                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
                </body>
                </html>'''

                css_simulacion = '''html {
                    min-height: 100%;
                    position: relative;
                }

                body {
                    background-color:rgb(1, 11, 26);
                    padding-top: 20px;
                    margin-bottom: 150px;
                }

                /* ===== Iconos de Google ===== */
                /* Rules for sizing the icon. */
                .material-icons.md-24 { font-size: 24px; }
                .material-icons.md-30 { font-size: 30px; }
                .material-icons.md-100 { font-size: 100px; }
                /* Rules for using icons as black on a light background. */
                .material-icons.md-dark { color: rgba(0, 0, 0, 0.54); }
                .material-icons.md-dark.md-inactive { color: rgba(0, 0, 0, 0.26); }
                /* Rules for using icons as white on a dark background. */
                .material-icons.md-light { color: rgba(255, 255, 255, 1); }
                .material-icons.md-light.md-inactive { color: rgba(255, 255, 255, 0.3); }

                h1 {
                    color: white;
                    font-family: 'Lato', sans-serif;
                    font-size: 75px;
                }

                .datos-reporte {
                    background-color: rgb(255, 255, 255);
                    padding-top: 20px;
                    padding-bottom: 20px;
                    padding-left: 50px;
                    margin: 30px 100px 30px 100px;
                }

                .datos {
                    font-family: 'Lato', sans-serif;
                    font-size: 30px;
                    padding-left: 20px;
                }

                .tabla-ensamblaje {
                    overflow-x: scroll;
                    padding-top: 20px;
                    text-align: center;
                    font-family: 'Lato', sans-serif;
                    font-size: 20px;
                    letter-spacing: 1px;
                    width: 96%;
                }

                table {
                    width: 100%;
                    table-layout: fixed;
                }

                table td, th{    
                    color: white;
                    width: 200px;
                }

                table #tiempo {
                    width: 100px;
                }

                #uno {
                    background-color: rgb(61, 57, 48);
                }

                #dos {
                    background-color: rgb(54, 1, 1);
                }

                footer {
                    color: white;
                    line-height: 10px;
                    text-align: center;
                    padding-top: 20px;
                    padding-bottom: 5px;
                    font-size: 15px;
                    font-family: 'Lato', sans-serif;
                    position: absolute;
                    bottom: 0;
                    width: 100%;
                    background-image: url("images/footer.png");
                }'''

                try:
                    root = ET.fromstring(root_salidasimulacion)
                    tree_xml_salida = ET.ElementTree(element=root)
                    tree_xml_salida.write(f"Salidas XML/{product_assembling.nombre}.xml", encoding="utf-8", xml_declaration=True)
                    print("--> El archivo de simulación XML se creo exitosamente.")
                except Exception as e:
                    print(e)
                    print("--> No pudo crearse el archivo XML.")
                try:
                    reporte_html = open(f"Reportes HTML/{product_assembling.nombre}.html", "w",encoding="utf8")
                    reporte_html.write(html_simulacion)
                    reporte_html.close()
                    print("--> El reporte de simulación HTML se creo exitosamente.")
                except Exception as e:
                    print(e)
                    print("--> No pudo crearse el archivo HTML.")
                try:
                    reporte_css = open(f"Reportes HTML/{product_assembling.nombre}.css", "w",encoding="utf8")
                    reporte_css.write(css_simulacion)
                    reporte_css.close()
                    print("--> El CSS del reporte de simulación se creo exitosamente.")
                except Exception as e:
                    print(e)
                    print("--> No pudo crearse el archivo CSS.")
                
                return segundos
            actual = actual.siguiente
    
    def treeview_producto_ensamblado(self, nombre_producto, treeview):
        actual = self.primer_maquina
        while actual:
            product_assembling = actual.maquina.listado_productos.devolver_producto(nombre_producto)
            if product_assembling is not None:
                #Cabeceras
                for n in range(actual.maquina.cantidad_lineas + 1):
                    if n == 0:
                        treeview.column(f"#{n}", width = 50)
                        treeview.heading(f"#{n}", text = "Tiempo")
                    else:
                        treeview.column(f"#{n}", width = 150, anchor='center')
                        treeview.heading(f"#{n}", text = f"Línea {n}")
                for i in range(product_assembling.segundos_ensamblaje_total):
                    treeview.insert("", END, text=f"{i+1}", values=product_assembling.listado_acciones.devolver_acciones(i+1))
                root_salidasimulacion = "<SalidaSimulacion>"
                root_salidasimulacion += f"\n\t<Nombre>Simulación Individual {product_assembling.nombre}</Nombre>"
                root_salidasimulacion += "\n\t<ListadoProductos>"
                producto_xml = product_assembling.salida_xml()
                root_salidasimulacion += producto_xml
                root_salidasimulacion += "\n\t</ListadoProductos>"
                root_salidasimulacion += "\n</SalidaSimulacion>"

                html_simulacion = '''<!DOCTYPE html>
                <html lang="es">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
                    <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">'''
                html_simulacion += f'\n<link rel="stylesheet" href="{product_assembling.nombre}.css" type="text/css" />'
                html_simulacion += '''\n    <title>Reporte HTML</title>
                </head>
                <body>
                    <li style="float: left; padding-left: 3%; padding-right: 20px;"><span class="material-icons md-light md-100">precision_manufacturing</span></li>
                    <h1>Reporte Simulación individual</h1>'''
                producto_html = product_assembling.salida_html(actual.maquina.cantidad_lineas)
                html_simulacion += producto_html
                html_simulacion += '''\n    <footer>
                        <p>Elías Abraham Vasquez Soto - 201900131</p>
                        <p>Proyecto 1 - Laboratorio Introducción a la Programación y Computación 2 E</p>        
                        <img src="images/logo_usac.png" width="220" height="60"/>
                    </footer>

                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
                </body>
                </html>'''

                css_simulacion = '''html {
                    min-height: 100%;
                    position: relative;
                }

                body {
                    background-color:rgb(1, 11, 26);
                    padding-top: 20px;
                    margin-bottom: 150px;
                }

                /* ===== Iconos de Google ===== */
                /* Rules for sizing the icon. */
                .material-icons.md-24 { font-size: 24px; }
                .material-icons.md-30 { font-size: 30px; }
                .material-icons.md-100 { font-size: 100px; }
                /* Rules for using icons as black on a light background. */
                .material-icons.md-dark { color: rgba(0, 0, 0, 0.54); }
                .material-icons.md-dark.md-inactive { color: rgba(0, 0, 0, 0.26); }
                /* Rules for using icons as white on a dark background. */
                .material-icons.md-light { color: rgba(255, 255, 255, 1); }
                .material-icons.md-light.md-inactive { color: rgba(255, 255, 255, 0.3); }

                h1 {
                    color: white;
                    font-family: 'Lato', sans-serif;
                    font-size: 75px;
                }

                .datos-reporte {
                    background-color: rgb(255, 255, 255);
                    padding-top: 20px;
                    padding-bottom: 20px;
                    padding-left: 50px;
                    margin: 30px 100px 30px 100px;
                }

                .datos {
                    font-family: 'Lato', sans-serif;
                    font-size: 30px;
                    padding-left: 20px;
                }

                .tabla-ensamblaje {
                    overflow-x: scroll;
                    padding-top: 20px;
                    text-align: center;
                    font-family: 'Lato', sans-serif;
                    font-size: 20px;
                    letter-spacing: 1px;
                    width: 96%;
                }

                table {
                    width: 100%;
                    table-layout: fixed;
                }

                table td, th{    
                    color: white;
                    width: 200px;
                }

                table #tiempo {
                    width: 100px;
                }

                #uno {
                    background-color: rgb(61, 57, 48);
                }

                #dos {
                    background-color: rgb(54, 1, 1);
                }

                footer {
                    color: white;
                    line-height: 10px;
                    text-align: center;
                    padding-top: 20px;
                    padding-bottom: 5px;
                    font-size: 15px;
                    font-family: 'Lato', sans-serif;
                    position: absolute;
                    bottom: 0;
                    width: 100%;
                    background-image: url("images/footer.png");
                }'''
                try:
                    root = ET.fromstring(root_salidasimulacion)
                    tree_xml_salida = ET.ElementTree(element=root)
                    tree_xml_salida.write(f"Salidas XML/{product_assembling.nombre}.xml", encoding="utf-8", xml_declaration=True)
                    print("--> El archivo de simulación individual XML se creo exitosamente.")
                except Exception as e:
                    print(e)
                    print("--> No pudo crearse el archivo XML individual.")
                try:
                    reporte_html = open(f"Reportes HTML/{product_assembling.nombre}.html", "w",encoding="utf8")
                    reporte_html.write(html_simulacion)
                    reporte_html.close()
                    print("--> El reporte de simulación HTML se creo exitosamente.")
                except Exception as e:
                    print(e)
                    print("--> No pudo crearse el archivo HTML.")
                try:
                    reporte_css = open(f"Reportes HTML/{product_assembling.nombre}.css", "w",encoding="utf8")
                    reporte_css.write(css_simulacion)
                    reporte_css.close()
                    print("--> El CSS del reporte de simulación se creo exitosamente.")
                except Exception as e:
                    print(e)
                    print("--> No pudo crearse el archivo CSS.")
                return product_assembling.segundos_ensamblaje_total
            actual = actual.siguiente

    def boolean_producto_cargado(self, nombre_producto):
        actual = self.primer_maquina
        encontrado = False
        while actual:
            encontrado = actual.maquina.listado_productos.producto_en_maquina(nombre_producto)
            if encontrado:
                break
            actual = actual.siguiente
        return encontrado
    
    def obtener_producto(self, nombre_producto):
        actual = self.primer_maquina
        while actual:
            product = actual.maquina.listado_productos.devolver_producto(nombre_producto)
            if product is not None:
                return product
            actual = actual.siguiente
    
    def ensamblar_por_simulacion(self, nombre_producto):
        actual = self.primer_maquina
        while actual:
            product_assembling = actual.maquina.listado_productos.devolver_producto(nombre_producto)
            if product_assembling is not None:
                actual.maquina.listado_lineas.pendientes_por_linea(product_assembling.listado_comandos)
                #Acciones por segundo
                segundos = 0
                while True:
                    segundos += 1
                    actual.maquina.listado_lineas.acciones_por_segundo(segundos, product_assembling)
                    if product_assembling.ensamblado:
                        product_assembling.segundos_ensamblaje_total = segundos
                        break
                return True
            actual = actual.siguiente
        return False

# ========== LINEAS DE PRODUCCIÓN EN MÁQUINA ==========
class Linea:
    def __init__(self, numero, cantidad_componentes, tiempo_ensamblaje):
        self.numero = numero
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.listado_componentes = Lista_Componentes()

        for num_componente in range(cantidad_componentes):
            self.listado_componentes.insertar(num_componente + 1)

    def crear_componentes_pendientes(self, listado_comandos_producto):
        self.listado_componentes_pendientes = listado_comandos_producto.devolver_componentes_pendientes(self.numero)
        self.componente_actual = 0

class Nodo_Linea:
    def __init__(self, linea = None, siguiente = None):
        self.linea = linea
        self.siguiente = siguiente

class Lista_Lineas:
    def __init__(self):
        self.primer_linea = None

    def insertar(self, nueva_linea):
        if self.primer_linea is None:
            self.primer_linea = Nodo_Linea(linea=nueva_linea)
        else:
            linea_actual = self.primer_linea
            while linea_actual.siguiente:
                linea_actual = linea_actual.siguiente
            linea_actual.siguiente = Nodo_Linea(linea=nueva_linea)
    
    def pendientes_por_linea(self, listado_comandos_producto):
        actual = self.primer_linea
        while actual:
            actual.linea.crear_componentes_pendientes(listado_comandos_producto)
            actual = actual.siguiente

    def acciones_por_segundo(self, segundo, producto):
        actual = self.primer_linea
        componente_ensamblado = False
        while actual:
            componentes_pendientes = actual.linea.listado_componentes_pendientes
            hay_pendientes = componentes_pendientes.hay_componentes_pendientes()
            if hay_pendientes:
                if actual.linea.componente_actual == componentes_pendientes.primer_componente.numero:
                    if producto.listado_comandos.ensamblando_otro_componente(actual.linea.numero, actual.linea.componente_actual):
                        producto.nueva_accion(segundo, actual.linea.numero, False, False)
                    else:
                        comando_requiere_ensamblar = producto.listado_comandos.devolver_requiere_ensamblar()
                        if actual.linea.numero == comando_requiere_ensamblar.linea and actual.linea.componente_actual == comando_requiere_ensamblar.componente:
                            if comando_requiere_ensamblar.ensamblando:
                                producto.nueva_accion(segundo, actual.linea.numero, True, False, componente=actual.linea.componente_actual)
                                producto.segundos_ensamblando += 1
                            else:
                                comando_requiere_ensamblar.ensamblando = True
                                producto.nueva_accion(segundo, actual.linea.numero, True, False, componente=actual.linea.componente_actual)
                                producto.segundos_ensamblando += 1
                            if producto.segundos_ensamblando == actual.linea.tiempo_ensamblaje:
                                if comando_requiere_ensamblar.es_ultimo:
                                    comando_requiere_ensamblar.requiere_ensamblar = False
                                    producto.ensamblado = True
                                    componente_ensamblado = True
                                    print(f"Ensamblado componente L{comando_requiere_ensamblar.linea}C{comando_requiere_ensamblar.componente}")
                                    print("->Producto ensamblado totalmente")
                                else:
                                    print(f"Ensamblado componente L{comando_requiere_ensamblar.linea}C{comando_requiere_ensamblar.componente}")
                                    componente_ensamblado = True
                                    producto.segundos_ensamblando = 0
                                    componentes_pendientes.eliminar_primer_componente_pendiente()
                        else:
                            producto.nueva_accion(segundo, actual.linea.numero, False, False)
                elif actual.linea.componente_actual < componentes_pendientes.primer_componente.numero:
                    actual.linea.componente_actual += 1
                    producto.nueva_accion(segundo, actual.linea.numero, False, True, componente=actual.linea.componente_actual)
                else:
                    actual.linea.componente_actual = actual.linea.componente_actual - 1
                    producto.nueva_accion(segundo, actual.linea.numero, False, True, componente=actual.linea.componente_actual)
            else:
                producto.nueva_accion(segundo, actual.linea.numero, False, False)
            actual = actual.siguiente
        if componente_ensamblado:
            comando_requiere_ensamblar.ensamblando = False
            producto.listado_comandos.estado_requiere_siguiente()

# ========== COMPONENTES EN LINEA, TODOS Y PENDIENTES ==========
class Nodo_Componente:
    def __init__(self, numero = None, siguiente = None):
        self.numero = numero
        self.siguiente = siguiente

class Lista_Componentes:
    def __init__(self):
        self.primer_componente = None
    
    def insertar(self, numero_nuevo_componente):
        if self.primer_componente is None:
            self.primer_componente = Nodo_Componente(numero=numero_nuevo_componente)
        else:
            componente_actual = self.primer_componente
            while componente_actual.siguiente:
                componente_actual = componente_actual.siguiente
            componente_actual.siguiente = Nodo_Componente(numero=numero_nuevo_componente)
    
    def hay_componentes_pendientes(self):
        if self.primer_componente:
            return True
        return False
    
    def eliminar_primer_componente_pendiente(self):
        actual = self.primer_componente
        self.primer_componente = actual.siguiente
        actual.siguiente = None

    # def eliminar_componentes_pendientes(self):
    #     if self.primer_componente:
    #         self.primer_componente = None

# ========== PRODUCTOS EN MÁQUINA ==========
class Producto:
    def __init__(self, nombre, listado_comandos, ensamblado = False):
        self.nombre = nombre
        self.listado_comandos = listado_comandos
        self.ensamblado = ensamblado
        self.segundos_ensamblaje_total = 0
        self.listado_acciones = Lista_Acciones()
        self.segundos_ensamblando = 0
    
    def nueva_accion(self, segundo, linea, ensamblando, moviendose, componente=None):
        self.listado_acciones.insertar(Accion(segundo, linea, ensamblando, moviendose, componente))
    
    def salida_xml(self):
        producto_xml = "\n\t\t<Producto>"
        producto_xml += f"\n\t\t\t<Nombre>{self.nombre}</Nombre>"
        producto_xml += f"\n\t\t\t<TiempoTotal>{self.segundos_ensamblaje_total}</TiempoTotal>"
        producto_xml += "\n\t\t\t<ElaboracionOptima>"
        for i in range(self.segundos_ensamblaje_total):
            segundo = i+1
            producto_xml += f'\n\t\t\t\t<Tiempo NoSegundo="{segundo}">'
            lineas_ensamblaje = self.listado_acciones.acciones_por_segundo_XML(segundo)
            producto_xml += lineas_ensamblaje
            producto_xml += '\n\t\t\t\t</Tiempo>'
        producto_xml += "\n\t\t\t</ElaboracionOptima>"
        producto_xml += "\n\t\t</Producto>"
        return producto_xml
    
    def salida_html(self, num_lineas):
        producto_html = f'''\n    <div class="datos-reporte">
            <p class="datos">Producto: {self.nombre}</p>
            <p class="datos">Tiempo óptimo de ensamblaje: {self.segundos_ensamblaje_total} segundos</p>
                <div class="tabla-ensamblaje">
                    <table class="table table-striped table-hover">
                        <thead style="background-color: black; color: white;">
                            <tr>
                            <th scope="col" id="tiempo">Tiempo</th>'''
        for i in range(num_lineas):
            producto_html += f'\n<th scope="col">Linea {i + 1}</th>'
        producto_html += '''\n                </tr>
                        </thead>
                        <tbody>'''
        id_fila = ""
        for i in range(self.segundos_ensamblaje_total):
            segundo = i+1
            id_fila = "uno" if segundo%2 == 1 else "dos"
            lineas_ensamblaje = self.listado_acciones.acciones_por_segundo_HTML(segundo, id_fila)
            producto_html += lineas_ensamblaje
        producto_html += '''\n            </tbody>
                </table>
            </div>
        </div>'''
        return producto_html

class Nodo_Producto:
    def __init__(self, producto = None, siguiente = None):
        self.producto = producto
        self.siguiente = siguiente

class Lista_Productos:
    def __init__(self):
        self.primer_producto = None
    
    def insertar(self, nuevo_producto):
        if self.primer_producto is None:
            self.primer_producto = Nodo_Producto(producto=nuevo_producto)
        else:
            producto_actual = self.primer_producto
            while producto_actual.siguiente:
                producto_actual = producto_actual.siguiente
            producto_actual.siguiente = Nodo_Producto(producto=nuevo_producto)

    def insertar_nombre_productos_LB(self, listbox):
        actual = self.primer_producto
        while actual:
            listbox.insert(END, actual.producto.nombre)
            actual = actual.siguiente
    
    def producto_en_maquina(self, nombre_producto):
        actual = self.primer_producto
        while actual:
            if actual.producto.nombre == nombre_producto:
                return True
            actual = actual.siguiente
        return False

    def producto_ensamblado(self, nombre_producto):
        actual = self.primer_producto
        while actual:
            if actual.producto.nombre == nombre_producto:
                return actual.producto.ensamblado
            actual = actual.siguiente
    
    def devolver_producto(self, nombre_producto):
        actual = self.primer_producto
        while actual:
            if actual.producto.nombre == nombre_producto:
                return actual.producto
            actual = actual.siguiente
        return None

# ========== COMANDOS EN PRODUCTO ==========
class Comando:
    def __init__(self, linea, componente, requiere_ensamblar = False, es_ultimo = False, ensamblando = False):
        self.linea = linea
        self.componente = componente
        self.requiere_ensamblar = requiere_ensamblar
        self.es_ultimo = es_ultimo
        self.ensamblando = ensamblando

class Nodo_Comando:
    def __init__(self, comando = None, siguiente = None):
        self.comando = comando
        self.siguiente = siguiente
    
class Lista_Comandos:
    def __init__(self):
        self.primer_comando = None
    
    def insertar(self, nuevo_comando):
        if self.primer_comando is None:
            self.primer_comando = Nodo_Comando(comando=nuevo_comando)
        else:
            comando_actual = self.primer_comando
            while comando_actual.siguiente:
                comando_actual = comando_actual.siguiente
            comando_actual.siguiente = Nodo_Comando(comando=nuevo_comando)
    
    def ultimo_true(self):
        if self.primer_comando is not None:
            actual = self.primer_comando
            while actual.siguiente:
                actual = actual.siguiente
            actual.comando.es_ultimo = True
    
    def devolver_componentes_pendientes(self, linea):
        actual = self.primer_comando
        listado_pendientes = Lista_Componentes()
        while actual:
            if actual.comando.linea == linea:
                listado_pendientes.insertar(actual.comando.componente)
            actual = actual.siguiente
        return listado_pendientes
    
    def ensamblando_otro_componente(self, linea_actual, componente_actual):
        actual = self.primer_comando
        ensamblando_otro = False
        while actual:
            if actual.comando.componente != componente_actual:
                if actual.comando.ensamblando is True:
                    ensamblando_otro = True
                    break
            elif actual.comando.linea != linea_actual:
                if actual.comando.ensamblando is True:
                    ensamblando_otro = True
                    break
            actual = actual.siguiente
        return ensamblando_otro
    
    def devolver_requiere_ensamblar(self):
        actual = self.primer_comando
        while actual:
            if actual.comando.requiere_ensamblar:
                return actual.comando
            actual = actual.siguiente
    
    def estado_requiere_siguiente(self):
        actual = self.primer_comando
        while actual:
            if actual.comando.requiere_ensamblar:
                actual.comando.requiere_ensamblar = False
                actual.siguiente.comando.requiere_ensamblar = True
                break
            actual = actual.siguiente
    
    def devolver_str_comandos(self):
        comandos =""
        actual = self.primer_comando
        while actual:
            if actual.siguiente is not None:
                comandos += "L" + str(actual.comando.linea) + "C" + str(actual.comando.componente) + " -> "
            else:
                comandos += "L" + str(actual.comando.linea) + "C" + str(actual.comando.componente)
            actual = actual.siguiente
        return comandos

# ========== SIMULACIONES DE ENSAMBLAJE DE PRODUCTOS ==========
class Simulacion:
    def __init__(self, nombre, listado_nombres_productos):
        self.nombre = nombre
        self.listado_nombres_productos = listado_nombres_productos

class Nodo_Simulacion:
    def __init__(self, simulacion = None, siguiente = None):
        self.simulacion = simulacion
        self.siguiente = siguiente

class Lista_Simulaciones:
    def __init__(self):
        self.primer_simulacion = None
    
    def insertar(self, nueva_simulacion):
        if self.primer_simulacion is None:
            self.primer_simulacion = Nodo_Simulacion(simulacion=nueva_simulacion)
        else:
            simulacion_actual = self.primer_simulacion
            while simulacion_actual.siguiente:
                simulacion_actual = simulacion_actual.siguiente
            simulacion_actual.siguiente = Nodo_Simulacion(simulacion=nueva_simulacion)

    def listbox_simulaciones(self, listbox):
        actual = self.primer_simulacion
        while actual:
            listbox.insert(END, actual.simulacion.nombre)
            actual = actual.siguiente
    
    def retornar_simulacion(self, nombre_simulacion):
        actual = self.primer_simulacion
        while actual:
            if actual.simulacion.nombre == nombre_simulacion:
                return actual.simulacion
            actual = actual.siguiente

class Nodo_Nombre_Producto:
    def __init__(self, nombre_producto = None, siguiente = None):
        self.nombre_producto = nombre_producto
        self.siguiente = siguiente

class Lista_Nombres_Productos:
    def __init__(self):
        self.primer_nombre = None
    
    def insertar(self, nuevo_nombre):
        if self.primer_nombre is None:
            self.primer_nombre = Nodo_Nombre_Producto(nombre_producto=nuevo_nombre)
        else:
            nombre_actual = self.primer_nombre
            while nombre_actual.siguiente:
                nombre_actual = nombre_actual.siguiente
            nombre_actual.siguiente = Nodo_Nombre_Producto(nombre_producto=nuevo_nombre)
    
    def ensamblar_productos(self, lista_maquinas, lista_no_encontrados, frame_scroll, nombre_simulacion):
        root_salidasimulacion = "<SalidaSimulacion>"
        root_salidasimulacion += f"\n\t<Nombre>{nombre_simulacion}</Nombre>"
        root_salidasimulacion += "\n\t<ListadoProductos>"

        html_simulacion = '''<!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">'''
        html_simulacion += f'\n<link rel="stylesheet" href="{nombre_simulacion}.css" type="text/css" />'
        html_simulacion += f'''\n    <title>Reporte HTML</title>
        </head>
        <body>
            <li style="float: left; padding-left: 3%; padding-right: 20px;"><span class="material-icons md-light md-100">precision_manufacturing</span></li>
            <h1>Reporte Simulación {nombre_simulacion}</h1>'''

        actual = self.primer_nombre
        while actual:
            producto_cargado = lista_maquinas.boolean_producto_cargado(actual.nombre_producto)
            if producto_cargado:
                producto_ensamblado = lista_maquinas.boolean_producto_ensamblado(actual.nombre_producto)
                if producto_ensamblado:
                    producto = lista_maquinas.obtener_producto(actual.nombre_producto)
                    Label(frame_scroll, text="Producto ensamblado: " + producto.nombre, font=("Consolas", 14), bg="white").pack()
                    Label(frame_scroll, text="Tiempo más óptimo de ensamblaje: " + str(producto.segundos_ensamblaje_total) + " segundos", font=("Consolas", 14, 'bold'), bg="white").pack()
                    Label(frame_scroll, text="Componentes ensamblados:", font=("Consolas", 14), bg="white").pack()
                    comandos = producto.listado_comandos.devolver_str_comandos()             
                    t_comandos = Text(frame_scroll, font=("Consolas", 14))
                    t_comandos.tag_configure("centrado", justify='center')
                    t_comandos.insert("1.0", comandos)
                    t_comandos.tag_add("centrado", "1.0")
                    t_comandos.config(bg="white", width=40, height=2, state='disabled')
                    t_comandos.pack()       
                    Label(frame_scroll, text="", font=("Consolas", 14), bg="white").pack()
                    producto_xml = producto.salida_xml()
                    root_salidasimulacion += producto_xml
                    num_lineas = lista_maquinas.cantidad_lineas(producto.nombre)
                    producto_html = producto.salida_html(num_lineas)
                    html_simulacion += producto_html
                else:
                    ensamblado = lista_maquinas.ensamblar_por_simulacion(actual.nombre_producto)
                    if ensamblado:
                        producto = lista_maquinas.obtener_producto(actual.nombre_producto)
                        Label(frame_scroll, text="Producto ensamblado: " + producto.nombre, font=("Consolas", 14), bg="white").pack()
                        Label(frame_scroll, text="Tiempo más óptimo de ensamblaje: " + str(producto.segundos_ensamblaje_total) + " segundos", font=("Consolas", 14, 'bold'), bg="white").pack()
                        Label(frame_scroll, text="Componentes ensamblados:", font=("Consolas", 14), bg="white").pack()
                        comandos = producto.listado_comandos.devolver_str_comandos()             
                        t_comandos = Text(frame_scroll, font=("Consolas", 14))
                        t_comandos.tag_configure("centrado", justify='center')
                        t_comandos.insert("1.0", comandos)
                        t_comandos.tag_add("centrado", "1.0")
                        t_comandos.config(bg="white", width=40, height=2, state='disabled')
                        t_comandos.pack()       
                        Label(frame_scroll, text="", font=("Consolas", 14), bg="white").pack()
                        producto_xml = producto.salida_xml()
                        root_salidasimulacion += producto_xml
                        num_lineas = lista_maquinas.cantidad_lineas(producto.nombre)
                        producto_html = producto.salida_html(num_lineas)
                        html_simulacion += producto_html
                    else:
                        print("Ocurrió un error, no se encontró " + producto.nombre + " para ensamblaje")
            else:
                lista_no_encontrados.insertar(actual.nombre_producto)
            actual = actual.siguiente

        root_salidasimulacion += "\n\t</ListadoProductos>"
        root_salidasimulacion += "\n</SalidaSimulacion>"

        html_simulacion += '''    <footer>
                <p>Elías Abraham Vasquez Soto - 201900131</p>
                <p>Proyecto 1 - Laboratorio Introducción a la Programación y Computación 2 E</p>        
                <img src="images/logo_usac.png" width="220" height="60"/>
            </footer>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
        </body>
        </html>'''

        css_simulacion = '''html {
            min-height: 100%;
            position: relative;
        }

        body {
            background-color:rgb(1, 11, 26);
            padding-top: 20px;
            margin-bottom: 150px;
        }

        /* ===== Iconos de Google ===== */
        /* Rules for sizing the icon. */
        .material-icons.md-24 { font-size: 24px; }
        .material-icons.md-30 { font-size: 30px; }
        .material-icons.md-100 { font-size: 100px; }
        /* Rules for using icons as black on a light background. */
        .material-icons.md-dark { color: rgba(0, 0, 0, 0.54); }
        .material-icons.md-dark.md-inactive { color: rgba(0, 0, 0, 0.26); }
        /* Rules for using icons as white on a dark background. */
        .material-icons.md-light { color: rgba(255, 255, 255, 1); }
        .material-icons.md-light.md-inactive { color: rgba(255, 255, 255, 0.3); }

        h1 {
            color: white;
            font-family: 'Lato', sans-serif;
            font-size: 75px;
        }

        .datos-reporte {
            background-color: rgb(255, 255, 255);
            padding-top: 20px;
            padding-bottom: 20px;
            padding-left: 50px;
            margin: 30px 100px 30px 100px;
        }

        .datos {
            font-family: 'Lato', sans-serif;
            font-size: 30px;
            padding-left: 20px;
        }

        .tabla-ensamblaje {
            overflow-x: scroll;
            padding-top: 20px;
            text-align: center;
            font-family: 'Lato', sans-serif;
            font-size: 20px;
            letter-spacing: 1px;
            width: 96%;
        }

        table {
            width: 100%;
            table-layout: fixed;
        }

        table td, th{    
            color: white;
            width: 200px;
        }

        table #tiempo {
            width: 100px;
        }

        #uno {
            background-color: rgb(61, 57, 48);
        }

        #dos {
            background-color: rgb(54, 1, 1);
        }

        footer {
            color: white;
            line-height: 10px;
            text-align: center;
            padding-top: 20px;
            padding-bottom: 5px;
            font-size: 15px;
            font-family: 'Lato', sans-serif;
            position: absolute;
            bottom: 0;
            width: 100%;
            background-image: url("images/footer.png");
        }'''

        reportes_generados = True

        try:
            root = ET.fromstring(root_salidasimulacion)
            tree_xml_salida = ET.ElementTree(element=root)
            tree_xml_salida.write(f"Salidas XML/{nombre_simulacion}.xml", encoding="utf-8", xml_declaration=True)
            print("--> El archivo de simulación XML se creo exitosamente.")
        except Exception as e:
            print(e)
            print("--> No pudo crearse el archivo XML.")
            reportes_generados = False
        try:
            reporte_html = open(f"Reportes HTML/{nombre_simulacion}.html", "w",encoding="utf8")
            reporte_html.write(html_simulacion)
            reporte_html.close()
            print("--> El reporte de simulación HTML se creo exitosamente.")
        except Exception as e:
            print(e)
            print("--> No pudo crearse el archivo HTML.")
            reportes_generados = False
        try:
            reporte_css = open(f"Reportes HTML/{nombre_simulacion}.css", "w",encoding="utf8")
            reporte_css.write(css_simulacion)
            reporte_css.close()
            print("--> El CSS del reporte de simulación se creo exitosamente.")
        except Exception as e:
            print(e)
            print("--> No pudo crearse el archivo CSS.")
            reportes_generados = False
        
        return reportes_generados
    
    def lb_productos_no_encontrados(self, frame_scroll):
        actual = self.primer_nombre
        while actual:
            Label(frame_scroll, text=actual.nombre_producto, font=("Consolas", 14), bg="white").pack()
            actual = actual.siguiente
    
# ========== ACCIONES AL ENSAMBLAR UN PRODUCTO ==========

class Accion:
    def __init__(self, segundo, linea, ensamblando, moviendose, componente, tipo_accion = "No hacer nada"):
        self.segundo = segundo
        self.linea = linea
        if ensamblando is True:
            self.tipo_accion = f"Ensamblando C{componente}"
        elif moviendose is True:
            self.tipo_accion = f"Moviendose a C{componente}"
        else:
            self.tipo_accion = tipo_accion

class Nodo_Accion:
    def __init__(self, accion = None, siguiente = None):
        self.accion = accion
        self.siguiente = siguiente
    
class Lista_Acciones:
    def __init__(self):
        self.primera_accion = None
    
    def insertar(self, nueva_accion):
        if self.primera_accion is None:
            self.primera_accion = Nodo_Accion(accion=nueva_accion)
        else:
            accion_actual = self.primera_accion
            while accion_actual.siguiente:
                accion_actual = accion_actual.siguiente
            accion_actual.siguiente = Nodo_Accion(accion=nueva_accion)
    
    def devolver_acciones(self, segundo):
        actual = self.primera_accion
        acciones = ""
        while actual:
            if actual.accion.segundo == segundo:
                if acciones == "":
                    acciones += actual.accion.tipo_accion
                else:
                    acciones += "$"
                    acciones += actual.accion.tipo_accion
            actual = actual.siguiente
        return (acciones.split("$"))
    
    def acciones_por_segundo_XML(self, segundo):
        actual = self.primera_accion
        lineas_ensamblaje = ""
        while actual:
            if actual.accion.segundo == segundo:
                lineas_ensamblaje += f'\n\t\t\t\t\t<LineaEnsamblaje NoLinea="{actual.accion.linea}">{actual.accion.tipo_accion}</LineaEnsamblaje>'
            actual = actual.siguiente
        return lineas_ensamblaje
    
    def acciones_por_segundo_HTML(self, segundo, id_fila):
        actual = self.primera_accion
        lineas_ensamblaje = f'''\n                <tr id="{id_fila}">
                    <th scope="row" id="tiempo">{segundo}</th>'''
        linea_actual = 1
        while actual:
            if actual.accion.segundo == segundo:
                if actual.accion.linea == linea_actual:
                    lineas_ensamblaje += f'\n                <td>{actual.accion.tipo_accion}</td>'
                    actual = self.primera_accion
                    linea_actual += 1
                    continue
            actual = actual.siguiente
        lineas_ensamblaje += '                </tr>'
        return lineas_ensamblaje