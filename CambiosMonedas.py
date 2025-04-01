#Importar libreria GUI
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook
import Util
import csv

iconos = ["./iconos/Grafica.png", "./iconos/Datos.png"]
textos = ["Grafica Fecha vs Cambios", "Calcular estadisticas"]

def ObtenerMonedas():
    monedas = set() #Conjunto vacio
    # Abrir el archivo CSV
    with open("./datos/Cambios Monedas.csv") as archivo:
        lectorArchivo = csv.reader(archivo)
        next(lectorArchivo) #Omitir linea de encabezados
        for linea in lectorArchivo:
            moneda, strfecha, strcambio = linea
            monedas.add(moneda)
        
    return list(monedas)
                

def mostrarGrafica():
    messagebox.showinfo("", "Hizo click en GRAFICA")

def mostrarEstadisticas():
    messagebox.showinfo("", "Hizo click en ESTADISTICAS")

ventana = Tk()
ventana.title("Cambio de Monedas")
ventana.geometry("400x300")

botones = Util.agregarBarra(ventana, iconos, textos)
botones[0].configure(command=mostrarGrafica)
botones[1].configure(command=mostrarEstadisticas)

FrmMoneda = Frame(ventana)
FrmMoneda.pack(side=TOP, fill=X)

Util.agregarEtiqueta(FrmMoneda, "Moneda", 0, 0)
monedas = ObtenerMonedas()
Util.agregarLista(FrmMoneda, monedas, 0, 1)

nb = Notebook(ventana)
nb.pack(expand=YES, fill=BOTH)
pestañas = ["Graficas", "Estadisticas"]
for p in pestañas:
    frm = Frame(nb)
    nb.add(frm, text=p)


ventana.mainloop()
