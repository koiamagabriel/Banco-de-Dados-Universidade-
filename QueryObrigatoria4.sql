SELECT 
    d.id_disciplina,
    d.nome AS nome_disciplina,
    p.nome AS nome_professor
FROM historicoescolar h
JOIN disciplinas d ON h.id_disciplina = d.id_disciplina
JOIN disciplinaslecionadas dl ON d.id_disciplina = dl.id_disciplina
JOIN professores p ON dl.id_professor = p.id_professor
WHERE h.id_aluno = 1;  -- Substitua 1 pelo id do aluno que você deseja consultar
