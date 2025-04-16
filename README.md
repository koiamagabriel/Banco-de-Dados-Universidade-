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



---

### Modelo Relacional



---


# Estrutura do Projeto:

## Entidades e Relacionamentos

| Tabela        | Descrição |
|---------------|-----------|
| `aluno`       | Alunos com nome, RA, curso e TCC |
| `professor`   | Professores vinculados a departamentos |
| `disciplina`  | Disciplinas oferecidas pelos cursos |
| `curso`       | Cursos e seus coordenadores |
| `departamento`| Departamentos da universidade |
| `tcc`         | Temas de TCC associados a professores e departamentos |
| `participa`   | Relação entre professores e departamentos |
| `possui`      | Relaciona disciplinas com cursos |
| `cursa`       | Disciplinas que os alunos estão cursando |
| `historico`   | Registro de notas, semestre e situação dos alunos |
| `historico_disciplina` | Relacionamento N:N entre histórico e disciplina |


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
Acesse: https://supabase.com

Clique em "Start your project" ou "Sign Up".

Crie sua conta (pode usar GitHub ou email).

Após o login, clique em "New Project":

Escolha um nome e senha para o banco de dados.

Selecione a região e clique em "Create project".

Aguarde alguns minutos até o Supabase criar seu banco de dados.
