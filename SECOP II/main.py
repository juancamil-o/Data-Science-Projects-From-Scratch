from queries import *
import requests
from extract import extraerContratosDelDia
from transformacion import transformar_datos_del_dia
import os
if __name__ == '__main__':
    #extract()
    #queryTopDiezEntidadesQueMasContrataron()
    #queryTopDiezSectoresQueMasContrataron()
    #queryPorcentajePorTipoDeContrato()

    numeroDiasAtras = 1
    if extraerContratosDelDia(numeroDiasAtras) > 0:
        print(transformar_datos_del_dia(numeroDiasAtras))
    queryall()
