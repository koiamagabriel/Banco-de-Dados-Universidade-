SELECT COUNT(DISTINCT h.id_aluno) AS total_estudantes
FROM historicoescolar h
JOIN curso_disciplina cd ON h.id_disciplina = cd.id_disciplina
JOIN disciplinas d ON cd.id_disciplina = d.id_disciplina
WHERE d.nome = 'Inteligência Artificial';
