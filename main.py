
import os
import random
from supabase import create_client, Client
from pprint import pprint
from collections import defaultdict

url: str = os.environ.get("SUPABASE_URL", "https://vcaneihxrqnmrqcttnsl.supabase.co")
chave: str = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZjYW5laWh4cnFubXJxY3R0bnNsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQzMzQ1MDIsImV4cCI6MjA1OTkxMDUwMn0.3VZ7H4KNKJGPLShDhk_p6dT2n-ayJHWEBsPrLhkeUdg")
supabase: Client = create_client(url, chave)

historicoescolar_registros = supabase.table("historicoescolar").select("id_aluno, id_disciplina").execute().data

for registro in historicoescolar_registros:
    supabase.table("historicoescolar").delete()\
        .eq("id_aluno", registro["id_aluno"])\
        .eq("id_disciplina", registro["id_disciplina"]).execute()

print("Tabela 'historicoescolar' limpa com sucesso.")

disciplinaslecionadas_registros = supabase.table("disciplinaslecionadas").select("id_disciplina, id_professor").execute().data

for registro in disciplinaslecionadas_registros:
    supabase.table("disciplinaslecionadas").delete()\
        .eq("id_disciplina", registro["id_disciplina"])\
        .eq("id_professor", registro["id_professor"]).execute()

print("Tabela 'disciplinaslecionadas' limpa com sucesso.")

curso_disciplina_registros = supabase.table("curso_disciplina").select("id_disciplina, id_curso").execute().data

for registro in curso_disciplina_registros:
    supabase.table("curso_disciplina").delete()\
        .eq("id_disciplina", registro["id_disciplina"])\
        .eq("id_curso", registro["id_curso"]).execute()

print("Tabela 'curso_disciplina' limpa com sucesso. Pronto para realizar UPSERT nas disciplinas.")

nomes_departamentos_possiveis = [
    "Departamento de Computação",
    "Departamento de Matemática",
    "Departamento de Física",
    "Departamento de Química",
    "Departamento de Biologia",
    "Departamento de Engenharia",
    "Departamento de Administração",
    "Departamento de Letras"
]

departamentos_selecionados = random.sample(nomes_departamentos_possiveis, 5)

registros_departamentos = []
for i, nome_dep in enumerate(departamentos_selecionados, start=1):
    registro = {
        "id_departamento": i,
        "nome": nome_dep,
        "id_chefe": None
    }
    registros_departamentos.append(registro)

resposta_departamentos = supabase.table("departamentos").upsert(registros_departamentos).execute()
print("Departamentos inseridos/atualizados:")
pprint(resposta_departamentos.data)

nomes_primeiros = [
    "Alice", "Bruno", "Carlos", "Daniela", "Eduardo", "Fabiana", "Gabriel", "Helena", "Igor", "Juliana",
    "Kevin", "Laura", "Marcos", "Natália", "Otávio", "Paula", "Quintino", "Rafael", "Sabrina", "Thiago",
    "Úrsula", "Vinícius", "Wagner", "Ximena", "Yuri"
]

sobrenomes = [
    "Silva", "Souza", "Oliveira", "Pereira", "Lima", "Costa", "Rodrigues", "Almeida", "Nascimento", "Gomes",
    "Martins", "Ribeiro", "Carvalho", "Fernandes", "Rocha", "Barbosa", "Mendes", "Araújo", "Teixeira", "Ramos",
    "Dias", "Correia", "Melo", "Castro", "Borges", "Vasconcelos", "Pinto", "Santos", "Moraes", "Moreira",
    "Cardoso", "Lacerda", "Monteiro", "Gonçalves", "Farias", "Vieira", "Pacheco", "Rezende", "Assis", "Batista"
]

emails_gerados = set()
registros_professores = []
contador_id_professor = 1

for id_dep in range(1, 6):
    for _ in range(20):
        primeiro_nome = random.choice(nomes_primeiros)
        sobrenome1, sobrenome2 = random.sample(sobrenomes, 2)
        nome_completo = f"{primeiro_nome} {sobrenome1} {sobrenome2}"
        email = f"{primeiro_nome}{sobrenome1}{sobrenome2}".replace(" ", "").lower() + "@gmail.com"
        
        while email in emails_gerados:
            primeiro_nome = random.choice(nomes_primeiros)
            sobrenome1, sobrenome2 = random.sample(sobrenomes, 2)
            nome_completo = f"{primeiro_nome} {sobrenome1} {sobrenome2}"
            email = f"{primeiro_nome}{sobrenome1}{sobrenome2}".replace(" ", "").lower() + "@gmail.com"
        
        emails_gerados.add(email)
        
        registro_professor = {
            "id_professor": contador_id_professor,
            "nome": nome_completo,
            "email": email,
            "id_departamento": id_dep
        }
        registros_professores.append(registro_professor)
        contador_id_professor += 1

resposta_professores = supabase.table("professores").upsert(registros_professores).execute()
print("Professores inseridos/atualizados:")
pprint(resposta_professores.data)

for id_dep in range(1, 6):
    resposta_prof_dep = supabase.table("professores").select("id_professor")\
                                      .eq("id_departamento", id_dep).execute()
    professores_dep = resposta_prof_dep.data
    if professores_dep:
        chefe_selecionado = random.choice(professores_dep)["id_professor"]
        resposta_update = supabase.table("departamentos").update({"id_chefe": chefe_selecionado})\
                              .eq("id_departamento", id_dep).execute()
        print(f"Departamento {id_dep} atualizado com o chefe {chefe_selecionado}:")
        pprint(resposta_update.data)
    else:
        print(f"Nenhum professor encontrado para o departamento {id_dep}.")

resposta_departamentos = supabase.table("departamentos").select("id_departamento, nome, id_chefe").execute()
departamentos = resposta_departamentos.data
if not departamentos:
    raise Exception("Nenhum departamento encontrado. Insira os departamentos antes de criar os cursos.")

dicionario_cursos = {
    "computação": [
        "Engenharia de Computação", "Ciência da Computação", "Sistemas de Informação",
        "Redes de Computadores", "Inteligência Artificial", "Segurança da Informação", "Computação Gráfica"
    ],
    "matemática": [
        "Matemática Pura", "Matemática Aplicada", "Estatística",
        "Análise Numérica", "Geometria", "Álgebra", "Probabilidade"
    ],
    "física": [
        "Física Teórica", "Física Experimental", "Física Nuclear",
        "Astrofísica", "Mecânica Quântica", "Termodinâmica", "Óptica"
    ],
    "química": [
        "Química Orgânica", "Química Inorgânica", "Química Analítica",
        "Bioquímica", "Química Computacional", "Química Ambiental", "Físico-Química"
    ],
    "biologia": [
        "Biologia Celular", "Genética", "Ecologia",
        "Biotecnologia", "Microbiologia", "Zoologia", "Botânica"
    ],
    "engenharia": [
        "Engenharia Civil", "Engenharia de Produção", "Engenharia de Computação",
        "Engenharia Mecânica", "Engenharia Elétrica", "Engenharia Química", "Engenharia Ambiental"
    ],
    "administração": [
        "Administração de Empresas", "Gestão Financeira", "Marketing",
        "Recursos Humanos", "Gestão de Projetos", "Logística", "Empreendedorismo"
    ],
    "letras": [
        "Letras - Inglês", "Letras - Português", "Letras - Espanhol",
        "Letras - Francês", "Letras - Alemão", "Letras - Italiano", "Letras - Japonês"
    ]
}

registros_cursos = []
contador_id_curso = 1

