import pandas as np
from pulp import *
from pandas import DataFrame
from munkres import Munkres

ori=[]
des=[]
oferta={}
demanda={}
cotoE={}


def crearOri(ori):
    while (True):
        entr=input("dame el nombre del origen (si terminaste(y)):")
        if (entr=="y"):
            return ori
        ori.append(entr)

def creaoferta(ori,demanda):
    for i in range(len(ori)):
        var=int ( input("dame el valor de"+ori[i]+":"))
        demanda[ori[i]]= var
    return demanda
def costoEnvio(des,ori,cotoE):
    for i in range(len(ori)):
        cotoE[ori[i]]={}
        for j in range(len(des)):
            vat=int(input("dame el costo de envio de"+ori[i]+" a "+des[j]+":"))
            cotoE[ori[i]][des[j]]=vat
    return cotoE
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
        



