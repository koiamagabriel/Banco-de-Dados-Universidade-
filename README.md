# Banco-de-Dados-Universidade-

Criadores do Projeto:

João Pedro Lopes - RA: 22.125.065-7
***
João Pedro Peterutto - RA: 22.125.066-5
***
Gabriel Koiama - RA: 22.125.067-3
***

`Este repositório contém o desenvolvimento completo de um banco de dados relacional para gerenciamento acadêmico de uma universidade. O projeto foi construído com base em um modelo realista, integrando tabelas como alunos, professores, disciplinas, cursos, TCCs e históricos escolares.`

---


### Modelo Entidade-Relacionamento (DER)
![Imagem do WhatsApp de 2025-04-16 à(s) 23 01 58_e7c6fa68](https://github.com/user-attachments/assets/2e64c10e-4a57-4759-b184-7d02b3b6b90e)




---

### Modelo Relacional

![Esquema Relacional - Supabase](https://github.com/user-attachments/assets/d3226c87-9c6a-4d32-a805-4a74e3864185)


---


# Estrutura do Projeto:

## Entidades e Relacionamentos

| Tabela        | Descrição |
|---------------|-----------|
| `alunos`       | Registra informações sobre os alunos, incluindo nome, idade, e-mail, e o curso em que estão matriculados. |
| `professores`   | Informações sobre os professores, incluindo nome, e-mail e o departamento ao qual pertencem. |
| `disciplinas`  | Contém informações sobre as disciplinas oferecidas, incluindo o nome da disciplina, carga horária e um identificador único |
| `cursos`       | Informações sobre os cursos oferecidos pela universidade, incluindo o nome do curso, o departamento e o coordenador. |
| `departamento`| Contém informações sobre os departamentos da universidade, como o nome do departamento e o chefe. |
| `tccs`         | Armazena os temas de TCC dos alunos, associando cada TCC a um professor orientador |
| `tcc_alunos`   | Relaciona alunos com os TCCs que estão orientando, criando uma associação N:N entre alunos e seus TCCs. |
| `curso_disciplina`       | Relaciona cursos e disciplinas, associando cada curso com as disciplinas que ele oferece, incluindo o período em que são lecionadas. |
| `disciplinaslecionadas`   | Relaciona professores às disciplinas que lecionam, incluindo o serial da disciplina e o professor responsável |
| `historicoescolar` | Registra o desempenho dos alunos nas disciplinas que estão cursando, incluindo nota, semestre e status (aprovado ou reprovado) |


## Passo a Passo do Desenvolvimento

### Etapa 1: Modelagem dos Dados
`Nesta etapa, utilizamos a plataforma ERD Plus para criar o Modelo Entidade-Relacionamento (DER) do sistema. A ferramenta facilitou a visualização e organização das entidades e relacionamentos, além de permitir a conversão direta para o modelo relacional. O objetivo foi representar de forma clara a estrutura acadêmica da universidade, mapeando alunos, cursos, professores, disciplinas, TCCs e departamentos.`

### Etapa 2: Criação das Tabelas
`Com o modelo relacional pronto, desenvolvemos os scripts DDL para criação das tabelas no Supabase. Essa etapa permitiu integrar o banco de dados ao Visual Studio Code, possibilitando o uso de Python para manipulação e inserção de dados.`



### Etapa 3: Inserção de Dados
`Com a estrutura feita na etapa anterior, passamos para a fase de inserção dos dados. Utilizamos Python em conjunto com o Supabase para gerar informações aleatórias, como nomes de alunos, professores, temas de TCC, notas e vínculos entre as tabelas. Para garantir que os dados fossem inseridos de forma segura e sem repetições, aplicamos a lógica de UPSERT, que insere novos registros ou atualiza os existentes automaticamente.`

### Etapa 4: Lógica de Vínculo
- Cada aluno é vinculado a:
  - 1 curso
  - 1 tema de TCC
  - 1 histórico
  - De 3 a 5 disciplinas compatíveis com o seu curso
- Regras de preenchimento:
  - Cada disciplina com 1 a 5 alunos
  - Cada curso com 3 a 10 alunos

### Etapa 5: Consultas SQL Avançadas
- Join entre tabelas para gerar:
  - Situação dos alunos (Aprovado/Reprovado)
  - Cálculo de semestre real
  - Listagem de TCCs por departamento
   

## Como executar o projeto

### Etapa 1: Criar uma conta no Supabase
- Acesse: https://supabase.com
  - Clique em "Start your project" ou "Sign Up"
  - Crie sua conta (pode usar GitHub ou email)

### Etapa 2: Criar um novo projeto
- Após o login, clique em "New Project":
  - Escolha um nome e senha para o banco de dados
  - Selecione a região e clique em "Create project"

### Etapa 3: Criar as tabelas no Supabase
- No painel do projeto, vá até a aba "SQL Editor"
  - Cole os scripts DDL fornecidos no repositório
  - Execute para criar todas as tabelas do banco

### Etapa 4: Instalar o Python
- Acesse: https://www.python.org/downloads/
  - Baixe a versão mais recente
  - Durante a instalação, marque a opção "Add Python to PATH"


### Etapa 5: Instalar o Visual Studio Code
- Acesse: https://code.visualstudio.com/
  - Baixe e instale o VS Code
  - Instale a extensão "Python" pelo menu de extensões
  - Crie uma pasta para o projeto e abra no VS Code

### Etapa 6: Instalar as bibliotecas necessárias
- No terminal do VS Code, execute:
  - pip install supabase
 
### Etapa 7: Configurar a conexão com o Supabase
- Siga as instruções do link a seguir:
  -  https://supabase.com/docs/reference/python/introduction

### Etapa 8: Executar o Projeto
- Execute os scripts Python fornecidos neste repositório para inserir dados e fazer consultas
  -  Acompanhe os dados pelo painel do Supabase (aba "Table Editor")
  -  Utilize comandos SQL ou Python para validar os relacionamentos e a estrutura