for dept in departamentos:
    id_dep = dept["id_departamento"]
    nome_depart = dept["nome"]
    
    nome_depart_lower = nome_depart.lower()
    
    chave_area = None
    for area in dicionario_cursos.keys():
        if area in nome_depart_lower:
            chave_area = area
            break
    if chave_area is None:
        chave_area = random.choice(list(dicionario_cursos.keys()))
    
    lista_cursos_possiveis = dicionario_cursos[chave_area]
    cursos_selecionados = random.sample(lista_cursos_possiveis, 4)
    
    resposta_prof_dep = supabase.table("professores").select("id_professor")\
                                      .eq("id_departamento", id_dep).execute()
    professores_dep = resposta_prof_dep.data if resposta_prof_dep.data else []
    
    candidatos = []
    if professores_dep:
        for prof in professores_dep:
            if dept["id_chefe"] is not None and prof["id_professor"] == dept["id_chefe"]:
                continue
            candidatos.append(prof["id_professor"])
    if not candidatos and professores_dep:
        candidatos = [prof["id_professor"] for prof in professores_dep]
    
    for curso_nome in cursos_selecionados:
        id_coordenador = random.choice(candidatos) if candidatos else None
        registro_curso = {
            "id_curso": contador_id_curso,
            "nome": curso_nome,
            "id_departamento": id_dep,
            "id_coordenador": id_coordenador
        }
        registros_cursos.append(registro_curso)
        contador_id_curso += 1

resposta_cursos = supabase.table("cursos").upsert(registros_cursos).execute()
print("Cursos inseridos/atualizados:")
pprint(resposta_cursos.data)

cursos_por_departamento = {
    "computação": [
        "Engenharia de Computação", 
        "Ciência da Computação", 
        "Sistemas de Informação",
        "Redes de Computadores", 
        "Inteligência Artificial", 
        "Segurança da Informação", 
        "Computação Gráfica"
    ],
    "matemática": [
        "Matemática Pura", 
        "Matemática Aplicada", 
        "Estatística",
        "Análise Numérica", 
        "Geometria", 
        "Álgebra", 
        "Probabilidade"
    ],
    "física": [
        "Física Teórica", 
        "Física Experimental", 
        "Física Nuclear",
        "Astrofísica", 
        "Mecânica Quântica", 
        "Termodinâmica", 
        "Óptica"
    ],
    "química": [
        "Química Orgânica", 
        "Química Inorgânica", 
        "Química Analítica",
        "Bioquímica", 
        "Química Computacional", 
        "Química Ambiental", 
        "Físico-Química"
    ],
    "biologia": [
        "Biologia Celular", 
        "Genética", 
        "Ecologia",
        "Biotecnologia", 
        "Microbiologia", 
        "Zoologia", 
        "Botânica"
    ],
    "engenharia": [
        "Engenharia Civil", 
        "Engenharia de Produção", 
        "Engenharia de Computação",
        "Engenharia Mecânica", 
        "Engenharia Elétrica", 
        "Engenharia Química", 
        "Engenharia Ambiental"
    ],
    "administração": [
        "Administração de Empresas", 
        "Gestão Financeira", 
        "Marketing",
        "Recursos Humanos", 
        "Gestão de Projetos", 
        "Logística", 
        "Empreendedorismo"
    ],
    "letras": [
        "Letras - Inglês", 
        "Letras - Português", 
        "Letras - Espanhol",
        "Letras - Francês", 
        "Letras - Alemão", 
        "Letras - Italiano", 
        "Letras - Japonês"
    ]
}

