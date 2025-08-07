from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import DeltaTable
import os
from datetime import date, timedelta


json_path = os.getenv("JSON_PATH", "datosDeHoy.json")
delta_path = os.getenv("DELTA_PATH", "Silver")

def transformarDatosDelDia():
    # Inicializar Spark
    spark = (
    SparkSession.builder.appName("SECOP II")
    .config("spark.jars.packages", "io.delta:delta-spark_2.12:3.0.0,org.apache.hadoop:hadoop-aws:3.3.4")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
    .getOrCreate()
)


    # Fecha objetivo = AYER
    fecha_objetivo = (date.today() - timedelta(days=1)).isoformat()  # '2025-08-05'

    # Validar archivo
    if not os.path.exists(json_path) or os.path.getsize(json_path) == 0:
        raise FileNotFoundError(f"El archivo {json_path} no existe o está vacío.")

    try:
        # Leer JSON
        df = spark.read.option("multiLine", "false").json(json_path)
        print(f"✅ Datos cargados en Spark: {df.count()} registros")
        print("Esquema detectado:")
        df.printSchema()

        # Validar columnas
        columnas_necesarias = [
            "nombre_entidad","nit_entidad","departamento","orden","sector","rama",
            "entidad_centralizada","tipo_de_contrato","modalidad_de_contratacion",
            "justificacion_modalidad_de","fecha_de_firma","valor_del_contrato",
            "documento_proveedor","urlproceso"
        ]
        columnas_faltantes = [c for c in columnas_necesarias if c not in df.columns]
        if columnas_faltantes:
            print(f"⚠ Columnas faltantes: {columnas_faltantes}")

        # Transformación
        df_transformado = (
            df.withColumn("nit_entidad", F.col("nit_entidad").cast("bigint"))
              .withColumn("documento_proveedor", F.col("documento_proveedor").cast("bigint"))
              .withColumn("valor_del_contrato", F.col("valor_del_contrato").cast("bigint"))
              .withColumn("fecha_firma_dia", F.to_date("fecha_de_firma"))  # solo la fecha
              .select([c for c in columnas_necesarias if c in df.columns] + ["fecha_firma_dia"])
        )

        # Guardar con particionado y replaceWhere
        df_transformado.write \
            .format("delta") \
            .mode("overwrite") \
            .option("replaceWhere", f"fecha_firma_dia = '{fecha_objetivo}'") \
            .partitionBy("fecha_firma_dia") \
            .save(delta_path)

        print(f"✅ Datos del {fecha_objetivo} guardados en Delta en partición correspondiente.")

    except Exception as e:
        print(f"❌ Error al transformar datos: {e}")
        raise
