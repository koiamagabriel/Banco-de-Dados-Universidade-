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

1. Descrição do Projeto:

## Passo a Passo do Desenvolvimento

### Etapa 1: Modelagem dos Dados
`Na primeira etapa, começamos criando um modelo DER na plataforma ERD Plus, facilitando assim, a nossa organização e, a propria plataforma, permite transformar do modelo DER para o modelo Relacional sem precisar buscar fontes externar para a continuidade do nosso projeto.`

### Etapa 2: Criação das Tabelas
`Na segunda etapa, com base nos modelos criados na etapa 1 `



### Etapa 3: Inserção de Dados
- Geração de dados aleatórios realistas com Python + Supabase
- Utilização de `UPSERT` para evitar duplicações

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
   


`Detalhamento do Passo a passo: Membro da empresa entrando na plataforma`