disciplinas_por_curso = {
    "Engenharia de Computação": [
        "Fundamentos de Computação",
        "Programação Estruturada",
        "Estruturas de Dados",
        "Arquitetura de Computadores",
        "Sistemas Digitais",
        "Redes de Computadores",
        "Banco de Dados",
        "Engenharia de Software",
        "Sistemas Operacionais",
        "Projeto de Hardware e Software"
    ],
    "Ciência da Computação": [
        "Introdução à Computação",
        "Algoritmos e Estruturas de Dados",
        "Programação Avançada",
        "Sistemas Operacionais",
        "Banco de Dados",
        "Teoria da Computação",
        "Redes de Computadores",
        "Inteligência Artificial",
        "Computação Gráfica",
        "Segurança da Informação"
    ],
    "Sistemas de Informação": [
        "Fundamentos de Sistemas de Informação",
        "Análise de Sistemas",
        "Modelagem de Dados",
        "Desenvolvimento Web",
        "Banco de Dados",
        "Gestão de Projetos de TI",
        "Segurança da Informação",
        "Sistemas Distribuídos",
        "Inteligência de Negócios",
        "Tópicos em Sistemas de Informação"
    ],
    "Redes de Computadores": [
        "Fundamentos de Redes",
        "Protocolos de Comunicação",
        "Arquitetura de Redes",
        "Redes Sem Fio",
        "Segurança em Redes",
        "Redes de Dados",
        "Roteamento e Comutação",
        "Gerenciamento de Redes",
        "Otimização de Redes",
        "Tópicos Avançados em Redes"
    ],
    "Inteligência Artificial": [
        "Introdução à IA",
        "Aprendizado de Máquina",
        "Redes Neurais",
        "Processamento de Linguagem Natural",
        "Visão Computacional",
        "Robótica",
        "Mineração de Dados",
        "Ética em IA",
        "Sistemas Especialistas",
        "Tópicos Avançados em IA"
    ],
    "Segurança da Informação": [
        "Fundamentos de Segurança",
        "Criptografia",
        "Segurança de Redes",
        "Análise de Riscos",
        "Segurança em Sistemas Operacionais",
        "Segurança em Aplicações Web",
        "Gestão de Segurança da Informação",
        "Auditoria e Compliance",
        "Testes de Penetração",
        "Tópicos em Segurança da Informação"
    ],
    "Computação Gráfica": [
        "Introdução à Computação Gráfica",
        "Modelagem 3D",
        "Renderização",
        "Animação Digital",
        "Processamento de Imagens",
        "Iluminação e Sombreamento",
        "Computação Visual",
        "Realidade Virtual",
        "Tópicos em Gráficos Computacionais",
        "Projeto de Computação Gráfica"
    ],
    "Matemática Pura": [
        "Cálculo",
        "Lógica Matemática",
        "Álgebra Abstrata",
        "Teoria dos Números",
        "Geometria Euclidiana",
        "Análise Real",
        "Topologia",
        "Matemática Discreta",
        "História da Matemática",
        "Seminários em Matemática Pura"
    ],
    "Matemática Aplicada": [
        "Cálculo Diferencial",
        "Cálculo Integral",
        "Equações Diferenciais",
        "Álgebra Linear",
        "Métodos Numéricos",
        "Estatística Aplicada",
        "Cálculo",
        "Modelagem Matemática",
        "Análise Numérica",
        "Tópicos em Matemática Aplicada"
    ],
    "Estatística": [
        "Probabilidade",
        "Inferência Estatística",
        "Estatística Descritiva",
        "Cálculo",
        "Regressão e Correlação",
        "Amostragem",
        "Análise de Variância",
        "Estatística Computacional",
        "Séries Temporais",
        "Tópicos Avançados em Estatística"
    ],
    "Análise Numérica": [
        "Fundamentos de Análise Numérica",
        "Interpolação e Aproximação",
        "Resolução de Equações",
        "Métodos Iterativos",
        "Erros Numéricos",
        "Otimização Numérica",
        "Equações Diferenciais Numéricas",
        "Álgebra Numérica",
        "Análise de Convergência",
        "Tópicos em Análise Numérica"
    ],
    "Geometria": [
        "Geometria Plana",
        "Geometria Espacial",
        "Geometria Analítica",
        "Geometria Diferencial",
        "Transformações Geométricas",
        "Geometria Computacional",
        "Geometria Projetiva",
        "História da Geometria",
        "Cálculo",
        "Seminários em Geometria"
    ],
    "Álgebra": [
        "Fundamentos de Álgebra",
        "Álgebra Linear",
        "Equações e Inequações",
        "Cálculo",
        "Sistemas Lineares",
        "Álgebra Abstrata",
        "Polinômios",
        "Teoria dos Números",
        "Estruturas Algébricas",
        "Tópicos em Álgebra"
    ],
    "Probabilidade": [
        "Teoria da Probabilidade",
        "Variáveis Aleatórias",
        "Distribuições Probabilísticas",
        "Modelos Estocásticos",
        "Processos Estocásticos",
        "Inferência Bayesiana",
        "Probabilidade Aplicada",
        "Simulação de Monte Carlo",
        "Teoremas Limite",
        "Cálculo",
    ],
    "Física Teórica": [
        "Mecânica Clássica",
        "Eletromagnetismo",
        "Termodinâmica",
        "Física moderna",
        "Física Estatística",
        "Relatividade",
        "Física Matemática",
        "Tópicos em Física Teórica",
        "Métodos Matemáticos da Física",
        "Seminários em Física Teórica"
    ],
    "Física Experimental": [
        "Métodos Experimentais",
        "Análise de Dados Experimentais",
        "Física moderna",
        "Laboratório de Física",
        "Técnicas de Medição",
        "Erros e Incertezas",
        "Física Computacional",
        "Projetos Experimentais",
        "Tópicos em Física Experimental",
        "Seminários em Física Experimental"
    ],
    "Física Nuclear": [
        "Introdução à Física Nuclear",
        "Estrutura do Núcleo",
        "Radioatividade",
        "Reações Nucleares",
        "Física de Partículas",
        "Detectores Nucleares",
        "Modelos Nucleares",
        "Aplicações da Física Nuclear",
        "Física moderna",
        "Tópicos em Física Nuclear"
    ],
    "Astrofísica": [
        "Física moderna",
        "Cosmologia",
        "Estrutura Estelar",
        "Evolução Estelar",
        "Galáxias e Aglomerados",
        "Astrofísica Computacional",
        "Observação Astronômica",
        "Técnicas de Astrofísica",
        "Tópicos em Astrofísica",
        "Seminários em Astrofísica"
    ],
    "Mecânica Quântica": [
        "Fundamentos da Mecânica Quântica",
        "Álgebra de Operadores",
        "Equação de Schrödinger",
        "Física moderna",
        "Teoria das Medidas",
        "Tópicos Avançados em QM",
        "Aplicações da Mecânica Quântica",
        "Método Variacional",
        "Tópicos em Mecânica Quântica",
        "Seminários em QM"
    ],
    "Termodinâmica": [
        "Fundamentos da Termodinâmica",
        "Leis da Termodinâmica",
        "Processos Termodinâmicos",
        "Ciclos Termodinâmicos",
        "Máquinas Térmicas",
        "Entropia e Energia",
        "Processos Reversíveis e Irreversíveis",
        "Aplicações da Termodinâmica",
        "Tópicos em Termodinâmica",
        "Física moderna",
    ],
    "Óptica": [
        "Fundamentos da Óptica",
        "Geometria da Óptica",
        "Óptica Física",
        "Interferência e Difração",
        "Polarização",
        "Física moderna",
        "Lasers e Aplicações",
        "Instrumentos Ópticos",
        "Tópicos em Óptica",
        "Seminários em Óptica"
    ],
    "Química Orgânica": [
        "Estrutura Molecular",
        "Reações Orgânicas",
        "Química Orgânica Avançada",
        "Síntese Orgânica",
        "Tabela Periódica",
        "Química Orgânica Experimental",
        "Mecanismos Reacionais",
        "Química dos Polímeros",
        "Química Organometálica",
        "Seminários em Química Orgânica"
    ],
    "Química Inorgânica": [
        "Tabela Periódica",
        "Compostos Inorgânicos",
        "Estrutura dos Compostos Inorgânicos",
        "Ligação Química Inorgânica",
        "Química dos Metais",
        "Química dos Não-Metais",
        "Síntese Inorgânica",
        "Aplicações da Química Inorgânica",
        "Tópicos em Química Inorgânica",
        "Seminários em Química Inorgânica"
    ],
    "Química Analítica": [
        "Fundamentos de Química Analítica",
        "Técnicas de Análise",
        "Cromatografia",
        "Espectrometria",
        "Análise Instrumental",
        "Métodos Volumétricos",
        "Análise Estatística",
        "Controle de Qualidade",
        "Tópicos em Química Analítica",
        "Tabela Periódica"
    ],
    "Bioquímica": [
        "Fundamentos de Bioquímica",
        "Biomoléculas",
        "Metabolismo",
        "Enzimologia",
        "Bioenergética",
        "Tabela Periódica",
        "Bioquímica Clínica",
        "Sinalização Celular",
        "Tópicos em Bioquímica",
        "Seminários em Bioquímica"
    ],
    "Química Computacional": [
        "Introdução à Química Computacional",
        "Modelagem Molecular",
        "Métodos Computacionais em Química",
        "Simulações Moleculares",
        "Química Teórica Computacional",
        "Dinâmica Molecular",
        "Tabela Periódica",
        "Tópicos em Química Computacional",
        "Aplicações da Química Computacional",
        "Seminários em Química Computacional"
    ],
    "Química Ambiental": [
        "Fundamentos de Química Ambiental",
        "Poluição e Impactos Ambientais",
        "Química dos Contaminantes",
        "Monitoramento Ambiental",
        "Tratamento de Efluentes",
        "Tabela Periódica",
        "Impacto Ambiental de Produtos Químicos",
        "Tópicos em Química Ambiental",
        "Gestão Ambiental",
        "Seminários em Química Ambiental"
    ],
    "Físico-Química": [
        "Fundamentos de Físico-Química",
        "Termodinâmica Química",
        "Equilíbrio Químico",
        "Tabela Periódica",
        "Eletroquímica",
        "Propriedades dos Materiais",
        "Soluções e Colóides",
        "Tópicos em Físico-Química",
        "Métodos Espectroscópicos",
        "Seminários em Físico-Química"
    ],
    "Biologia Celular": [
        "Fundamentos de Biologia Celular",
        "Estrutura Celular",
        "Metabolismo Celular",
        "Divisão Celular",
        "Comunicação Celular",
        "Organelas e Funções",
        "Sinalização Celular",
        "Técnicas de Biologia Celular",
        "Tópicos em Biologia Celular",
        "Seminários em Biologia Celular"
    ],
    "Genética": [
        "Introdução à Genética",
        "Genética Mendeliana",
        "Genética Molecular",
        "Hereditariedade",
        "Evolução e Genética",
        "Genética Populacional",
        "Biotecnologia Genética",
        "Análise de DNA",
        "Estrutura Celular",
        "Seminários em Genética"
    ],
    "Ecologia": [
        "Fundamentos de Ecologia",
        "Ecossistemas",
        "Estrutura Celular",
        "Dinâmica Populacional",
        "Interações Ecológicas",
        "Conservação Ambiental",
        "Ecologia de Comunidades",
        "Tópicos em Ecologia",
        "Monitoramento Ambiental",
        "Seminários em Ecologia"
    ],
    "Biotecnologia": [
        "Estrutura Celular",
        "Técnicas Moleculares",
        "Cultura de Tecidos",
        "Engenharia Genética",
        "Aplicações da Biotecnologia",
        "Bioinformática",
        "Biotecnologia Industrial",
        "Tópicos em Biotecnologia",
        "Bioética",
        "Seminários em Biotecnologia"
    ],
    "Microbiologia": [
        "Fundamentos de Microbiologia",
        "Microrganismos",
        "Técnicas Microbiológicas",
        "Imunologia",
        "Estrutura Celular",
        "Fermentação e Bioprocessos",
        "Patógenos e Doenças",
        "Resistência Microbiana",
        "Tópicos em Microbiologia",
        "Seminários em Microbiologia"
    ],
    "Zoologia": [
        "Fundamentos de Zoologia",
        "Classificação Animal",
        "Anatomia Animal",
        "Fisiologia Animal",
        "Comportamento Animal",
        "Ecologia Animal",
        "Evolução Animal",
        "Tópicos em Zoologia",
        "Sistemática Animal",
        "Seminários em Zoologia"
    ],
    "Botânica": [
        "Introdução à Botânica",
        "Morfologia Vegetal",
        "Fisiologia Vegetal",
        "Estrutura Celular",
        "Ecologia Vegetal",
        "Genética Vegetal",
        "Fitopatologia",
        "Biotecnologia Vegetal",
        "Tópicos em Botânica",
        "Seminários em Botânica"
    ],
    "Engenharia Civil": [
        "Cálculo",
        "Materiais de Construção",
        "Mecânica dos Sólidos",
        "Geotecnia",
        "Hidráulica",
        "Planejamento e Gestão de Obras",
        "Desenho Técnico",
        "Estruturas de Concreto",
        "Estruturas Metálicas",
        "Projeto Integrado"
    ],
    "Engenharia de Produção": [
        "Fundamentos de Engenharia de Produção",
        "Gestão da Produção",
        "Pesquisa Operacional",
        "Planejamento e Controle da Produção",
        "Logística",
        "Cálculo",
        "Economia de Engenharia",
        "Métodos Quantitativos",
        "Engenharia de Processos",
        "Tópicos em Engenharia de Produção"
    ],
    "Engenharia de Computação": [
        "Fundamentos de Computação",
        "Programação Digital",
        "Sistemas Digitais",
        "Arquitetura de Computadores",
        "Eletrônica Digital",
        "Redes de Computadores",
        "Sistemas Embarcados",
        "Processamento de Sinais",
        "Cálculo",
        "Projeto Integrado em Computação"
    ],
    "Engenharia Mecânica": [
        "Desenho Mecânico",
        "Termodinâmica",
        "Cálculo",
        "Dinâmica",
        "Resistência dos Materiais",
        "Máquinas e Mecanismos",
        "Processos de Fabricação",
        "Projeto Mecânico",
        "Simulação em Engenharia Mecânica",
        "Tópicos em Engenharia Mecânica"
    ],
    "Engenharia Elétrica": [
        "Circuitos Elétricos",
        "Eletrônica Analógica",
        "Eletrônica Digital",
        "Sistemas de Energia",
        "Cálculo",
        "Controle de Processos",
        "Instrumentação Elétrica",
        "Redes Elétricas",
        "Automação Industrial",
        "Tópicos em Engenharia Elétrica"
    ],
    "Engenharia Química": [
        "Fundamentos de Engenharia Química",
        "Operações Unitárias",
        "Reações Químicas",
        "Termodinâmica Química",
        "Processos Químicos",
        "Engenharia de Reações",
        "Transferência de Massa",
        "Controle de Processos Químicos",
        "Cálculo",
        "Tópicos em Engenharia Química"
    ],
    "Engenharia Ambiental": [
        "Cálculo",
        "Controle da Poluição",
        "Tratamento de Água e Efluentes",
        "Gestão de Resíduos",
        "Impacto Ambiental",
        "Avaliação Ambiental",
        "Monitoramento Ambiental",
        "Legislação Ambiental",
        "Tópicos em Engenharia Ambiental",
        "Seminários em Engenharia Ambiental"
    ],
    "Administração de Empresas": [
        "Fundamentos de Administração",
        "Teoria da Administração",
        "Planejamento Estratégico",
        "Gestão de Pessoas",
        "Finanças Corporativas",
        "Marketing",
        "Logística e Operações",
        "Gestão da Produção",
        "Negócios Internacionais",
        "Empreendedorismo"
    ],
    "Gestão Financeira": [
        "Contabilidade Financeira",
        "Análise de Balanços",
        "Matemática Financeira",
        "Finanças Corporativas",
        "Investimentos",
        "Gestão de Riscos",
        "Mercado Financeiro",
        "Planejamento Financeiro",
        "Teoria da Administração",
        "Seminários em Gestão Financeira"
    ],
    "Marketing": [
        "Fundamentos de Marketing",
        "Comportamento do Consumidor",
        "Teoria da Administração",
        "Estratégias de Marketing",
        "Comunicação e Propaganda",
        "Marketing Digital",
        "Gestão de Marcas",
        "Vendas e Negociação",
        "Tópicos em Marketing",
        "Seminários em Marketing"
    ],
    "Recursos Humanos": [
        "Gestão de Pessoas",
        "Recrutamento e Seleção",
        "Treinamento e Desenvolvimento",
        "Gestão de Desempenho",
        "Legislação Trabalhista",
        "Relações Trabalhistas",
        "Administração de Pessoal",
        "Comunicação Interna",
        "Teoria da Administração",
        "Seminários em Recursos Humanos"
    ],
    "Gestão de Projetos": [
        "Fundamentos de Gestão de Projetos",
        "Planejamento e Controle",
        "Métodos Ágeis",
        "Gerenciamento de Riscos",
        "Teoria da Administração",
        "Ferramentas de Gestão",
        "Estrutura Analítica de Projetos",
        "Comunicação em Projetos",
        "Tópicos em Gestão de Projetos",
        "Estudos de Caso em Projetos"
    ],
    "Logística": [
        "Fundamentos de Logística",
        "Gestão da Cadeia de Suprimentos",
        "Transporte e Distribuição",
        "Armazenagem e Estoques",
        "Logística Internacional",
        "Sistemas de Informação Logística",
        "Teoria da Administração",
        "Tópicos em Logística",
        "Gestão de Riscos Logísticos",
        "Seminários em Logística"
    ],
    "Empreendedorismo": [
        "Teoria da Administração",
        "Criação de Novos Negócios",
        "Gestão da Inovação",
        "Plano de Negócios",
        "Finanças para Empreendedores",
        "Marketing para Startups",
        "Estratégias Empreendedoras",
        "Desenvolvimento de Produtos",
        "Tópicos em Empreendedorismo",
        "Laboratório de Empreendedorismo"
    ],
    "Letras - Inglês": [
        "Linguística Geral",
        "Fonética e Fonologia",
        "Literatura Inglesa",
        "Escrita e Composição",
        "Análise de Textos",
        "Tradução e Interpretação",
        "História da Língua Inglesa",
        "Cultura Anglo-Saxônica",
        "Tópicos em Linguística",
        "Seminários em Literatura Inglesa"
    ],
    "Letras - Português": [
        "Literatura Brasileira",
        "Literatura Portuguesa",
        "Teoria Literária",
        "Linguística Aplicada",
        "Crítica Literária",
        "Redação e Comunicação",
        "História da Língua Portuguesa",
        "Estudos Culturais",
        "Tópicos em Literatura",
        "Seminários em Literatura Brasileira"
    ],
    "Letras - Espanhol": [
        "Literatura Hispânica",
        "Gramática Espanhola",
        "Cultura e História da Espanha",
        "Linguística Hispânica",
        "Tradução e Interpretação",
        "Redação em Espanhol",
        "Literatura Contemporânea",
        "Tópicos em Cultura Hispânica",
        "Expressão Oral e Escrita",
        "Seminários em Literatura Hispânica"
    ],
    "Letras - Francês": [
        "Literatura Francesa",
        "Gramática Francesa",
        "Filosofia e Cultura Francesa",
        "Redação em Francês",
        "Expressão Oral em Francês",
        "Análise Literária",
        "História da Literatura Francesa",
        "Tópicos em Cultura Francesa",
        "Tradução e Interpretação",
        "Seminários em Literatura Francesa"
    ],
    "Letras - Alemão": [
        "Literatura Alemã",
        "Gramática Alemã",
        "História da Língua Alemã",
        "Filosofia Alemã",
        "Redação em Alemão",
        "Expressão Oral e Escrita",
        "Análise Textual",
        "Tópicos em Literatura Alemã",
        "Tradução e Interpretação",
        "Seminários em Literatura Alemã"
    ],
    "Letras - Italiano": [
        "Literatura Italiana",
        "Gramática Italiana",
        "História da Literatura Italiana",
        "Redação em Italiano",
        "Expressão Oral em Italiano",
        "Análise Literária",
        "Tópicos em Cultura Italiana",
        "Tradução e Interpretação",
        "Tópicos em Literatura Italiana",
        "Seminários em Literatura Italiana"
    ],
    "Letras - Japonês": [
        "Literatura Japonesa",
        "Gramática Japonesa",
        "Cultura Japonesa",
        "Escrita e Kanji",
        "História do Japão",
        "Tradução e Interpretação",
        "Filosofia Japonesa",
        "Tópicos em Cultura Japonesa",
        "Expressão Oral e Escrita",
        "Seminários em Literatura Japonesa"
    ]
}

