from setuptools import setup, find_packages

setup(
    name="data_engineering_bacen_api_meios_pagamento",
    version="0.0.1",
    author="Natanael Domingos",
    author_email="",
    description="Projeto de Porftólio integração e ingestão de dados da API de Pagamentos do Banco Central",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/natanaeldgsantos/data-engineering-bacen-api-meios-pagamento",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=['ingestion_meios_pagamento'],
    include_packages_data=True,
    python_requires=">=3.10.9",
    entry_points={
        "console_scripts":[
            "run_workflow=main:execute_workflow"
        ]
    }
)