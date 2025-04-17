SELECT 
    h1.id_aluno,
    h1.id_disciplina,
    h1.semestre AS semestre_reprovado,
    h1.status AS status_reprovado,
    h2.semestre AS semestre_aprovado,
    h2.status AS status_aprovado
FROM historicoescolar h1
JOIN historicoescolar h2 ON h1.id_aluno = h2.id_aluno
                          AND h1.id_disciplina = h2.id_disciplina
                          AND h2.status = 'Aprovado!'
                          AND h1.status = 'Reprovado!'
                          AND CAST(h2.semestre AS INTEGER) = CAST(h1.semestre AS INTEGER) + 1
WHERE h1.status = 'Reprovado!';