def gerar_abreviacao(nome_curso: str) -> str:
    """
    Gera uma abreviação para o curso removendo palavras comuns e utilizando:
      - Se houver pelo menos duas palavras relevantes: usa a primeira letra de cada uma.
      - Caso contrário: usa os dois primeiros caracteres do nome.
    """
    palavras_comuns = {"de", "da", "do", "dos", "das", "e", "-", "em"}
    palavras = nome_curso.split()
    relevantes = [palavra for palavra in palavras if palavra.lower() not in palavras_comuns]
    
    if len(relevantes) >= 2:
        abreviacao = relevantes[0][0] + relevantes[1][0]
    elif len(relevantes) == 1:
        abreviacao = relevantes[0][:2]
    else:
        abreviacao = nome_curso[:2]
    
    return abreviacao.upper()

resposta_departamentos = supabase.table("departamentos").select("id_departamento, nome").execute()
departamentos_existentes = {dep["id_departamento"]: dep["nome"] for dep in resposta_departamentos.data}

resposta_cursos = supabase.table("cursos").select("id_curso, nome, id_departamento").execute()
cursos = resposta_cursos.data

registros_disciplinas = []
disciplina_serial_atual = 1

for curso in cursos:
    id_curso = curso["id_curso"]
    nome_curso = curso["nome"]
    id_departamento = curso["id_departamento"]
    
    if id_departamento not in departamentos_existentes:
        continue

    if nome_curso not in disciplinas_por_curso:
        continue

    abbrev = gerar_abreviacao(nome_curso)
    lista_disciplinas = disciplinas_por_curso[nome_curso]
    
    for i in range(1, 11):
        id_disciplina = f"{abbrev}-{id_curso:03d}-{i:03d}"
        nome_disciplina = lista_disciplinas[i - 1]
        carga_horaria = random.randint(1, 5)

        registro = {
            "id_disciplina": id_disciplina,
            "nome": nome_disciplina,
            "carga_horaria": carga_horaria,
            "disciplina_serial": disciplina_serial_atual
        }
        registros_disciplinas.append(registro)
        
        disciplina_serial_atual += 1

