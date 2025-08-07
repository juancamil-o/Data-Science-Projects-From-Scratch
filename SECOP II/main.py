from queries import *
import requests
from extract import extraerContratosDelDia
from transformacion import transformarDatosDelDia


def make_request(params):
    BASE_URL = "https://www.datos.gov.co/resource/jbjy-vk9h.json"   

    return requests.get(BASE_URL, params=params)
    
if __name__ == '__main__':
    #extract()
    #queryTopDiezEntidadesQueMasContrataron()
    #queryTopDiezSectoresQueMasContrataron()
    #queryPorcentajePorTipoDeContrato()
    if extraerContratosDelDia() > 0:
        print(transformarDatosDelDia())

