SELECT 
    a.id_aluno,
    a.nome AS nome_aluno
FROM tcc_alunos ta
JOIN alunos a ON ta.id_aluno = a.id_aluno
JOIN tccs t ON ta.id_tcc = t.id_tcc
WHERE t.id_professor = '3';
