## **Projeto: Pipeline de Dados e Análise dos Meios de Pagamento no Brasil**

**Será que a mudança no monitoramento do PIX vai reduzir a demanda?**

Olá me chamo Natanael Domingos, e decidi iniciar uma série de projetos de Engenheria de dados como forma de compartilhar conhecimento e construir um portfólio.

A alguns dias me deparei com a API de Pagamentos, mantida pelo Banco Central do Brasil, que contêm estatísticas sobre:
- Diferentes **tipos** de pagamento no país
- A quantidade de transações realizadas por cada tipo
- O total de valores movimentados por tipo, consolidado por mês ou trimestre.

Documentação e Referência da API:
- https://dadosabertos.bcb.gov.br/dataset/estatisticas-meios-pagamentos

Vou usar este recurso como fonte de dados para este projeto de portfólio. A intensão será desenvolver um novo pipeline de dados e depois realizar algumas análises. 

Tenho certeza que este será um bom exemplo para ilustrar o que acontece no dia a dia de um Engenheiro de dados. Meu objetivo será demonstrar habilidades essenciais para engenharia de dados utilizando tecnologias modernas como MinIO e ferramentas open source, além de abordar um tema relevante e atual na economia brasileira.

Pela simplicidade, e também por questões de custos, vou usar soluções simples e open source neste projeto, todavia pretendo explorar recursos mais comerciais, como Cloud, em outras versões deste mesmo projeto ou em novos projetos.

### **Objetivo**
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
#### **3. Processamento e Transformação dos Dados**

Como solução de armazenamento teremos um Data Lake no MinIO, aplicando a arquitetura Medalhão com uma adição, a folder Landing, a seguir explicarei cada parte.

  - **Camada Landing(Área de pouso para alguns casos, Histórico As-Is em outros Casos)**
    - Optei por adicionar a folder Landing, para pouso e gravação de dados no seu formato original, exatamente como foram recebidos das fontes. Para alguns cenários esta inclusão pode ser útils, para outros cenários, em algumas empresas pode algo redundante e só aumentar os custos. Mas a minha ideia é já aplicar um formato padronizado (Delta) a partir da Bronze.

  - **Camada Bronze(Dados Brutos)**
    - Mantendo ainda os dados como no original "as-is" a ideia aqui é aplicar somente um formato otimizado e padronizado (Delta)
    - É claro que já ocorre alguma tratativa, como explodir listar ou objetos do arquivo JSON original para a tabela final Delta, mas nada que filtre ou altere os dados.
  
  - **Camada Silver(Dados Refinados)**
    - Vamos realizar a limpeza, eliminação e validação de valores duplicados

  - **Camada Silver(Dados Curados)**

Como solução para processamento dentro do Data Lake, entre as camas da arquitetura medalhão, vou usar o Spark.






    - Na arquitetura medalhão geralmente começamos a partir da Bronze, armazenando neste folder os dados em variós formatos, "as-is" com o Sistema origem.
    - Tomei esta decisão levando em consideração, resumidamente, alguns pontos:
      - Usuário deveria consumir dados diretamente da Bronze? por definição não, uma primeira camada de dados tratados e confiáveis deveriam ser consumidas a partir da Silver, mas nada neste mundo esta *escrito na pedra*. E seu alguma esquipe de Machine Learning, IA developers, quiser ter acesso ao dado bruto, em seu formato original, sem ter passado por nenhuma normalização ou padronização que possa ter desbalanceado ou enviezado sua amostra de dados, para o treinamento de seu modelo?
      - Neste casos seria mais prático ter estes dados a disposição na Bronze já em um formato otimizado e performático (Delta e.g), claro, com alguma tratativa mas sem nenhuma normalização.
      - Imagine outro cenário onde a empresa já tem um ambiente OnPrem e esta migrando para a Cloud, ou seja estas bases na origem já tem uma estrutura mínima, como Parquet, estas poderiam vir diretamente para a Bronze, em um processo de ingesta, mas talvez outras fontes, com formatos diferentes devam pousar primeiramente na landing para em seguida, convertendendo para um formato otimizado ser carregado na bronze. 
    - T
    - Normalização e tratamento dos Dados para carregamento e disponibilização na camada Silver.
      - 
  - Da Silver para a Gold
  
  - Extração dos Dados no formato original da folder Landing
  - Normalização dos campos (ex.: padronizar valores monetários).
  - Tratamento de valores ausentes ou inconsistentes.
  - Conversão para formatos otimizados (ex.: Parquet, Delta) para carregamento eficiente no data warehouse.
- Use frameworks como Pandas ou Apache Spark para processar os dados.

#### **4. Carregamento no Data Warehouse Open Source**
- Escolha um data warehouse open source adequado:
  - **DuckDB**: Alternativa leve para análises locais ou em pequenos clusters.
- Configure a ingestão dos arquivos transformados do MinIO diretamente no data warehouse escolhido.

#### **5. Análise e Visualização**
- Realize análises exploratórias e crie relatórios:
  - Comparação entre o crescimento do Pix e a redução do uso de TED/DOC.
  - Impacto sazonal nos pagamentos com cartões.
  - Correlação entre volume transacionado e número de transações por tipo de pagamento.
- Conecte ferramentas como Metabase (open source) ou Superset ao data warehouse para criar dashboards interativos.

#### **6. Monitoramento e Automação**
- Use o Apache Airflow para orquestrar todo o pipeline, desde a coleta na API até o carregamento no data warehouse.
- Configure alertas para monitorar falhas no pipeline ou atrasos na atualização dos dados.

---

### **Ferramentas Utilizadas**
1. **Armazenamento**: MinIO (compatível com S3).
2. **Processamento**: Python (Pandas, PySpark) ou Apache Spark.
3. **Data Warehouse Open Source**: DuckDB.
4. **Orquestração**: Apache Airflow.
5. **Visualização**: Para simplificar vamos usar um Notebook Python mesmo com Plotly, vai ficar bem simples e legal no final

---

### **Resultados Esperados**
- Um pipeline automatizado que coleta, processa e analisa dados sobre meios de pagamento no Brasil.
- Insights detalhados sobre a evolução do mercado financeiro, incluindo:
  - Adoção crescente do Pix em comparação com métodos tradicionais (TED/DOC).
  - Tendências sazonais no uso de cartões pré-pagos versus crédito/débito.
- Dashboards interativos acessíveis via Metabase/Superset conectados ao data warehouse.

---

