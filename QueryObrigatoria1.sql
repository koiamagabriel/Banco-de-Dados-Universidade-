SELECT 
    t.id_tcc,
    t.assunto AS nome_tcc,
    p.nome AS nome_professor,
    a.nome AS nome_aluno
FROM tccs t
JOIN professores p ON t.id_professor = p.id_professor
JOIN tcc_alunos ta ON t.id_tcc = ta.id_tcc
JOIN alunos a ON ta.id_aluno = a.id_aluno
WHERE p.id_professor = '48';
