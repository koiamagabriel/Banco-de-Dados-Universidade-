SELECT DISTINCT a.nome AS nome_estudante
FROM alunos a
JOIN historicoescolar h ON a.id_aluno = h.id_aluno
WHERE h.id_disciplina IN ('CS202', 'CS-204')
GROUP BY a.id_aluno, a.nome
HAVING COUNT(DISTINCT h.id_disciplina) = 2;
