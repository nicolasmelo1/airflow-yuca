# airflow-yuca
Project for Yuca's Data Engeneering Role

## Motivação
Essa é a solução ótima para o problema ainda que a solução seja bastante _overkill_ para o problema proposto.
Com essa solução nós não temos que rodar um programa ou script todo dia para nos lembrar de fazer algo, nós simplesmente criamos uma [DAG](https://airflow.apache.org/docs/apache-airflow/stable/concepts.html#dags) para realizar essa tarefa para nós no dia e no momento que precisamos. Além disso, ao invés de precisarmos extrair os dados de uma maneira "fisica", como um arquivo, nós simplesmente realizamos um processo chamado de ETL (ou Extract, Load and Transform) onde nós pegamos os dados do Big Query, transformamos e carregamos no nosso banco de dados. Dessa maneira as informações estarão sempre disponiveis para os usuários que desejarem visualizar esse dado. Permitindo cruzamentos entre varias informações internas e outras analises.

## O projeto
Para isso, nós utilizamos o [Airflow](https://airflow.apache.org). O Airflow é uma ferramenta open source criado no Airbnb para gerenciar e programar fluxos de trabalho. Com ele podemos programar várias DAGs e dentro de cada DAG, podemos criar tasks a fim de cumprir um ou mais objetivos.
Geralmente o Airflow é bastante utilizado pelas empresas para a realização de ETLs. Onde os dados precisam ser extraidos de uma ponta e carregados em outra ponta. Em alguns poucos casos ele também é utilizado para automação e agendamento de tarefas, porém não recomendo, uma vez que existem soluções mais simples para tais problemas, como utilizar Bull em Node.js ou uma aplicação Flask ou Django simples com Celery e supervisord.

### Conteúdos e pastas
- **dags/**: Contém todas as dags do airflow, para o nosso caso simples, apenas a dag `teste_yuca_dag.py` (tenha em mente que o nome do arquivo geralmente é o nome da dag e esse nome também deve ser definido ao inicializar a classe DAG no topo do arquivo)
- **scripts/**: Aqui teremos nossos scripts de produção, staging e desenvolvimento, eles irão conter arquivos shell para configurar nossos ambientes, consideraremos *production* como sendo tanto staging quanto produção, dessa maneira conseguimos deixar nosso ambiente de staging o mais proximo possivel do ambiente de produção.
- **sql/**: Aqui deixamos nossos templates SQL para utilizarmos nas nossas dags. (tenha em mente que as variaveis definidas nesses arquivos estão definidas de maneira errada pois estamos fazendo uma subsitituição por string, porém o jeito correto é o seguinte: https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.execute)
- **operations.sqlite**: Nós não temos um banco de dados criado para onde irão os nossos dados, portanto escolhi usar um banco de dados simples, local, chamado SQlite. Como ele é apenas um arquivo, se torna extremamente simples trabalharmos com ele, e a lógica que é aplicada nele pode ser aplicada em qualquer outro banco de dados relacional como Postgres ou MySQL.
- **Teste Yuca Big Query-de3f6b24ce4b.json**: Minha chave para acessar o Big Query, podia usar o próprio operador do Big Query oferecido pelo airflow porém escolhi usar a própria API diretamente. Uma vez que escolhi usar a API, este arquivo contém todos os dados necessários para acessar o big query do google.

### Como inicializar

Recomendo utilizar o docker e o docker-compose, caso você tenha ele instalado em seu computador.

#### Necessário ter instalado no seu computador
- Python 3.8
- Docker
- Docker-compose

##### Docker
Para rodar a aplicação rode os seguintes comandos em ordem
```
$ docker-compose build
$ docker-compose run --rm airflow_scheduler airflow users create --username admin --firstname admin --lastname admin --role Admin --password admin --email admin@admin.com
$ docker-compose up
```
 
Passo a passo:

- Buildamos a aplicação e criamos nossos containers docker
- Criamos um usuário para que possamos nos cadastrar com na UI, o email desse usuário é `admin@admin.com` e a senha é `admin`
- Efetivamente rodamos o container docker
- Acesse: localhost:8080 no seu browser, se logue com o e mail e senha do novo usuário
- Clique em Dags no menu superior, e ative a dag chamada `teste_yuca_dag` clicando no Switch lateral esquerdo da interface.

##### Local
Para rodar a aplicação localmente, primeiro crie uma venv e ative ela com os comandos ([no windows é um pouco diferente](https://docs.python.org/pt-br/3/library/venv.html))
```
$ python3 -m venv venv
$ source venv/bin/activate
```

Seguido isso instale as dependências com o comando:
```
$ pip install -r requirements.txt
```

Modifique o arquivo `scripts/development/development.env` setando as variaveis de ambiente necessárias de acordo com sua plataforma (os paths devem ser absolutos).

Para rodar, use os seguintes comandos em duas janelas do seu terminal:
```
$ source ./scripts/development/development.env && airflow scheduler
$ source ./scripts/development/development.env && airflow webserver
```

A partir dai sua interface UI estará disponivel na porta 8080