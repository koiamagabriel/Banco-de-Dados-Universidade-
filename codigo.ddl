/* 1. Tabela: Departamentos */
/* Note que as colunas id_chefe, id_curso e id_professor são declaradas, mas as restrições de FK serão adicionadas posteriormente */
CREATE TABLE Departamentos (
    id_departamento INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_chefe VARCHAR(10)      -- FK para Professores (a ser adicionada via ALTER TABLE)
);

/* 2. Tabela: Professores */
CREATE TABLE Professores (
    id_professor VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    id_departamento INT NOT NULL,
    CONSTRAINT fk_prof_departamento
        FOREIGN KEY (id_departamento)
        REFERENCES Departamentos(id_departamento)
);

ALTER TABLE Departamentos
ADD CONSTRAINT fk_departamento_chefe
    FOREIGN KEY (id_chefe)
    REFERENCES Professores(id_professor);

create table public.cursos (
  id_curso integer not null,
  nome character varying(100) not null,
  id_departamento integer not null,
  id_coordenador character varying(10) null,
  constraint cursos_pkey primary key (id_curso),
  constraint fk_curso_coordenador foreign KEY (id_coordenador) references professores (id_professor),
  constraint fk_curso_departamento foreign KEY (id_departamento) references departamentos (id_departamento)
) TABLESPACE pg_default;

create table public.alunos (
  id_aluno integer not null,
  nome character varying(100) not null,
  idade integer null,
  email character varying(100) null,
  id_curso integer not null,
  constraint alunos_pkey primary key (id_aluno),
  constraint fk_aluno_curso foreign KEY (id_curso) references cursos (id_curso)
) TABLESPACE pg_default;

create table public.disciplinas (
  id_disciplina character varying(10) not null,
  nome character varying(100) not null,
  carga_horaria integer null,
  disciplina_serial integer not null,
  constraint disciplinas_pkey primary key (disciplina_serial),
  constraint disciplinas_id_disciplina_key unique (id_disciplina)
) TABLESPACE pg_default;

create table public.curso_disciplina (
  id_curso integer not null,
  id_disciplina character varying(10) not null,
  periodo character varying(10) null,
  constraint curso_disciplina_pkey primary key (id_curso, id_disciplina),
  constraint fk_cursodisciplina_curso foreign KEY (id_curso) references cursos (id_curso),
  constraint fk_cursodisciplina_disciplina foreign KEY (id_disciplina) references disciplinas (id_disciplina)
) TABLESPACE pg_default;

create table public.historicoescolar (
  id_aluno integer not null,
  id_disciplina character varying(10) not null,
  nota numeric(3, 1) null,
  semestre character varying(20) not null,
  status character varying(10) null,
  constraint fk_historico_aluno foreign KEY (id_aluno) references alunos (id_aluno),
  constraint fk_historico_disciplina foreign KEY (id_disciplina) references disciplinas (id_disciplina)
) TABLESPACE pg_default;

create table public.disciplinaslecionadas (
  id_professor character varying(10) not null,
  id_disciplina character varying(10) not null,
  disciplina_serial integer null,
  constraint disciplinaslecionadas_disciplina_serial_fkey foreign KEY (disciplina_serial) references disciplinas (disciplina_serial),
  constraint fk_historicolec_disciplina foreign KEY (id_disciplina) references disciplinas (id_disciplina),
  constraint fk_historicolec_professor foreign KEY (id_professor) references professores (id_professor)
) TABLESPACE pg_default;

create table public.tccs (
  id_tcc integer not null,
  assunto character varying(255) not null,
  id_professor character varying(10) not null,
  constraint tccs_pkey primary key (id_tcc),
  constraint fk_tcc_professor foreign KEY (id_professor) references professores (id_professor)
);

create table public.tcc_alunos (
  id_tcc integer not null,
  id_aluno integer not null,
  constraint tcc_alunos_pkey primary key (id_tcc, id_aluno),
  constraint fk_tccaluno_aluno foreign KEY (id_aluno) references alunos (id_aluno),
  constraint fk_tccaluno_tcc foreign KEY (id_tcc) references tccs (id_tcc)
);
