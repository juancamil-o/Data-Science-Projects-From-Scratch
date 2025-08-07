from main import make_request
from queries import *
import json
import os


json_path = os.getenv("JSON_PATH", "datosDeHoy.json")

def extraerContratosDelDia(dia):
    response = make_request(queryFechaDeFirmaDia(dia))
    if response.status_code == 200:
        data = response.json()
        print(f'Número de contratos en la fecha {dia}: {len(data)}')

        # Guardar como NDJSON (uno por línea)
        with open(json_path, "w", encoding="utf-8") as f:
            for record in data:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return len(data)
    else:
        return 0


def extraerContratosDelMes():
    response = make_request(queryFechaDeFirmaMesPasado())
    if response.status_code == 200:
        print(f'Número de contratos firmados el mes pasado :' + str(len(response.json())))
        with open("datosDelMesPasado.json", "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        return len(response.json())
    else:
        return 0
    

def extraerContratoIndividual(NIT):
    params = {"documento_proveedor": NIT}
    response = make_request(params)

    if response.status_code == 200:
        contratos = response.json()
        return contratos     
    else:
        return 0
