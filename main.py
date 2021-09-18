from xml.etree import ElementTree as ET
from tkinter import *
from tkinter import filedialog
from clases import *

class Interfaz:
    def __init__(self, ventana):
        self.window = ventana
        self.window.title('Digital Intelligence Assembler')        
        self.window.state('zoomed')

        title = Label(self.window, text="Digital Intelligence Assembler", font=("Consolas", 60, "bold"), bg="white")
        title.place(x=100, y=70)
        
        frame_btn = Frame(self.window, bg="white")
        frame_btn.place(x=75, y=200)

        self.cargar_maquina_btn = Button(frame_btn, text="Cargar Archivo - Máquina", font=("Consolas", 15), bg="light sea green", command = lambda:[])
        self.cargar_maquina_btn.grid(row=0, column=0, padx=20)

        self.cargar_simulacion_btn = Button(frame_btn, text="Cargar Archivo - Simulación", font=("Consolas", 15), bg="light sea green", command = lambda:[])
        self.cargar_simulacion_btn.grid(row=0, column=1, padx=20)

        self.ensamblar_btn = Button(frame_btn, text="Ensamblar productos", font=("Consolas", 15), bg="light sea green", command = lambda:[])
        self.ensamblar_btn.grid(row=0, column=2, padx=20)

        self.reporte_cola_btn = Button(frame_btn, text="Reporte de cola de secuencia", font=("Consolas", 15), bg="light sea green", command = lambda:[])
        self.reporte_cola_btn.grid(row=0, column=3, padx=20)

        self.ayuda_btn = Button(frame_btn, text="Ayuda", font=("Consolas", 15), bg="light sea green", command = lambda:[])
        self.ayuda_btn.grid(row=0, column=4, padx=20)

if __name__ == '__main__':
    ventana = Tk()
    app = Interfaz(ventana)
    ventana.mainloop()