""" Processo de Ingesta para camada Raw da API De Pagamento do Banco Central """

import json
import requests
import os
import dlt
from dlt.sources.rest_api import rest_api_source, rest_api_resources


# Local Modules and packages


from logs.logger import LoggerManager
from storages import minio_storage


# Configura os Logs da Ingesta
logger_manager = LoggerManager(name = f"{__file__}")
logger = logger_manager.get_logger()


base_url = "https://olinda.bcb.gov.br/olinda/servico/MPV_DadosAbertos/versao/v1/odata"

recursos = {
    "cartoes_trimestral": "Quantidadeetransacoesdecartoes(trimestre=@trimestre)?%40trimestre='1'", 
    "pagamentos_mensal": "MeiosdePagamentosMensalDA(AnoMes=@AnoMes)?%40AnoMes='2024-01'", 
    "meios_pagamentos_trimestral": "MeiosdePagamentosTrimestralDA(trimestre=@trimestre)?%40trimestre='1'"
}


# Vamos usar o DLT do python como motor de Extração da API, simplificando a lógica e agilizando o desenvolvimento


minio_client = minio_storage.get_minio_client()


def get_data_from_bacen(urll: str) -> dict:
    """ 
        Extrai dados da api do Bacen 
    
    """

    header = { 'Accept': 'application/json' }

    try:
        response = requests.get(urll, headers=header)
        response.raise_for_status
        return response.json()
    
    except Exception as e:
        logger.info(f"Error ao tentar obter dados da API: \n*urll: {urll}")




endpoint_cartoes = f"{base_url}/{recursos.get('cartoes_trimestral')}"
print(f"\n* urll: {endpoint_cartoes}")
response_data = get_data_from_bacen(endpoint_cartoes)

minio_storage.create_bucket_if_not_exists(minio_client, "raw")

minio_storage.upload_file_to_bucket(
    response_data,
    minio_client,
    "raw",
    "bacen/pagamentos/cartoes.json",
    
)

print(json.dumps(response_data.get('value')[0], indent=4, ensure_ascii=False))





  

        

    







