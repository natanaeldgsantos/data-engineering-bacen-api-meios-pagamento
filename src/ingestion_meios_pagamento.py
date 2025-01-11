""" Processo de Ingesta para camada Raw da API De Pagamento do Banco Central """

import json
import requests
import os
import dlt
from dlt.sources.rest_api import rest_api_source, rest_api_resources
from datetime import datetime
import pytz

# Local Modules and packages
from logs.logger import LoggerManager
from storages import minio_storage


# Vamos sempre usar o timezone do Brasil, já que é a api do Bacen, vamos manter o mesmo critério
brazil_timezone = pytz.timezone('America/Sao_Paulo')
now_timestamp = datetime.now(brazil_timezone).strftime('%d_%m_%Y_%H_%M_%S')


# Configura os Logs da Ingesta
logger_manager = LoggerManager(name = f"{__file__}")
logger = logger_manager.get_logger()


base_url = "https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata"
ano_mes = '2024-01'
bucket_name = "bank-databr"


# Endpoints para Consumo
resources = [
    
    {
        "name": "cartoes_trimestral",
        "url": f"{base_url}/Quantidadeetransacoesdecartoes(trimestre=@trimestre)?%40trimestre='1'"
    },
    {
        "name": "pagamentos_mensal",
        "url": f"{base_url}/MeiosdePagamentosMensalDA(AnoMes=@AnoMes)?%40AnoMes='{ano_mes}'"
    },
    {
        "name": "meios_pagamentos_trimestral",
        "url": f"{base_url}/MeiosdePagamentosTrimestralDA(trimestre=@trimestre)?%40trimestre='1'"
    }
]
    

# Step 01: Criando o Bucket e as folders

minio_client = minio_storage.get_minio_client()
minio_storage.create_bucket_if_not_exists(minio_client, bucket_name)


def get_data_from_bacen(urll: str) -> dict:
    """ Extrai dados da api do Bacen """

    header = { 'Accept': 'application/json' }

    try:
        response = requests.get(urll, headers=header)
        response.raise_for_status
        return response.json()
    
    except Exception as e:
        logger.info(f"Error ao tentar obter dados da API: \n*urll: {urll}")


# Step 02: Recuperando e Gravando dados na Landing
for resource in resources:

    print(f"* Processando recurso: {resource.get('name')}")
    response_data = get_data_from_bacen(resource.get('url'))

    minio_storage.upload_file_to_bucket(
        response_data,
        minio_client,
        bucket_name,
        f"bacen/{resource.get('name')}/data_{now_timestamp}.json",
        
    )








  

        

    