if registros_disciplinas:
    resposta_disciplinas = supabase.table("disciplinas").upsert(
        registros_disciplinas,
        on_conflict=["disciplina_serial"]
    ).execute()
    print("Disciplinas inseridas/atualizadas:")
    pprint(resposta_disciplinas.data)
else:
    print("Nenhum registro de disciplina foi gerado.")

periodos = ["manhã", "tarde", "noite"]

resposta_cursos = supabase.table("cursos").select("id_curso, nome").execute()
cursos = resposta_cursos.data

registros_curso_disciplina = []

for curso in cursos:
    id_curso = curso["id_curso"]
    nome_curso = curso["nome"]
    abbrev = gerar_abreviacao(nome_curso)
    
    for i in range(1, 11):
        id_disciplina = f"{abbrev}-{id_curso:03d}-{i:03d}"
        periodo = random.choice(periodos)
        registro = {
            "id_curso": id_curso,
            "id_disciplina": id_disciplina,
            "periodo": periodo
        }
        registros_curso_disciplina.append(registro)

if registros_curso_disciplina:
    resposta_curso_disciplina = supabase.table("curso_disciplina").upsert(registros_curso_disciplina).execute()
    print("Registros inseridos/atualizados na tabela 'curso_disciplina':")
    pprint(resposta_curso_disciplina.data)
else:
    print("Nenhum registro foi gerado para a tabela 'curso_disciplina'.")

primeiros_nomes = [
    "Alice", "Bruno", "Carlos", "Daniela", "Eduardo", "Fabiana", "Gabriel", "Helena",
    "Igor", "Juliana", "Kevin", "Laura", "Marcos", "Natália", "Otávio", "Paula", "Quintino", 
    "Rafael", "Sabrina", "Thiago", "Úrsula", "Vinícius", "Wagner", "Ximena", "Yuri",
    "Zuleica", "André", "Beatriz", "César", "Diana", "Enzo", "Flávia", "Gustavo",
    "Heloísa", "Isadora", "Jonas", "Karen", "Leandro", "Mirela", "Nicolas", "Olívia",
    "Pedro", "Quezia", "Renato", "Sara", "Tiago", "Úrsula", "Valéria", "William"
]

sobrenomes = [
    "Silva", "Souza", "Oliveira", "Pereira", "Lima", "Costa", "Rodrigues", "Almeida",
    "Nascimento", "Gomes", "Martins", "Ribeiro", "Carvalho", "Fernandes", "Rocha", 
    "Barbosa", "Mendes", "Araújo", "Teixeira", "Ramos", "Dias", "Correia", "Melo", 
    "Castro", "Borges", "Vasconcelos", "Pinto", "Santos", "Moraes", "Moreira", "Cardoso",
    "Lacerda", "Monteiro", "Gonçalves", "Farias", "Vieira", "Pacheco", "Rezende", 
    "Assis", "Batista", "Freitas", "Leite", "Nascimento", "Macedo", "Duarte", "Guimarães",
    "Menezes", "Guerra", "Barros", "Siqueira", "Ferraz", "Peixoto", "Aguiar", "Amaral",
    "Valente", "Baptista", "Carneiro", "Cavalcante", "Campos", "Dantas", "Furtado", 
    "Galvão", "Moura", "Novais", "Peixoto", "Queiroz", "Salgado", "Santana", "Soares",
    "Tavares", "Uchoa", "Viegas", "Xavier", "Yamamoto", "Zagallo", "Aragão", "Brito",
    "Cunha", "Drumond", "Esteves", "Ferreira", "Gentil", "Helena", "Ibrahim", "Jardim",
    "Klein", "Lima", "Machado", "Nogueira", "Ortega", "Peres", "Quintana", "Ramalho"
]

resposta_professores = supabase.table("professores").select("nome").execute()
nomes_professores = {prof["nome"] for prof in resposta_professores.data}

resposta_cursos = supabase.table("cursos").select("id_curso").execute()
lista_cursos = [curso["id_curso"] for curso in resposta_cursos.data]
if not lista_cursos:
    raise Exception("Nenhum curso encontrado para atribuição aos alunos.")

alunos_registros = []
nomes_usados = set() 

idades_intervalo = [random.randint(17, 22) for _ in range(240)]
idades_rand = [random.randint(17, 35) for _ in range(160)]
lista_idades = idades_intervalo + idades_rand
random.shuffle(lista_idades)

contador = 1
while len(alunos_registros) < 400:
    nome = random.choice(primeiros_nomes)
    sobrenome1, sobrenome2 = random.sample(sobrenomes, 2)
    nome_completo = f"{nome} {sobrenome1} {sobrenome2}"
    
    if nome_completo in nomes_usados or nome_completo in nomes_professores:
        continue

    nomes_usados.add(nome_completo)
    
    email = (nome + sobrenome1 + sobrenome2).replace(" ", "").lower() + "@gmail.com"
    
    id_curso = random.choice(lista_cursos)
    
    idade = lista_idades[len(alunos_registros)]
    
    registro_aluno = {
        "id_aluno": contador,
        "nome": nome_completo,
        "email": email,
        "id_curso": id_curso,
        "idade": idade
    }
    alunos_registros.append(registro_aluno)
    contador += 1

if alunos_registros:
    resposta_alunos = supabase.table("alunos").upsert(alunos_registros).execute()
    print("Alunos inseridos/atualizados:")
    pprint(resposta_alunos.data)
else:
    print("Nenhum registro de aluno foi gerado.")

resposta_professores = supabase.table("professores").select("id_professor").execute()
professores = resposta_professores.data

resposta_disciplinas = supabase.table("disciplinas").select("id_disciplina, disciplina_serial").execute()
disciplinas = resposta_disciplinas.data


num_professores = len(professores)
num_disciplinas = len(disciplinas)

if num_disciplinas != 200:
    raise Exception(f"O número de disciplinas deve ser 200, mas há {num_disciplinas} disciplinas.")
if num_professores == 0:
    raise Exception("Não há professores cadastrados.")

disciplinas_por_professor = {prof["id_professor"]: 1 for prof in professores}

disciplinas_restantes = num_disciplinas - num_professores

while disciplinas_restantes > 0:
    for professor in professores:
        if disciplinas_restantes == 0:
            break
        if disciplinas_por_professor[professor["id_professor"]] < 3:
            disciplinas_por_professor[professor["id_professor"]] += 1
            disciplinas_restantes -= 1

total_disciplinas = sum(disciplinas_por_professor.values())
print(f"Total de disciplinas distribuídas: {total_disciplinas} (deve ser 200)")

