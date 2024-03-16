import pandas as np
from pulp import *
from pandas import DataFrame
from munkres import Munkres
import os
ori=[]
des=[]
oferta={}
demanda={}
cotoE={}
hungalo=[[]]
#funcion para generar los origenes y destinos para el metodo de trasporte 
def crearOri(ori,st):
    while (True):
        entr=input("dame el nombre del "+st+" (si terminaste(y)): ")
        if (entr=="y"):
            return ori
        ori.append(entr)
#funcion que nos genera una las ofertas y demandas de los origenes y destinos
def creaoferta(ori,demanda):
    for i in range(len(ori)):
        var=int ( input("dame el valor de "+ori[i]+": "))
        demanda[ori[i]]= var
    return demanda
#funcion que nos rellena la mastis de costo de trasporte
def costoEnvio(des,ori,cotoE):
    for i in range(len(ori)):
        cotoE[ori[i]]={}
        for j in range(len(des)):
            vat=int(input("dame el costo de envio de "+ori[i]+" a "+des[j]+": "))
            cotoE[ori[i]][des[j]]=vat
    return cotoE

#funcion que nos aplica el metodo de trasporte 
def transporte(destino,origen,costo_envio):
    prob = LpProblem('Transporte', LpMinimize)

    rutas = [(i,j) for i in origen for j in destino]
    cantidad = LpVariable.dicts('Cantidad de Envio',(origen,destino),0)
    prob += lpSum(cantidad[i][j]*costo_envio[i][j] for (i,j) in rutas)
    for j in destino:
        prob += lpSum(cantidad[i][j] for i in origen) == demanda[j]
    for i in origen:
        prob += lpSum(cantidad[i][j] for j in destino) <= oferta[i]
    ### Resolvemos e imprimimos el Status, si es Optimo, el problema tiene solución.
    prob.solve()
    print("Status:", LpStatus[prob.status])

    ### Imprimimos la solución
    for v in prob.variables():
        if v.varValue > 0:
            print(v.name, "=", v.varValue)
    print('El costo mínimo es:', value(prob.objective))
#funcion que aplica el metodo de asignacion(hungaro)
def aplicar_metodo_hungaro(cost_matrix):
    # Crear instancia del algoritmo de asignación óptima de Munkres
    m = Munkres()

    # Aplicar el algoritmo de asignación óptima en la matriz de costos
    asignacion = m.compute(cost_matrix)

    # Obtener las asignaciones óptimas y los costos totales
    asignacion_optima = []
    costo_total = 0

    for row, col in asignacion:
        costo = cost_matrix[row][col]
        asignacion_optima.append((row, col))
        costo_total += costo

    # Devolver las asignaciones óptimas y el costo total
    return asignacion_optima, costo_total

#metodo que para el menu que nos dan las obciones 
def menuP():
    print("-----------Menu----------")
    print("1) problema de trasporte")
    print("2) metodo hungaro")
    return int(input("que operacion quieres hacer: "))
#metodo que rellena la matris para el metodo de asignacion 
def damevalor(st):
    return int(input("dame el numero de "+st+": "))

def dameVal2(n,m,ma):
    for i in range(n):
        for j in range(m):
            ma[i][j]=int(input("valor "+i+" "+j+": "))
    return ma



#llamamos los metodos 
n=1

while (n>0):
    n=menuP()
    os.system("cls")
    #metodo de trasporte
    if (n==1):
        ori=crearOri(ori,"origen")
        des=crearOri(des,"destino")
        oferta=creaoferta(ori,oferta)
        demanda=creaoferta(des,demanda)
        cotoE=costoEnvio(des,ori,cotoE)
        transporte(des,ori,cotoE)
    #metodo hungaro 
    elif(n==2):
        N=damevalor("filas")
        M=damevalor("columna")
        hungalo=[[0]*M for k in range(N) ]
        hungalo=dameVal2(N,M,hungalo)
        asignacion_optima, costo_total = aplicar_metodo_hungaro(hungalo)
        os.system("cls")
        print("Asignación óptima:", asignacion_optima)
        print("Costo total:", costo_total)
    ori=[]
    des=[]
    oferta={}
    demanda={}
    cotoE={}
    hungalo=[[]]


       
    
    



