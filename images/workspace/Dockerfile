FROM jupyter/pyspark-notebook

# Instalando dependências Delta para PySpark

RUN pip install delta-spark==3.3.0


# Bibliotecas de integração com o Data Storage MinIO, que usa formato like
# AWS S3, usaremos o s3fs para configurar a sessão pyspark com o storage.
RUN pip install s3fs boto3

# (Opcional) Seguindo minha preferência, disponibiliza temas de melhor design 
# para o Jupyter Lab (para mim o melhor é o Macchiato)
RUN pip install catppuccin-jupyterlab


# Configurar o PySpark para usar Delta Lake
ENV PYSPARK_SUBMIT_ARGS="--packages io.delta:delta-core_2.12:3.3.0 \
    --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
    --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog pyspark-shell"