disciplinaslecionadas_registros = supabase.table("disciplinaslecionadas").select("id_disciplina, id_professor").execute().data
for registro in disciplinaslecionadas_registros:
    supabase.table("disciplinaslecionadas").delete()\
        .eq("id_disciplina", registro["id_disciplina"])\
        .eq("id_professor", registro["id_professor"]).execute()

print("Tabela 'disciplinaslecionadas' limpa com sucesso.")

registros_disciplinas_lecionadas = []

for professor in professores:
    num_disciplinas_professor = disciplinas_por_professor[professor["id_professor"]]
    disciplinas_selecionadas = random.sample(disciplinas, num_disciplinas_professor)
    
    for disciplina in disciplinas_selecionadas:
        registro_discip_lecionada = {
            "id_professor": professor["id_professor"],
            "id_disciplina": disciplina["id_disciplina"],
            "disciplina_serial": disciplina["disciplina_serial"]
        }
        registros_disciplinas_lecionadas.append(registro_discip_lecionada)

if registros_disciplinas_lecionadas:
    resposta_disciplinas_lecionadas = supabase.table("disciplinaslecionadas").upsert(registros_disciplinas_lecionadas).execute()
    print("Disciplinas lecionadas inseridas/atualizadas:")
    pprint(resposta_disciplinas_lecionadas.data)
else:
    print("Nenhum registro de disciplina lecionada foi gerado.")

alunos = supabase.table("alunos").select("id_aluno, id_curso").execute().data

cursos_disciplinas = {}
resposta_cursos = supabase.table("curso_disciplina").select("id_curso, id_disciplina").order("id_disciplina").execute()
for item in resposta_cursos.data:
    if item["id_curso"] not in cursos_disciplinas:
        cursos_disciplinas[item["id_curso"]] = []
    cursos_disciplinas[item["id_curso"]].append(item["id_disciplina"])

def simular_historico(aluno):
    historico = []
    id_aluno = aluno["id_aluno"]
    id_curso = aluno["id_curso"]
    
    disciplinas = cursos_disciplinas.get(id_curso, [])
    
    situacao = {
        'aprovadas': set(),
        'reprovadas': [],
        'semestre_atual': 1,
        'carga_semestre': 2 
    }
    
    while len(situacao['aprovadas']) < 10:
        novas = disciplinas[(situacao['semestre_atual']-1)*2 : situacao['semestre_atual']*2]
        cursar = [d for d in novas if d not in situacao['aprovadas']] + situacao['reprovadas']
        situacao['reprovadas'] = []
        
        for disc in cursar:
            if random.random() < 0.7:
                nota = round(random.uniform(5.0, 10.0), 1)
                status = "Aprovado!"
                situacao['aprovadas'].add(disc)
            else:
                nota = round(random.uniform(0.0, 4.9), 1)
                status = "Reprovado!"
                situacao['reprovadas'].append(disc)
            
            historico.append({
                "id_aluno": id_aluno,
                "id_disciplina": disc,
                "semestre": str(situacao['semestre_atual']),
                "nota": float(nota),
                "status": status
            })
        
        situacao['semestre_atual'] += 1
    
    return historico

for aluno in alunos:
    historico = simular_historico(aluno)
    if historico:
        supabase.table("historicoescolar").upsert(historico).execute()
        print(f"Histórico gerado para aluno {aluno['id_aluno']}")

print("Históricos escolares gerados com sucesso!")

