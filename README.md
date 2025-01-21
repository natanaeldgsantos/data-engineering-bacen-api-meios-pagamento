## **Pipeline de Dados e Análise dos Meios de Pagamento no Brasil**

**Será que a mudança no monitoramento do PIX vai reduzir a demanda?**

Olá, me chamo Natanael Domingos seja bem vindo a mais um projeto de portólio em Engenharia de Dados.

A alguns dias me deparei com a API de Pagamentos do Banco Central do Brasil, que retornar informações e estatísticaqs sobre:
- Diferentes **tipos** de pagamentos no país.
- A **quantidade** de transações realizadas por cada tipo.
- O **total de valores** movimentados consolidados por tipo, mês ou trimestre.

Segue a documentação de referência desta API:
- https://dadosabertos.bcb.gov.br/dataset/estatisticas-meios-pagamentos


Decide utilizar este recurso como fontes de dados para este projeto, a minha intenção é desenvolver um novo **pipeline de dados** e depois realizar algumas análises. 

Acredito que este será um bom exemplo para ilustrar situações do dia a dia de um Engenheiro de dados. 

Neste projeto vamos construir um ambiente distribuido do zero utilizando:

- Docker para levantar o ambiente local, algo que seja reproduzivel.
- MinIO, como nosso storage ou Delta Lakehouse
- PySpark para processamento dos dados
- Python e diversas bibliotecas open source para desenvolvimento.

Com isso, podemos criar um ambiente prático, open-source e  reutilizável para um projeto que aborda um assunto atual e relevante para a economia brasileira.

Por motivo de simplicidade e questão de custos, optei por utilizar um ambiente open-source, todavia pretendo explorar recursos também comerciais, como de Cloud, em outras versões deste mesmo projeto, no futuro. Aguarde!

### **Objetivo Principal**
Desenvolver um pipeline de dados automatizado para:
01. Consumir informações da API de Estatísticas de Meios de Pagamento do Banco Central.
02. Armazenar os dados em um Data Lake.
03. Processar, Normalizar e Disponbilizar os dados em um formato otimizado dentro de uma camada de consumo do nosso Data Lake com arquitetura Medalhão.
04. Realizar o Consumo destas informações, já normalizadas e especializadas para o Négócio, realizando análises em um Data Warehouse ou SQL Engine.
05. Explorar o Conjunto de dados, realizando análises e criando Dashboards para tomada de decisão.

Enfim, como objetivo final pretendo identificar tendências no uso de diferentes meios de pagamento, como Pix, TED, boletos e cartões.

### Pipeline de Dados para nosso Projeto

![pipeline](./docs/img/pipeline.svg "Data Pipeline_ BCB - API Estatísticas de Pagamento")

---

### **Etapas do Projeto**

#### **Configuração do Ambiente Local de Desenvolvimento**

Para este projeto vou usar uma imagem personalizada do Docker, feita sobre medida para ser a mais prática e leve possível para subir um ambiente com:
- Spark (PySpark) versão 3.5.*
- Delta Lake
- Bibliotecas de integração com AWS e storage como MinIO
- Jupyter Lab, assim como alguns templates de melhor design para trabalhar com Jupyter.

Para não deixar este projeto muito longo, estou separando o local desta imagem em outro projeto no meu reposítorio, visto que esta imagem
poderá ser utilizada para qualquer outro projeto que precise de Spark e um Data Lakehouse.

#### **01. Coleta e Armazenamento dos Dados**

Neste etapa vamos:

- Acessar a API do BCB para coletar dados mensais e trimestrais contendo Estatísticas sobre Meios de Pagamentos no Brasil.
- Realizar a Ingestão da fonte de dados. 
  - Aqui vou aproveitar para usar **Python DLT**, mas poderia ser uma ferramenta de ingestão como **Nifi** ou **Airbyte**, ou algo proprietário como **Data Factory** ou **Glue**.
- Salvar os dados coletados em seu formato original (JSON) dentro da folder Landing no nosso Data Lake:

Referência: https://min.io/

##### **Exemplo de Estrutura de Diretórios na folder Landing do nosso Data Lake com MinIO**
```
├── /bank-databr/
    ├── landing/
        |── bacen/
            ├── cartoes_trimestral/
                └── 2025
                      └── 01
                        └── 12
                          └── data_12_01_2025_01_16_54.json
            ├── meios_pagamentos_mensal/
                └── 2025
                      └── 01
                        └── 12
                          └── data_12_01_2025_01_16_54.json
            ├── meios_pagamentos_trimestral/
                └── 2025
                      └── 01
                        └── 12
                          └── data_12_01_2025_01_16_54.json
```

