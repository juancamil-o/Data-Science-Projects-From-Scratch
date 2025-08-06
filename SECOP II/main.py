from queries import *
import requests
import json
from transformacion import transformarDatosDelDia


def contratos_del_dia(dia):
    response = make_request(queryFechaDeFirmaDia(dia))
    if response.status_code == 200:
        data = response.json()
        print(f'Número de contratos el día {dia}: {len(data)}')

        # Guardar como NDJSON (uno por línea)
        with open("datosDeHoy.json", "w", encoding="utf-8") as f:
            for record in data:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return len(data)
    else:
        return 0

def contratos_del_mes():
    response = make_request(queryFechaDeFirmaMesPasado())
    if response.status_code == 200:
        print(f'Número de contratos firmados el mes pasado :' + str(len(response.json())))
        with open("datosDelMesPasado.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        return len(response.json())
    else:
        return 0

def tranformacionDeDatos():
    pass

def contratos_individuales():
    NIT = "1007722129" 

    params = {"documento_proveedor": NIT}

    response = make_request(params)

    if response.status_code == 200:
        contratos = response.json()
        totalContratos = 0
        #print(contratos[0])  # Lista de contratos en JSON
        for contrato in contratos:
            totalContratos += int(contrato['valor_del_contrato'])
        representante_legal = contratos[0]['nombre_representante_legal']
        valor_formateado = "${:,.0f}".format(int(totalContratos))
        print(f"El contratista tiene contratos por un valor de {valor_formateado}.")
        print(contratos)
        valor_formateado = "${:,.0f}".format(int(totalContratos))
        return f"<h1>Bienvenido a mi aplicación Flask</h1><p>El contratista {representante_legal} tiene contratos por un valor de {valor_formateado}.</p>"
    else:
        print(f"Error: {response.status_code}")

    #return "<h1>Bienvenido a mi aplicación Flask</h1><p>Esta es una app básica.</p>"

#Contratos asociados a una institución en particular
def contratos_entidad():
    params = {
         "nombre_entidad": "DANE - DIRECCION TERRITORIAL NORTE",
         "$limit": 5000,  # Ajusta el límite según lo necesario
         "$offset": 0 }

    response = make_request(params)

    if response.status_code == 200:
        contratos = response.json()
        totalContratos = 0
        #print(contratos[0])  # Lista de contratos en JSON
    for contrato in contratos:
        totalContratos += int(contrato['valor_del_contrato'])
    valor_formateado = "${:,.0f}".format(int(totalContratos))
    return f"<h1>Bienvenido a mi aplicación Flask</h1><p>La entidad {params['nombre_entidad']} tiene {len(contratos)} contratos activos por valor de {valor_formateado}.</p>"

#Entidades únicas por departamento o ciudad
def home():
    response = make_request(queryEntidadesXDepartamento('Distrito Capital de Bogotá', 'Nacional'))
    if response.status_code == 200:
        entidadesNoNal = response.json()
        entidades = 'Entidades = '
        print(len(entidadesNoNal))
    else:
        print(f"Error: {response.status_code}, {response.text}")
    return f"<h1>Bienvenido a mi aplicación Flask</h1><p>El contratista "


def make_request(params):
    BASE_URL = "https://www.datos.gov.co/resource/jbjy-vk9h.json"   

    return requests.get(BASE_URL, params=params)
    

def extract():
    numeroRegistros = contratos_del_dia(ayer())
    if numeroRegistros > 0:
        print(transformarDatosDelDia())
    

if __name__ == '__main__':
    #extract()
    #queryTopDiezEntidadesQueMasContrataron()
    #queryTopDiezSectoresQueMasContrataron()
    #queryPorcentajePorTipoDeContrato()
    queryNumeroDeRegistros()
