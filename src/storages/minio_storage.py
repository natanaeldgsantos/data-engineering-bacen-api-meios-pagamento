
import os
from minio import Minio
from io import BytesIO


# Local Modules and packages
from logs.logger import LoggerManager

logger_manager = LoggerManager(name = f"{__file__}")
logger = logger_manager.get_logger()


def get_minio_client() -> Minio:
    """ Cria Client Minio """

    return Minio(
        endpoint= os.environ.get('MINIO_ENDPOINT'),
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
        data: dict,
        minio_client: Minio, 
        bucket_name: str,
        # source_file_path_in_origin: str, 
        destination_file_path_in_bucket: str
):
    
    """ Verifica arquivo informado e realiza upload para buckload de destino """

    logger.info(f'Carregando arquivo: \n\t* bucket: {bucket_name} \n\t* destionation: {destination_file_path_in_bucket},')

    data_bytes = BytesIO(str(data).encode('utf-8'))

    minio_client.put_object(
        data = data_bytes,

        # Nome do Bucket
        bucket_name = bucket_name,

        # # Caminho do Arquivo na Origem
        # file_path = source_file_path_in_origin,

        # Destino do arquivo no Storage e nome final
        object_name = destination_file_path_in_bucket,

        length=data_bytes.getbuffer().nbytes,
        content_type="application/json"

    )
    logger.info("Carga de Dados realizada com Sucesso")