#Importar libreria GUI
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook
import Util
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from functools import reduce
import math

iconos = ["./iconos/Grafica.png", "./iconos/Datos.png"]
textos = ["Grafica Fecha vs Cambios", "Calcular estadisticas"]

def ObtenerMonedas():
    #CODIGO FUNCIONAL
    #Abrir el archivo csv
    with open("./datos/Cambios Monedas.csv") as archivo:
        lectorArchivo = csv.reader(archivo)
        next(lectorArchivo)
        return sorted(set(map(lambda linea: linea[0], lectorArchivo)))
    

    #NO FUNCIONAL
    monedas = set() #Conjunto vacio
    # Abrir el archivo CSV
    with open("./datos/Cambios Monedas.csv") as archivo:
        lectorArchivo = csv.reader(archivo)
        next(lectorArchivo) #Omitir linea de encabezados
        for linea in lectorArchivo:
            moneda, strfecha, strcambio = linea
            monedas.add(moneda)
        
    return list(monedas)

def obtenerDatos():
    with open("./datos/Cambios Monedas.csv") as archivo:
        lectorArchivo = csv.reader(archivo)
        next(lectorArchivo) #Omitir linea de encabezados
        return [
            {
                "moneda": linea[0], "fecha" : datetime.strptime(linea[1], "%d/%m/%Y"), "cambio": float(linea[2])
            }
            for linea in lectorArchivo
        ]
    
def filtrarDatos(datos, moneda, desde, hasta):
    return list(filter(lambda dato: dato["moneda"]==moneda and desde<=dato["fecha"] and dato["fecha"]<=hasta ,datos))

def extraerDatos(datos):
    datosOrdenados = sorted(datos, key=lambda dato: dato["fecha"])
    fechas = list(map(lambda dato: dato["fecha"], datosOrdenados))
    cambios = list(map(lambda dato: dato["cambio"], datosOrdenados))
    return fechas, cambios

def mostrarGrafica():
    if cmbMoneda.current() >= 0:
        #Obtener datos de entrada
        moneda = monedas[cmbMoneda.current()]
        desde = datetime.strptime(cldDesde.get(), "%d/%m/%Y")
        hasta = datetime.strptime(cldHasta.get(), "%d/%m/%Y")

        datos = obtenerDatos()
        datosfiltrados = filtrarDatos(datos, moneda, desde, hasta)
        fechas, cambios = extraerDatos(datosfiltrados)
        print(datosfiltrados, flush=True)

        #Graficar
        plt.title("Cambios Moneda")
        plt.clf() #Limpiar la grafica
        plt.ylabel("Valor del cambio")
        plt.xlabel("Fecha")

        plt.plot(fechas, cambios, label=f"Cambio de {moneda}")
        plt.grid()
        plt.legend()

        # Guardar la gráfica como imagen
        nombreArchivo = "graficacambioMoneda.png"
        plt.savefig(nombreArchivo)

        # Cargar la grafica
        imgGrafica = PhotoImage(file=nombreArchivo)

        # Crear Label para mostrar la gráfica
        lblGrafica = Label(paneles[0])
        lblGrafica.config(image=imgGrafica)
        lblGrafica.image=imgGrafica

        lblGrafica.place(x=0, y=0)

        # Redimensionar la ventana para que se ajuste a la imagen
        ventana.minsize(imgGrafica.width(), imgGrafica.height()+100)
        nb.select(0)

def extraerCambios(datos):
    cambios = list(map(lambda dato: dato["cambio"], datos))
    return cambios

# Calculos estadisticos
def calcularPromedio(cambios):
    #CODIGO FUNCIONAL
    return reduce(lambda cambio, suma: cambio + suma, cambios) / len(cambios) if cambios else 0

    #FUNCIONAL PYTHONICAMENTE
    #return sum(cambios) / len(cambios) if cambios else 0

    #No funcional
    suma = 0
    if len(cambios) == 0:
        for cambio in cambios:
            suma += cambio
    return suma / len(cambios)

def calcularDesviacionEstandar(cambios):
    #CODIGO FUNCIONAL
    promedio = calcularPromedio(cambios)
    return math.sqrt(reduce(lambda suma, cambio: suma + (cambio-promedio)**2, cambios, 0) / len(cambios) if cambios else 0)

    #No funcional
    desviacion = 0
    if cambios:
        promedio = calcularPromedio(cambios)
        suma = 0
        for cambio in cambios:
            suma += (cambio-promedio)**2
        desviacion = math.sqrt(suma / len(cambios))
    return desviacion

