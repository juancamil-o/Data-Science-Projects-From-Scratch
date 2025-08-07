from queries import *
import requests
from extract import extraerContratosDelDia
from transformacion import transformarDatosDelDia
    
if __name__ == '__main__':
    #extract()
    #queryTopDiezEntidadesQueMasContrataron()
    #queryTopDiezSectoresQueMasContrataron()
    #queryPorcentajePorTipoDeContrato()
    if extraerContratosDelDia() > 0:
        print(transformarDatosDelDia())