A concretização desta etapa poderá ser encontrada dentro do caminho a seguir, na estrutura de arquivos do projeto:

  **``` src > ingestions > ingestion_meios_pagamento.py ```**

#### **3. Processamento e Transformação dos Dados**

Como solução de armazenamento vamos usar o MinIO, a escolha se deu dado a sua simplicidade, alto poder e performance, além de ser open e facilmente configurável via Container Docker.

Para processamento distribuido dos dados entre as camadas do nosso Delta Lake vamos usar o Spark. 

Neste projeto vamos replicar uma **arquitetura Medalhão** com a adição de mais uma camada, a Landing. A seguir explicarei cada parte.

  - **Camada Landing(Área de pouso para alguns casos, Histórico As-Is em outros Casos)**
    - Optei por adicionar a camada Landing em nosso projeto para realização do pouso e gravação dos dados no seu formato original, exatamente como foram recebidos das fontes. Para alguns cenários, em algumas empresas, a Landing pode ser algo redundante e só aumentar os custos, entretanto, neste projeto, decidi implementá-la visando aplicar um formato padronizado (Delta) já à partir da camada Bronze.

    todo o fluxo de ingestão da landing para a Bronze pode ser acompanhado no notebook no seguinte caminho:
    
    **``` notebooks > landing2bronze.ipynb```**

  - **Camada Bronze(Dados Brutos)**
    - Mantendo ainda os dados como no original "as-is" a ideia aqui é aplicar somente um formato otimizado e padronizado (Delta)    
    - Vamos adicionar campos de metadados, como referência a origem entre outras.
    - Oferecer os dados como Delta, ainda na camada Bronze é ideal para:
      - Otimiza o trabalho de quem for consumir, não precisando ter tecnologias diferentes para diferentes formatos, como CSV, JSON, outros.
      - Otimiza o consumo ou leitura de dados ainda na origem, já que Delta é muito mais performático do que qualquer outro formato simples.
  
  - **Camada Silver(Dados Refinados)**
    - Vamos definir um Schema, já explodindo listas e objetos arquivo JSON original para a tabela final Delta.
    - Vamos realizar a limpeza, eliminação e validação de valores duplicados
    - Quando aplicável vamos criar novas variáveis.
    - Normalização dos campos (ex.: padronizar valores monetários).
    - Tratamento de missing/empty values ou valores inconsistentes, fora do esperado.

  - **Camada Gold(Dados Curados)**
    - Aqui vamos otimizar, agrupando ou ajustando segundo regras de negócio.
    - O objetivo será otimizar os dados para a geração de relatórios, visualizações ou usuários finais.

#### **4. Carregamento no Data Warehouse Open Source**

- Simulando um DataWarehouse ou engine de processamento SQL vou usar o **DuckDB**.
- Esta é uma alternativa leve extremamente poderosa para análises e processamento analytico local.

#### **5. Análise e Visualização**
- Vou realizar algumas análises exploratórias e criar visualizções sobre:
  - Comparação entre o crescimento do Pix e a redução do uso de TED/DOC.
  - Impacto sazonal nos pagamentos com cartões.
  - Correlação entre volume transacionado e número de transações por tipo de pagamento.
  - Para realização das análises e criação das visualizações vou usar Notebook Python e Plotly.

#### **6. Monitoramento e Automação**
- Use o Apache Airflow para orquestrar todo o pipeline, desde a coleta na API até o carregamento no data warehouse.
- Configure alertas para monitorar falhas no pipeline ou atrasos na atualização dos dados.


### **Ferramentas Utilizadas**
1. **Armazenamento**: MinIO (compatível com S3).
2. **Processamento**: Python (Pandas, PySpark) ou Apache Spark.
3. **Data Warehouse Open Source**: DuckDB.
4. **Orquestração**: Apache Airflow.
5. **Visualização**: Para simplificar vamos usar um Notebook Python mesmo com Plotly, vai ficar bem simples e legal no final


### **Resultados Esperados**
- Um pipeline automatizado que coleta, processa e analisa dados sobre meios de pagamento no Brasil.
- Insights detalhados sobre a evolução do mercado financeiro, incluindo:
  - Adoção crescente do Pix em comparação com métodos tradicionais (TED/DOC).
  - Tendências sazonais no uso de cartões pré-pagos versus crédito/débito.
- Dashboards interativos acessíveis via Metabase/Superset conectados ao data warehouse.