def calcularMaximo(cambios):
#CODIGO FUNCIONAL
    return reduce(lambda maximo, cambio: cambio if cambio > maximo else maximo, cambios) if cambios else 0

    #CODIGO FUNCIONAL
    return max(cambios) if cambios else 0

    #No funcional
    maximo = 0
    if cambios:
        for cambio in cambios:
            if cambio > maximo:
                maximo = cambio
    return maximo

def calcularMinimo(cambios):
    #CODIGO FUNCIONAL
    return reduce(lambda minimo, cambio: cambio if cambio < minimo else minimo, cambios) if cambios else 0

    #CODIGO FUNCIONAL
    return min(cambios) if cambios else 0

    #No funcional
    minimo = 0
    if cambios:
        for cambio in cambios:
            if cambio < minimo:
                minimo = cambio
    return minimo

def calcularModa(cambios):
    #Hallar la frecuencia de cada cambio
    frecuencias = reduce(lambda diccionarios, cambio: {**diccionarios, cambio: diccionarios.get(cambio, 0) + 1}, cambios, {})
    #hallar la mayor frecuencia
    maxFrecuencia = reduce(lambda maximo, frecuencia: frecuencia if frecuencia[1] > maximo[1] else maximo, frecuencias.items())
    return maxFrecuencia[0] if maxFrecuencia[1] > 1 else None

def calcularEstadisticas(moneda, desde, hasta):
    # Obtener datos de entrada
        datos = obtenerDatos()
        datosfiltrados = filtrarDatos(datos, moneda, desde, hasta)
        cambios = extraerCambios(datosfiltrados)

        return {
            "Promedio": calcularPromedio(cambios),
            "Desviacion": calcularDesviacionEstandar(cambios),
            "Maximo": calcularMaximo(cambios),
            "Minimo": calcularMinimo(cambios),
            "Moda": calcularModa(cambios) if calcularModa(cambios) else "No hay moda"
        }

def mostrarEstadisticas():
    if cmbMoneda.current() >= 0:
        # Obtener datos de entrada
        moneda = monedas[cmbMoneda.current()]
        desde = datetime.strptime(cldDesde.get(), "%d/%m/%Y")
        hasta = datetime.strptime(cldHasta.get(), "%d/%m/%Y")

        estadisticas = calcularEstadisticas(moneda, desde, hasta)
        for i,(clave,valor) in enumerate(estadisticas.items()):
            Util.agregarEtiqueta(paneles[1], clave, i, 0)
            Util.agregarEtiqueta(paneles[1], valor, i, 1)


        #Seleccionar la pestaña de estadisticas
        nb.select(1)

        
        #NO FUNCIONAL
        ## Mostrar Promedio
        #Util.agregarEtiqueta(paneles[1], "Promedio", 0, 0)
        #Util.agregarEtiqueta(paneles[1], calcularPromedio(cambios), 0, 1)
        ## Mostrar Desviacion Estandar
        #Util.agregarEtiqueta(paneles[1], "Desviacion Estandar", 1, 0)
        #Util.agregarEtiqueta(paneles[1], calcularDesviacionEstandar(cambios), 1, 1)
        ## Mostrar Maximo
        #Util.agregarEtiqueta(paneles[1], "Maximo", 2, 0)
        #Util.agregarEtiqueta(paneles[1], calcularMaximo(cambios), 2, 1)
        ## Mostrar Minimo
        #Util.agregarEtiqueta(paneles[1], "Minimo", 3, 0)
        #Util.agregarEtiqueta(paneles[1], calcularMinimo(cambios), 3, 1)
        ## Mostrar Moda
        #moda = calcularModa(cambios)
        #Util.agregarEtiqueta(paneles[1], "Moda", 4, 0)
        #Util.agregarEtiqueta(paneles[1], moda if moda else "No hay moda", 4, 1)

        

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
cmbMoneda = Util.agregarLista(FrmMoneda, monedas, 0, 1)

cldDesde = Util.agregarCalendario(FrmMoneda, 0, 2)
cldHasta = Util.agregarCalendario(FrmMoneda, 0, 3)

nb = Notebook(ventana)
nb.pack(expand=YES, fill=BOTH)
pestañas = ["Graficas", "Estadisticas"]
paneles = []
for p in pestañas:
    frm = Frame(nb)
    paneles.append(frm)
    nb.add(frm, text=p)


ventana.mainloop()