assuntos_por_curso = {
    "Engenharia de Computação": [
        "Sistemas embarcados para monitoramento de infraestrutura urbana",
        "Otimização energética em data centers usando IA",
        "Desenvolvimento de veículos autônomos para ambientes hostis",
        "Integração de blockchain em sistemas de votação digital",
        "Sensores inteligentes para agricultura de precisão",
        "Modelagem de sistemas ciber-físicos para manufatura 4.0"
    ],
    "Ciência da Computação": [
        "Algoritmos bioinspirados para problemas de roteamento",
        "Análise de dados genômicos usando computação distribuída",
        "Framework para detecção de deepfakes em tempo real",
        "Otimização de redes neurais para hardware de baixo consumo",
        "Sistemas de recomendação contextual para educação",
        "Modelagem preditiva de pandemias usando agentes inteligentes"
    ],
    "Sistemas de Informação": [
        "Plataforma integrada para cidades inteligentes",
        "Sistemas ERP adaptativos para PMEs",
        "Framework para compliance com LGPD em big data",
        "Análise de sentimentos em atendimento ao cliente",
        "Sistemas de business intelligence para saúde pública",
        "Gestão de identidade digital baseada em blockchain"
    ],
    "Redes de Computadores": [
        "Arquitetura SDN para redes 5G de baixa latência",
        "Protótipo de rede mesh para comunidades isoladas",
        "Monitoramento preditivo de falhas em redes ópticas",
        "Segurança em comunicações quânticas distribuídas",
        "Otimização de QoS em redes de IoT massiva",
        "Técnicas de detecção de intrusão em redes 6G"
    ],
    "Inteligência Artificial": [
        "Modelos generativos para criação de fármacos",
        "Sistemas multiagente para gestão de desastres",
        "Explicabilidade de modelos de deep learning médico",
        "Aprendizado por reforço em robótica subaquática",
        "Otimização de cadeias logísticas com IA evolutiva",
        "Detecção de fake news usando processamento multimodal"
    ],
    "Segurança da Informação": [
        "Framework para resposta a incidentes cibernéticos",
        "Análise forense em dispositivos IoT comprometidos",
        "Proteção de dados em computação edge federada",
        "Técnicas de anonymização em datasets sensíveis",
        "Modelagem de ameaças para sistemas de energia crítica",
        "Autenticação biométrica contínua em dispositivos móveis"
    ],
    "Computação Gráfica": [
        "Renderização realista para treinamento médico VR",
        "Técnicas de upscaling neural para patrimônio histórico",
        "Simulação física de materiais para engenharia",
        "Geração procedural de ecossistemas virtuais",
        "Otimização de ray tracing em GPUs heterogêneas",
        "Reconstrução 3D a partir de imagens 2D médicas"
    ],

    "Matemática Pura": [
        "Teoria das categorias aplicada à computação quântica",
        "Análise não-standard em problemas de infinitésimos",
        "Estruturas algébricas em teorias de gauge unificadas",
        "Topologia diferencial em sistemas dinâmicos complexos",
        "Teoria dos números aplicada à criptografia pós-quântica",
        "Geometria não-euclidiana em modelos cosmológicos"
    ],
    "Matemática Aplicada": [
        "Modelos estocásticos para previsão de crises hídricas",
        "Otimização combinatória em redes de transporte urbano",
        "Análise de dados funcionais em monitoramento climático",
        "Equações integro-diferenciais em dinâmica populacional",
        "Métodos numéricos para simulação de fusão nuclear",
        "Teoria dos jogos aplicada a mercados de energia"
    ],
    "Estatística": [
        "Inferência causal em estudos observacionais de saúde",
        "Modelos bayesianos hierárquicos para epidemiologia",
        "Análise de sobrevivência em falhas de equipamentos",
        "Técnicas de bootstrap em finanças de alta frequência",
        "Estatística espacial para mapeamento de crimes",
        "Controle estatístico de qualidade 4.0"
    ],
    "Análise Numérica": [
        "Métodos espectrales para equações de onda não-lineares",
        "Algoritmos paralelos para problemas de autovalores",
        "Malhas adaptativas em simulação de escoamentos",
        "Estabilidade numérica em aprendizado de máquina",
        "Métodos de elementos finitos para nanoestruturas",
        "Otimização de códigos numéricos para GPUs"
    ],
    "Geometria": [
        "Variedades simpléticas em mecânica clássica",
        "Tesselações não-periódicas em materiais avançados",
        "Geometria fractal em análise de redes complexas",
        "Grupos de transformação em cristalografia",
        "Geometria diferencial em relatividade numérica",
        "Topologia algébrica em processamento de dados"
    ],
    "Álgebra": [
        "Teoria de representações em física de partículas",
        "Álgebras de Lie na teoria de controle quântico",
        "Módulos projetivos em criptografia homomórfica",
        "Teoria de Galois inversa em sistemas dinâmicos",
        "Álgebras de operadores em aprendizado profundo",
        "Estruturas reticuladas em otimização discreta"
    ],
    "Probabilidade": [
        "Processos de Lévy em modelagem de mercados",
        "Teoria ergódica em sistemas biológicos",
        "Cálculo Malliavin em finanças matemática",
        "Percolação em redes sociais complexas",
        "Medidas aleatórias em processamento de sinais",
        "Teoria de grandes desvios em ecologia"
    ],

"Física Teórica": [
        "Teoria das cordas em espaços anti-de Sitter",
        "Matéria escura em modelos supersimétricos",
        "Eletrodinâmica quântica em materiais topológicos",
        "Transições de fase em sistemas fora do equilíbrio",
        "Gravitação quântica em loops aplicada a cosmologia",
        "Teoria de campos conformes em fenômenos críticos"
    ],
    "Física Experimental": [
        "Detecção de raios cósmicos ultraenergéticos",
        "Espectroscopia de múons em materiais exóticos",
        "Armadilhas magnéticas para antimatéria",
        "Criogenia aplicada a detectores de partículas",
        "Metrologia de precisão em testes de relatividade",
        "Plasmas confinados por laser para fusão nuclear"
    ],
    "Física Nuclear": [
        "Reações nucleares em estrelas de nêutrons",
        "Detectores semicondutores para raios gama",
        "Modelagem de decaimentos radioativos exóticos",
        "Aplicações médicas de feixes de íons pesados",
        "Simulação Monte Carlo de reatores nucleares",
        "Espectroscopia de nêutrons em materiais funcionais"
    ],
    "Astrofísica": [
        "Formação de galáxias em simulações cosmológicas",
        "Magnetohidrodinâmica em discos de acreção",
        "Assinaturas espectrais de exoplanetas habitáveis",
        "Evolução estelar em aglomerados globulares",
        "Ondas gravitacionais de buracos negros binários",
        "Química interestelar em regiões de formação estelar"
    ],
    "Mecânica Quântica": [
        "Emaranhamento quântico em sistemas muitos-corpos",
        "Teorema de Bell em experimentos de fotônicos",
        "Computação quântica com íons aprisionados",
        "Efeito Hall quântico fracionário em grafeno",
        "Decoerência em sistemas quânticos macroscópicos",
        "Simulações quânticas em átomos ultrafrios"
    ],
    "Termodinâmica": [
        "Máquinas térmicas em regime quântico",
        "Teoria de resposta linear em sistemas biológicos",
        "Transporte de calor em nanoestruturas",
        "Eficiência máxima em motores microscópicos",
        "Transições de fase em redes complexas",
        "Termodinâmica de buracos negros primordiais"
    ],
    "Óptica": [
        "Vórtices ópticos em comunicação quântica",
        "Metamateriais para invisibilidade ativa",
        "Laser de elétrons livres para imageamento médico",
        "Óptica não-linear em cristais fotônicos",
        "Twistrônica com polaritons de superfície",
        "Holografia digital para armazenamento de dados"
    ],

    "Química Orgânica": [
        "Síntese assimétrica de fármacos quirais",
        "Catalisadores organometálicos sustentáveis",
        "Dendrímeros para entrega controlada de medicamentos",
        "Reações click chemistry em bioconjugação",
        "Materiais porosos orgânicos para captura de CO2",
        "Fotocatalisadores para degradação de poluentes"
    ],
    "Química Inorgânica": [
        "Clusteres moleculares para armazenamento de hidrogênio",
        "Complexos luminescentes para OLEDs eficientes",
        "Nanopartículas magnéticas em hipertermia cancerígena",
        "Marcadores de MRI baseados em lantanídeos",
        "Eletrocatalisadores para produção de amônia verde",
        "Estruturas metal-orgânicas para dessalinização"
    ],
    "Química Analítica": [
        "Microscopia de sonda local em análise forense",
        "Sensores eletroquímicos vestíveis para saúde",
        "Espectrometria de massas ambientais em tempo real",
        "Métodos cromatográficos para doping esportivo",
        "Técnicas de fingerprinting em alimentos orgânicos",
        "Automação de análises laboratoriais com IA"
    ],
    "Bioquímica": [
        "Engenharia de vias metabólicas para biocombustíveis",
        "Mecanismos moleculares de doenças neurodegenerativas",
        "Aptâmeros para diagnóstico rápido de patógenos",
        "Dinâmica conformacional de proteínas membranares",
        "Sistemas enzimáticos artificiais para química verde",
        "Modulação alostérica em receptores farmacológicos"
    ],
    "Química Computacional": [
        "Machine learning em triagem virtual de fármacos",
        "Dinâmica molecular de membranas celulares",
        "Métodos ab initio para estados excitados moleculares",
        "Modelagem de catálise heterogênea em superfícies",
        "Algoritmos quânticos para problemas químicos",
        "Simulação de agregados moleculares em solventes"
    ],
    "Química Ambiental": [
        "Nanoremediação de solos contaminados",
        "Biossensores para monitoramento de microplásticos",
        "Processos avançados de oxidação para efluentes",
        "Química atmosférica de poluentes emergentes",
        "Valorização de resíduos agroindustriais",
        "Materiais sustentáveis para tratamento de água"
    ],
    "Físico-Química": [
        "Dinâmica de reações ultrarápidas com lasers",
        "Efeitos de confinamento em nanoporos",
        "Espectroscopia de superfície em catálise",
        "Auto-organização em sistemas moleculares complexos",
        "Transporte iônico em baterias de estado sólido",
        "Termodinâmica de soluções iônicas profundas"
    ],
    "Biologia Celular": [
        "Mecanismos de senescência celular reversível",
        "Transporte vesicular em neurônios humanos",
        "Dinâmica de organelas em células cancerígenas",
        "Sinalização cálcica em respostas imunes inatas",
        "Biogênese de peroxissomos em plantas transgênicas",
        "Técnicas de super-resolução em imageamento celular"
    ],
    "Genética": [
        "Edição gênica CRISPR em doenças monogênicas",
        "Epigenética do desenvolvimento em ambientes extremos",
        "Genômica populacional de espécies ameaçadas",
        "Regulação pós-transcricional em câncer de mama",
        "Elementos transponíveis no envelhecimento",
        "Marcadores moleculares para melhoramento vegetal"
    ],
    "Ecologia": [
        "Serviços ecossistêmicos em áreas urbanizadas",
        "Redes tróficas em ambientes de extremófilos",
        "Efeito de borda em fragmentos florestais",
        "Biomonitoramento de rios usando macroinvertebrados",
        "Dinâmica metapopulacional em mudanças climáticas",
        "Restauração ecológica de manguezais degradados"
    ],
    "Biotecnologia": [
        "Produção de bioplásticos por microrganismos",
        "Biorreatores para cultivo de células animais",
        "Vacinas comestíveis em plantas transgênicas",
        "Enzimas extremófilas em processos industriais",
        "Terapia gênica com vetores virais seguros",
        "Biosensores nanoestruturados para diagnóstico"
    ],
    "Microbiologia": [
        "Resistência antimicrobiana em ambientes hospitalares",
        "Consórcios microbianos para biorremediação",
        "Viroma de ecossistemas extremos",
        "Interações patógeno-hospedeiro em zoonoses",
        "Metabolismo microbiano em condições de microgravidade",
        "Probióticos para modulação da microbiota intestinal"
    ],
    "Zoologia": [
        "Bioacústica em comunicação animal",
        "Adaptações fisiológicas em altitude elevada",
        "Comportamento social em primatas não-humanos",
        "Mimetismo em artrópodes neotropicais",
        "Fisiologia térmica de répteis desertícolas",
        "Técnicas não-invasivas para estudos de campo"
    ],
    "Botânica": [
        "Fisiologia do estresse em plantas cactáceas",
        "Interações planta-polinizador em biomas ameaçados",
        "Metabolismo secundário em espécies medicinais",
        "Adaptações morfológicas em epífitas vasculares",
        "Sinalização hormonal em respostas a patógenos",
        "Bancos de sementes para conservação ex situ"
    ],

    "Engenharia Civil": [
        "Materiais autocicatrizantes para infraestrutura",
        "Modelagem BIM para cidades resilientes",
        "Técnicas de retrofit sísmico em edifícios históricos",
        "Pavimentos permeáveis para drenagem urbana",
        "Estruturas tensionadas para habitats lunares",
        "Gestão de resíduos na construção modular"
    ],
    "Engenharia de Produção": [
        "Indústria 4.0 em cadeias de suprimentos agrícolas",
        "Logística reversa de equipamentos eletrônicos",
        "Simulação discreta para hospitais inteligentes",
        "Lean manufacturing em pequenas empresas",
        "Gestão da qualidade em produtos biotecnológicos",
        "Economia circular na manufatura aditiva"
    ],
    "Engenharia Mecânica": [
        "Turbinas eólicas de eixo vertical urbano",
        "Materiais compósitos para mobilidade sustentável",
        "Sistemas de refrigeração por mudança de fase",
        "Manufatura digital em próteses personalizadas",
        "Análise de falhas em componentes aeronáuticos",
        "Robótica colaborativa em linhas de montagem"
    ],
    "Engenharia Elétrica": [
        "Microredes inteligentes com armazenamento híbrido",
        "Sensoriamento óptico em subestações digitais",
        "Conversores estáticos para veículos elétricos",
        "Proteção diferencial em redes com DERs",
        "Eficiência energética em data centers",
        "Controle preditivo em sistemas fotovoltaicos"
    ],
    "Engenharia Química": [
        "Biorrefinarias integradas para biocombustíveis",
        "Membranas avançadas para separação de gases",
        "Reatores microfluídicos para síntese farmacêutica",
        "Processos intensificados para hidrogênio verde",
        "Modelagem CFD em colunas de destilação",
        "Técnicas de encapsulamento para liberação controlada"
    ],
    "Engenharia Ambiental": [
        "Recuperação de áreas mineradas com espécies nativas",
        "Tecnologias para tratamento de chorume",
        "Pegada hídrica em processos industriais",
        "Sistemas alagados construídos para esgoto rural",
        "Modelagem da dispersão de poluentes atmosféricos",
        "Indicadores de sustentabilidade para municípios"
    ],
    "Engenharia de Computação": [
        "Otimização de Algoritmos para Sistemas Embarcados",
        "Machine Learning Aplicado à Robótica Autônoma",
        "Desenvolvimento de Sistemas IoT para Cidades Inteligentes",
        "Segurança Cibernética em Redes Industriais",
        "Realidade Virtual Aplicada à Educação",
        "Análise de Big Data para Sistemas de Transporte",
        "Arquitetura de Computadores de Alta Performance",
        "Blockchain para Contratos Inteligentes"
    ],
    "Administração de Empresas": [
        "Modelos de governança para startups de impacto",
        "Inteligência competitiva em mercados emergentes",
        "Gestão do conhecimento em organizações remotas",
        "Fusões e aquisições no setor de tecnologia",
        "Liderança adaptativa em contextos de crise",
        "Estratégias de internacionalização para PMEs"
    ],
    "Gestão Financeira": [
        "Finanças comportamentais em investimentos ESG",
        "Modelos preditivos para risco de crédito",
        "Criptoativos em carteiras institucionais",
        "Hedge accounting em commodities agrícolas",
        "Fintechs e inclusão financeira periférica",
        "Otimização tributária em operações internacionais"
    ],
    "Marketing": [
        "Neuromarketing aplicado a embalagens sustentáveis",
        "Influenciadores digitais em nichos especializados",
        "Gamificação em programas de fidelização",
        "Marketing sensorial em experiências omnichannel",
        "Narrativas de marca para geração Z",
        "Inteligência artificial em personalização em massa"
    ],
    "Recursos Humanos": [
        "Seleção por competências para trabalhos híbridos",
        "Plataformas de upskilling para indústria 4.0",
        "Diversidade geracional em equipes multiculturais",
        "Wellbeing corporativo em home office prolongado",
        "Análise de dados para retenção de talentos",
        "Liderança feminina em setores tradicionalmente masculinos"
    ],
    "Gestão de Projetos": [
        "Metodologias ágeis em projetos de impacto social",
        "Gerenciamento de riscos em megaprojetos de infraestrutura",
        "Ferramentas colaborativas para equipes distribuídas",
        "Indicadores de maturidade em PMOs governamentales",
        "Adaptação de frameworks em contextos não-software",
        "Gestão de portfólio em organizações de pesquisa"
    ],
    "Logística": [
        "Last mile delivery com veículos autônomos",
        "Blockchain para rastreabilidade em cadeias globais",
        "Otimização de rotas com restrições sanitárias",
        "Logística humanitária em desastres climáticos",
        "Armazéns automatizados para e-commerce rápido",
        "Modelos de compartilhamento em logística urbana"
    ],
    "Empreendedorismo": [
        "Startups de base tecnológica em regiões periféricas",
        "Modelos canvas para negócios de impacto ambiental",
        "Financiamento coletivo para inovações sociais",
        "Estratégias de pivotagem em contextos de crise",
        "Ecossistemas de inovação em cidades médias",
        "Intraempreendedorismo em corporações tradicionais"
    ],

    "Letras - Português": [
        "Análise crítica do discurso político digital",
        "Tradução intersemiótica em graphic novels",
        "Variação linguística em comunidades quilombolas",
        "Literatura marginal e periferias urbanas",
        "Ensino de português para refugiados venezuelanos",
        "Corpus linguístico de redes sociais brasileiras"
    ],
    "Letras - Inglês": [
        "Representação de gênero em literatura pós-colonial",
        "Aquisição de segunda língua em ambientes imersivos",
        "Análise contrastiva de phrasal verbs em traduções",
        "Linguística de corpus aplicada ao inglês jurídico",
        "Transcriação em localização de videogames",
        "Ensino de pronúncia para falantes de línguas tonais"
    ],
    "Letras - Espanhol": [
        "Dialetologia andina em contextos migratórios",
        "Tradução de realia culturais em literatura latino-americana",
        "Análise de discurso em mídias hispânicas",
        "Ensino de ELE para falantes de português",
        "Linguística histórica do espanhol americano",
        "Representações identitárias no boom latino-americano"
    ],
    "Letras - Francês": [
        "Ensino de FLE através de bandes dessinées",
        "Análise de discurso em textos diplomáticos francófonos",
        "Tradução comentada de Nouveau Roman",
        "Sociolinguística das variedades africanas do francês",
        "Intercompreensão entre línguas românicas",
        "Literaturas francófonas do Maghreb contemporâneo"
    ],
    "Letras - Alemão": [
        "Aquisição da morfologia verbal por brasileiros",
        "Tradução de termos filosóficos alemão-português",
        "Análise de erros em aprendizes lusófonos",
        "Literatura de migração no contexto europeu",
        "Linguística contrastiva em construções passivas",
        "Metodologias para ensino de alemão técnico"
    ],
    "Letras - Italiano": [
        "Dialetos italianos em comunidades de imigrantes",
        "Tradução de ópera libretti para português",
        "Ensino de italiano através do cinema neorrealista",
        "Linguística histórica do toscano literário",
        "Análise de discurso político na Itália contemporânea",
        "Literatura migrante italo-brasileira"
    ],
    "Letras - Japonês": [
        "Ensino de kanji para falantes de português",
        "Análise de honoríficos em traduções literárias",
        "Linguística contrastiva de estruturas passivas",
        "Mangá como ferramenta para aquisição linguística",
        "Tradução de conceitos estéticos japoneses",
        "Estudos de gênero na literatura japonesa moderna"
    ]
}

cursos = supabase.table("cursos").select("id_curso, nome, id_departamento").execute().data

professores_por_departamento = {}
for dept in supabase.table("departamentos").select("id_departamento").execute().data:
    profs = supabase.table("professores").select("id_professor").eq("id_departamento", dept["id_departamento"]).execute().data
    professores_por_departamento[dept["id_departamento"]] = [p["id_professor"] for p in profs]

registros_tccs = []
id_tcc = 1

for curso in cursos:
    assuntos = assuntos_por_curso.get
