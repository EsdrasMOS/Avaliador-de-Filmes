**🚀Avaliador de Filmes**

O sistema de Avaliação de Filmes registra novos filmes que o usuário adiciona com as informações do nome do filme, autor, diretor e genêro, podendo ler, atualizar informações ou deletar filmes específicos, podendo deixar a sua avaliação sobre cada um deles, e deixar um comentário sobre a sua opinião do filme. 

---

**📌 Sobre o projeto**

- Com o aumento do consumo de filmes, muitos usuários não encontram boas formas de organizar e registrar suas opiniões sobre o filme.
- Nesta perspectiva, criamos um sistema de controle personalizado, possibilitando criação de usuário, filmes, leitura de cada um e atualizações livres.
- Esse projeto se iniciou como um projeto acadêmico com o objetivo de praticar o uso de frameworks para back-end de sistemas.

---

**🛠️ Tecnologias utilizadas**

- Linguagem: Python
- Frameworks e Bibliotecas: Boto3, python-dotenv
- Banco de dados: DynamoDB
- Outras ferramentas: Git 

---

**⚙️ Funcionalidades**

- Criar, ler, atualizar e deletar usuários.
- Criar, ler, atualizar e deletar filmes.
- Avaliar filmes.
- Deletar avaliações
- CRUD interagível pelo terminal.

---

**📁 Estrutura do projeto**

```bash
📦 Avaliador-de-Filmes
 ┣ 📂 .vscode
    ┗ settings.json
 ┣ 📜 dynamo.py
 ┣ 📜 crud.py
 ┗ 📜 README.md

 ```

---

**Guia de Instalação**

## 1. Pré-requisitos
- Antes de começar, certifique-se de que você tem os seguintes itens instalados no seu computador:
- Python 3.8 ou superior:
- Conta na AWS: Você precisará de credenciais (Access Key e Secret Key) com permissões para ler e escrever no DynamoDB.
- (Opcional) AWS CLI: Instalado e configurado, caso prefira gerenciar as credenciais por ele.

## 2. Configuração do Ambiente Virtual
Para evitar conflitos com outras instalações do Python, sempre use um ambiente virtual.
Abra o PowerShell na pasta raiz do projeto (Avaliador-de-Filmes) e execute:

````Comando
py -m venv venv
.\venv\Scripts\Activate.ps1
````
Nota: Se o PowerShell bloquear a ativação, execute Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser e tente ativar novamente.

## 3. Instalação das Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias para o projeto.
Dependências do Projeto:
boto3: SDK da AWS para Python (usado para interagir com o DynamoDB).
python-dotenv: Para carregar variáveis de ambiente (como chaves da AWS) de forma segura.
Execute o comando abaixo no terminal:
````Comando
pip install boto3 python-dotenv
````

## 4. Configuração das Credenciais da AWS
Existem duas formas do boto3 saber quem você é para acessar o DynamoDB:
Opção A: Usando AWS CLI (Recomendado e mais simples)
Se você instalou o AWS CLI, basta abrir um terminal (não precisa estar com o venv ativado) e rodar:
````Comando
aws config
````
Insira sua AWS Access Key ID, AWS Secret Access Key e a Default region name (ex: sa-east-1 ou us-east-1). O boto3 lerá essas credenciais automaticamente.

Opção B: Usando arquivo .env (Se o seu código usar python-dotenv)
Crie um arquivo chamado .env na raiz do projeto (mesma pasta do crud.py) e adicione:

````Comando
AWS_ACCESS_KEY_ID=sua_access_key_aqui
AWS_SECRET_ACCESS_KEY=sua_secret_key_aqui
AWS_DEFAULT_REGION=sa-east-1
DYNAMODB_TABLE_NAME=nome_da_sua_tabela
````
(Certifique-se de que o arquivo .env não seja enviado para o GitHub/OneDrive).

## 5. Executando o Projeto
Com o ambiente ativado e as credenciais configuradas, você já pode rodar o script:
````Comando
py crud.py
````
