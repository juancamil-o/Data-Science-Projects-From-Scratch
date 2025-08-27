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
        transformar_datos_del_dia(
            dias_retro=1,
            json_path="datosDeHoy.json",
            out_dir="s3://proyecto-secop/processed/",   # <-- S3
            out_format="parquet",                   # parquet recomendado
        )
