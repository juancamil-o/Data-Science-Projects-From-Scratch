from datetime import date, datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import duckdb
import os 


con = duckdb.connect()
DEFAULT_DELTA_PATH = "Silver"  # o "Silver" si esa es la actual

def ayer():
    ayer = datetime.now() - timedelta(days=1)
    return ayer.strftime("%Y-%m-%d")



def hoy():
    return str(date.today())



def primer_y_ultimo_dia_mes_pasado():
    hoy = date.today()
    # Primer día del mes pasado
    primer_dia = (hoy.replace(day=1) - relativedelta(months=1))
    # Último día del mes pasado = primer día de este mes - 1 día
    ultimo_dia = hoy.replace(day=1) - timedelta(days=1)
    return primer_dia, ultimo_dia



def queryEntidadesXCiudad(ciudad):
    return {
        "$select": "distinct nombre_entidad",
        "$where": f"ciudad='{ciudad}' AND orden != 'Nacional'"
    }



def queryEntidadesXDepartamento(departamento, orden):
    return {
    "$select": "distinct nombre_entidad",
    "$where": f"departamento='{departamento}' AND orden != '{orden}'"
    }



def queryFechaDeFirmaDia(dia):
    return {
        "$select": "*",
        "$where": f"fecha_de_firma between '{dia}T00:00:00' and '{dia}T23:59:59'",
        "$limit": 500000
    }


def queryFechaDeFirmaMesPasado():
    primer_dia, ultimo_dia = primer_y_ultimo_dia_mes_pasado()
    return {
        "$select": "*",
        "$where": f"fecha_de_firma between '{primer_dia}T00:00:00' and '{ultimo_dia}T23:59:59'",
         "$limit": 500000
    }


#Load 

def queryTopDiezEntidadesQueMasContrataron():
    con = duckdb.connect()
    df = con.execute("""
        SELECT nombre_entidad, SUM(valor_del_contrato) AS total_contratado
        FROM delta_scan('{DELTA_PATH}')
        GROUP BY nombre_entidad
        ORDER BY total_contratado DESC
        LIMIT 10;
    """).fetchdf()
    print(df)

def queryTopDiezSectoresQueMasContrataron():
    df = con.execute("""
        SELECT sector,
               SUM(valor_del_contrato) AS total_contratado
        FROM delta_scan('{DELTA_PATH}')
        GROUP BY sector
        ORDER BY total_contratado DESC
        LIMIT 10;
    """).fetchdf()
    print(df)


def queryPorcentajePorTipoDeContrato():
    con = duckdb.connect()
    df = con.execute("""
        SELECT tipo_de_contrato,
               SUM(valor_del_contrato) AS total_contratado,
               ROUND(
                   100.0 * SUM(valor_del_contrato) / 
                   (SELECT SUM(valor_del_contrato) FROM 'Silver/part-*.snappy.parquet'),
                   2
               ) AS porcentaje
        FROM 'Silver/part-*.snappy.parquet'
        GROUP BY tipo_de_contrato
        ORDER BY total_contratado DESC;
    """).fetchdf()
    print(df)

def querySectoresUnicos():
    con = duckdb.connect()
    df = con.execute("""
        SELECT DISTINCT sector
        FROM 'Silver/part-*.snappy.parquet'
        WHERE sector IS NOT NULL
        ORDER BY sector;
    """).fetchdf()
    print(df)


def queryNumeroDeRegistros():
    con = duckdb.connect()
    df = con.execute("""
        SELECT COUNT(*) AS total_registros
        FROM 'Silver/fecha_firma_dia=2025-08-05/part-*.snappy.parquet';
    """).fetchdf()
    print(df)

def queryall():
    df = con.execute("""SELECT * FROM read_parquet('datos/*.parquet');
""").fetchdf()
    print(df)





