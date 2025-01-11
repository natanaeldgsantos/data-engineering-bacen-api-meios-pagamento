## **Projeto: Pipeline de Dados e Análise dos Meios de Pagamento no Brasil**

**Será que a mudança nas regras do pix vai reduzir a demanda?**

Questão super em alta neste momento (janeiro de 2025)

Olá me chamo Natanael Domingos, e decidi iniciar uma série de projetos de Engenheria de dados como forma de compartilhar conhecimento e construir um portfólio.

A alguns dias me deparei com a API de Pagamentos mantida pelo Banco Central do Brasil, que contem statísticas sobre:
- Diferentes **tipos** de pagamento no país
- A quantidade de transações realizadas por cada tipo
- O total de valores movimentados por tipo, consolidado por mês ou trimestre.

Vou usar este recurso como fonte de dados para o nosso projeto de portfólio. A intensão será desenvolver um novo pipeline de dados e depois realizar algumas análises. 

Tenho certeza que este case será um bom exemplo, ilustrando bem o que acontece no dia a dia de um Engenheiro de dados que tem com responsabilidades: 
  - Ingerir dados de diferentes tipos de fontes
  - Otimizar bases de dados para realização de análises
  - Remover dados corrompidos
  - Desenvolver, construir, testar e manter arquiteturas de dados. 

Este projeto demonstra habilidades essenciais para engenharia de dados utilizando tecnologias modernas como MinIO e ferramentas open source, além de abordar um tema relevante e atual na economia brasileira.

Pela simplicidade, e também por questões de custos, vou usar soluções simples e open source, mas pretendo explorar recursos mais comerciais, como Cloud, em outras versões deste mesmo projeto ou em novos.

### **Objetivo**
Desenvolver um pipeline de dados automatizado que consuma informações da API de Estatísticas de Meios de Pagamento do Banco Central, armazene os dados no MinIO como storage principal, e realize análises utilizando um Data Warehouse (vou usar o DuckDB mesmo). 

O objetivo é identificar tendências no uso de diferentes meios de pagamento, como Pix, TED, boletos e cartões.

---

### **Etapas do Projeto**

#### **1. Coleta e Armazenamento dos Dados **
- Utilize a API do Banco Central para acessar dados mensais e trimestrais sobre meios de pagamento.
- Realizar Ingestão dos dados na fonte (vou aproveitar para usar Python DLT, mas poderia ser uma ferramenta de ingestão como Nifi ou Airbyte).
- Salve os dados coletados em formato JSON ou CSV no MinIO, que será usado como camada de armazenamento principal.
  - Vamos simular uma arquitetura medalhão no MiniIO, vou criar o bucket principal com a seguintes folders:
    - Landing: armazenar os dados no formato original, no caso JSON
    - Bronze: dados ainda sem normalização mas já em um formato comun, vamos usar **tabelas Delta**.
    - Silver: Dados já normalizados e pré-processados, uma primeira camada confiável para o consumo.
    - Gold: Dados especializados com o olhar/regras do negócio, já agregados em especial para uso do BI

##### **Exemplo de Estrutura de Diretórios na folder Landing do nosso Data Lake com MinIO**
```
/meios_pagamento/
  ├── mensal/
  │     ├── pix_2023_09.json
  │     ├── ted_2023_09.json
  │     └── boletos_2023_09.json
  ├── trimestral/
  │     ├── cartoes_2023_Q3.csv
  │     └── convenios_2023_Q3.csv
```

#### **3. Processamento e Transformação dos Dados**
- Extraia os dados do MinIO para transformações:
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

