SELECT DISTINCT c.nome AS nome_curso
FROM cursos c
JOIN alunos a ON c.id_curso = a.id_curso
JOIN departamentos dep ON c.id_departamento = dep.id_departamento
WHERE dep.nome IN ('Departamento de Computação', 'Departamento de Matemática');
