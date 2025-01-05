
import os
from minio import Minio


# Local Modules and packages
from logs.logger import LoggerManager

logger_manager = LoggerManager(name = f"{__file__}")
logger = logger_manager.get_logger()

def get_minio_client() -> Minio:
    """ Cria Client Minio """

    return Minio(
        endpoint= os.environ.get('MINIO_USER'),
        access_key= os.environ.get('MINIO_USER'),
        secret_key= os.environ.get('MINIO_PASSWORD'),
        secure=False
    )


def create_bucket_if_not_exists(minio_client: Minio, bucket_name: str) -> None:
    """ 
        Verifica se o Bucket já existe, caso não cria novo 
        
        Args:
            bucket_name (str): Nome do Bucket

    """

    bucket_exists = minio_client.bucket_exists(bucket_name)
    
    if not bucket_exists:
        logger.info(f"Criando novo Bucket: {bucket_name}")
        minio_client.make_bucket(bucket_name)
    else:
        logger.info(f"Bucket [{bucket_name}] já existe")


def upload_file_to_bucket(
        minio_client: Minio, 
        bucket_name: str,
        source_file_path_in_origin: str, 
        destination_file_path_in_bucket: str
    ):
    
    """ Verifica arquivo informado e realiza upload para buckload de destino """

    minio_client.fput_object(

        # Nome do Bucket
        bucket_name="bacen", 

        # Caminho do Arquivo na Origem
        file_path="C:\\projetos\\banco_central_estatistica_meios_pagamento\\src\\utils\\customers.txt",

        # Destino do arquivo no Storage e nome final
        object_name="pagamentos/raw/customers_updated.txt"

)