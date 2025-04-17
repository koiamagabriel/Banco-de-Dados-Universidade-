SELECT 
    cd.id_disciplina, 
    d.nome AS nome_disciplina
FROM curso_disciplina cd
JOIN disciplinas d ON cd.id_disciplina = d.id_disciplina
JOIN cursos c ON cd.id_curso = c.id_curso
WHERE c.nome = 'Ciência da Computação';

SELECT 
    cd.id_disciplina, 
    d.nome AS nome_disciplina
FROM curso_disciplina cd
JOIN disciplinas d ON cd.id_disciplina = d.id_disciplina
JOIN cursos c ON cd.id_curso = c.id_curso
WHERE c.nome = 'Ciência de Dados';
