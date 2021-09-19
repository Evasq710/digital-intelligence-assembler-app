from tkinter import END

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

# ========== COMPONENTES EN LINEA ==========
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
    
    def eliminar_componentes_pendientes(self):
        if self.primer_componente:
            self.primer_componente = None

# ========== PRODUCTOS EN MÁQUINA ==========
class Producto:
    def __init__(self, nombre, listado_comandos):
        self.nombre = nombre
        self.listado_comandos = listado_comandos

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

# ========== COMANDOS EN PRODUCTO ==========
class Comando:
    def __init__(self, linea, componente, requiere_ensamblar = False, es_ultimo = False, ensamblando = False, nothing = False):
        self.linea = linea
        self.componente = componente
        self.requiere_ensamblar = requiere_ensamblar
        self.es_ultimo = es_ultimo
        self.ensamblando = ensamblando
        self.nothing = nothing

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

# ========== SIMULACIONES DE ENSAMBLAJE DE PRODUCTOS ==========
class Simulacion:
    def __init__(self, nombre, listado_nombres_productos):
        self.nombre = nombre
        self.listado_nombre_productos = listado_nombres_productos

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